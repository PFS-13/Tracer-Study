% ====== Definitions ======

% Tipe visualisasi yang akan dihasilkan.
marktype(point;bar;line;area;rect;arc;circle;tick;boxplot;errorband;errorbar;text;geoshape).
% Tipe data untuk visualisasi
type(quantitative;ordinal;nominal;temporal).
% Tipe data primitif / database
primitive_type(string;number;boolean;datetime).
% Tipe dasar dalam transformasi statistik
% regression digunakan untuk mencari hubungan matematis antar variable
% 
transform_type(loess;regression).
% Dapat diurutkan berdasarkan channel Y.
sort_type(y).
% Fungsi aggregat yang didukung
% aggregate_op(count;mean;median;min;max;stdev;sum).
aggregate_op(count;mean;sum;median).
summative_aggregate_op(count;sum).
% Angka bin yang direkomendasikan
binning(10;25;200).

% Encoding channels.//text,row,column
single_channel(x;y;color;size;shape;text).
% multi_channel(detail).

% semua yang termasuk single_channel otomatis dianggap sebagai channel
% A benar jika B benar
channel(C) :- single_channel(C).
% channel(C) :- multi_channel(C).
non_positional(color;size;shape;detail).

% Possible tasks.
tasks(correlate;change_over_time;magnitude;comparison;spatial;deviation;trend;bi_variate;error_range).
% tasks(value;summary).

% Possible stackings.
stacking(zero;normalize).
% zero : nilai asli, tinggi batang berbeda
% normalize : persentase, tinggi batang sama. 
% stacking(zero;normalize;center;null).
% stacking(normalize).



% ====== Helpers ======
% sebuah encoding dianggap discrete jika nominal dan ordinal datanya
discrete(E) :- type(E,(nominal;ordinal)).
% encoding yang dibinning juga dianggap discrete.
% karena data binning diubah menjadi interval kategori
discrete(E) :- bin(E,_). 
% encoding dianggap continuous dia encoding valid dan bukan discrete
continuous(E) :- encoding(E), not discrete(E).
% sebuah channel dianggap discrete jika ada encoding discrete yang menggunakan channel tersebut. dan seperti itu
channel_discrete(C) :- discrete(E), channel(E,C).
channel_continuous(C) :- continuous(E), channel(E,C).

ordered(E) :- type(E,(ordinal;quantitative)).

% Fields
%F adalah sebuah field jika F memiliki tipe (fieldtype)
field(F) :- fieldtype(F,_).

% Stacking is applied to the continuous x or y.
stack(EC,S) :- channel(EC,(x;y)), channel(ED,(x;y)), continuous(EC), discrete(ED), stack(S).
% X and y are continuous.
stack(E,S) :- channel_continuous(x), channel(E,y), continuous(E), stack(S).

stack(S) :- stack(_,S).

% Data properties
% example : field(e1, gender). cardinality(gender, 2).
% enc_cardinality(e1,2)
enc_cardinality(E,C) :- field(E,F), cardinality(F,C).
enc_entropy(E,EN) :- field(E,F), entropy(F,EN).
%enc_interesting(E) :- field(E,F), interesting(F).
%enc_extent(E,MIN,MAX) :- field(E,F), extent(F,MIN,MAX).

% Cardinality of discrete field. A binned field has the cadinality of its field.
discrete_cardinality(E,CE) :- discrete(E), enc_cardinality(E,CE), channel(E,C), not bin(E,_).
discrete_cardinality(E,CB) :- channel(E,C), bin(E,CB).

% Define a fake soft/2 for all soft/1.
% soft(F,_placeholder) :- soft(F).

% Silence warnings about properties never appearing in head.
% entropy(0,0) :- #false.
% interesting(0) :- #false.
% extent(0,0,0) :- #false.
% soft(0) :- #false.
% data(0) :- #false.

% == Chart Types ==
% Continuous by continuous.
is_c_c :- channel_continuous(x), channel_continuous(y).
% Continuous by discrete (or continuous only).
is_c_d :- channel_continuous(x), not channel_continuous(y).
is_c_d :- channel_continuous(y), not channel_continuous(x).

% Discrete by discrete.
is_d_d :- channel_discrete(x), channel_discrete(y).
is_d :- channel_discrete(x)

% == Overlap ==

% The continuous variable is a measure (it is aggregated) and all other channels are .aggregated, or we use stack -> no overlap
% Kondisi no_overlap (tidak terjadi overlap visual) terpenuhi jika:ada kombinasi data tertentu (is_c_d),ada encoding kontinu (continuous(E)),encoding itu berada di sumbu x atau y, nilai tersebut sudah di-aggregate, dan tidak ada kasus data kontinu yang belum di-aggregate yang menyebabkan overlap
non_pos_unaggregated :- channel(E,C), non_positional(C), not aggregate(E,_).
no_overlap :- is_c_d, continuous(E), channel(E,(x;y)), aggregate(E,_), not non_pos_unaggregated.
no_overlap :- is_c_d, stack(_).

% the size of the discrete positional encoding
discrete_size(S) :- is_c_d, x_y_cardinality(_,S).
discrete_size(1) :- is_c_d, channel_continuous(x), not channel(_,y).
discrete_size(1) :- is_c_d, channel_continuous(y), not channel(_,x).

% Data size is as small as discrete dimension -> no overlap.
no_overlap :- is_c_d, num_rows(S), discrete_size(S).

% We definitely overlap if the data size > discrete size.

overlap :- is_c_d, not no_overlap, num_rows(S1), discrete_size(S2), S1 > S2.

% helpers to go from quadratic to linear number of grounding
x_y_cardinality(x,S) :- channel(E,x), discrete_cardinality(E,S).
x_y_cardinality(y,S) :- channel(E,y), discrete_cardinality(E,S).

% No overlap if all other dimensions are aggregated.
discrete_size(S) :- is_d_d, x_y_cardinality(x,SX), x_y_cardinality(y,SY), S = SX*SY.
no_overlap :- is_d_d, not non_pos_unaggregated.
no_overlap :- is_d_d, num_rows(S1), discrete_size(S2), S1 <= S2.  % This cannot guarantee no overlap.

% We can guarantee overlap using this rule unless we are using row / column.
row_col :- channel(_,(row;column)).
overlap :- is_d_d, channel(E,C), not row_col, not no_overlap, num_rows(S1), discrete_size(S2), S1 > S2.

% == Orientation ==

% Orientation tells us which one is the dependent and independent variable.

orientation(vertical) :- mark(bar;tick;area;line), channel_discrete(x).
orientation(vertical) :- mark(area;line), channel_continuous(x), channel_continuous(y).
orientation(horizontal) :- mark(bar;tick;area;line), channel_discrete(y).
