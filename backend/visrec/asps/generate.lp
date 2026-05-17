% ====== Generators ======

% encodings

% maximum number for each multi channel encoding
#const max_extra_encs = 5.


obj_id(1..max_extra_encs).

%Mendefinisikan daftar kandidat encoding
encode(e0;e1;e2;e3;e4;e5;e6;e7;e8;e9;e10;e11;e12;e13).
%Untuk setiap E yang merupakan obj_id, boleh memilih atau tidak memilih encoding(E)
{ encoding(E): obj_id(E) }.

% Symmetry Breaking Constraint
% membatasi pilihan supaya tidak bolong
% encoding nya gak boleh meloncat
:- not encoding(ID), encoding(ID-1), obj_id(ID), obj_id(ID-1).

% properties of encodings

% channel and type have to be present
% untuk setiap pasangan (E,C) di mana C adalah channel,boleh memilih 0 atau 1
% rule ini hanya berlaku jika encoding(E) aktif
% Untuk setiap encoding E yang dipilih, dia boleh punya maksimal 1 channel (atau tidak punya sama sekali)
% encoding itu pemetaan
0 { channel(E,C): channel(C) } 1 :- encoding(E).
% 0 { type(E,T): type(T) } 1 :- encoding(E).
% Kalau encoding sudah dipakai (punya channel), maka dia harus tahu tipe datanya
% memastikan setiap encoding yang aktif punya definisi tipe data
{ type(E,T): type(T) } =1 :- channel(E,_).
% :- { channel(_,_)}<2.

% Harus ada 1 channel
:- { channel((e0;e1;e2;e3;e4;e5;e6;e7),_)}<1.

% field ADA + type TIDAK ADA → SOLUSI DITOLAK
% hanya berlaku untuk id yang valid / termasuk objek encoding
:- not type(ID,_),field(ID,_),obj_id(ID).

% :- not channel(ID,_),type(ID,_),obj_id(ID).
% :- not field(ID,_),type(ID,_),obj_id(ID).

%Jika ada aggregate → wajib ada channel
%Jika ada bin -> wajib ada channel 
:- not channel(E,_),aggregate(E,_).
:- not channel(E,_),bin(E,_).
% :- not channel(E,_),zero(E).

% other properties that are not required
% optional tapi maksimal 1
0 { field(E,F): field(F) } 1 :- encoding(E).
0 { aggregate(E,A): aggregate_op(A) } 1 :- encoding(E).
0 { bin(E,B): binning(B) } 1 :- encoding(E).
% 0 { zero(E) } 1 :- encoding(E).
% 0 { log(E) } 1 :- encoding(E).

% pick one mark type
{ mark(M) : marktype(M) } = 1.

% stacking
0 { stack(S): stacking(S) } 1.

% transform
0 { transform(S): transform_type(S) } 1.

% sort
0 { sort(E,S): sort_type(S) } 1 :- encoding(E).