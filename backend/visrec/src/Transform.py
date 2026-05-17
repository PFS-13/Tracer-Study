# import altair as alt
from visrec.src.GetType import get_var_type
import pandas as pd
import re
# import execjs
from copy import deepcopy


def GetNewColumnType(df: pd.DataFrame, ColumnTypes={}):
    header = list(df.columns)
    for h in header:
        if ColumnTypes[h] == 'unknown':
            series_description = get_var_type(df[h])
            ColumnTypes[h] = series_description['type2']
    return ColumnTypes

# Mengubah sebuah DataFrame menjadi ringkasan metadata yang berisi ukuran data, tipe tiap kolom, serta statistik dasar seperti jumlah data,
# nilai kosong, dan nilai unik untuk mendukung analisis atau rekomendasi visualisasi.
def Data2Schema(df: pd.DataFrame, ColumnTypes={}):
    # print("df\n",df,"\nhehe\n",ColumnTypes)
    # example of DF :
    #           Happiness Score  Happiness Rank
    # 0              7.587               1
    # 1              7.561               2
    # 2              7.527               3
    # 3              7.522               4
    # 4              7.427               5
    # ..               ...             ...
    # 310            3.484             153
    # 311            3.360             154
    # 312            3.303             155
    # 313            3.069             156
    # 314            2.905             157
    # [315 rows x 2 columns]


    # example of Column types :
    # {'Happiness Score': 'quantitative', 'Happiness Rank': 'quantitative'}

    info = {'size': df.shape[0], 'stats': {}}
    header = list(df.columns)
    print("info: ",info ,"\n header", header)
    # example of  info : {'size': 315, 'stats': {}}
    # example of header:  ['Happiness Score', 'Happiness Rank']

    # print("\n info :",info)
    # print("\n header: ",header)
    for h in header:
        print("==",h,"==\n")
        series_description = get_var_type(df[h])
        if ColumnTypes[h] == 'unknown':
            ColumnTypes[h] = series_description['type2']
        try:
            info['stats'][h] = {
                'type':     series_description['type1'],
                'count':    len(df[h]),
                'missing':  df[h].isnull().sum(),
                'distinct': series_description['distinct_count_with_nan'],
            }
        except:
            raise Exception(print(h))
        if h in ColumnTypes and ColumnTypes[h] == 'temporal':
            info['stats'][h]['type'] = 'datetime'
        elif h in ColumnTypes and ColumnTypes[h] == 'quantitative':
            info['stats'][h]['type'] = 'number'
    # example of info {'size': 315, 'stats': {'Happiness Score': {'type': 'number', 'count': 315, 'missing': 0, 'distinct': 299}, 'Happiness Rank': {'type': 'number', 'count': 315, 'missing': 0, 'distinct': 158}}}
    print("\n\ninfo_lengkap :",info)
    return info


def Schema2Asp(d: dict):
    # print("dict in s2a",d)
    # example of d: {'size': 315, 'stats': {'Happiness Score': {'type': 'number', 'count': 315, 'missing': 0, 'distinct': 299}, 'Happiness Rank': {'type': 'number', 'count': 315, 'missing': 0, 'distinct': 158}}}

    if len(d) < 1:
        print("No prepared data")
        return None
    asp = ['num_rows(%d).' % (d['size'])]
    for k, v in d['stats'].items():
        asp.append('fieldtype("%s",%s).' % (k, v['type'])) # tipe kolom
        asp.append('cardinality("%s",%d).' % (k, v['distinct'])) # kardinalitas
    # example of asp :['num_rows(315).', 'fieldtype("Happiness Score",number).', 'cardinality("Happiness Score",299).', 'fieldtype("Happiness Rank",number).', 'cardinality("Happiness Rank",158).']
    print("\n=== ASP RESULT ===")
    for item in asp:
        print(item)
    return asp


def Cql2Asp(spec: dict):
    facts = []
    marktype = ['point', 'bar', 'line', 'area', 'text', 'tick', 'rect']
    if 'mark' in spec:
        if spec['mark'] in marktype:
            facts.append('mark("%s").' % (spec['mark']))
    if 'url' in spec['data']:
        facts.append('data("%s").' % (spec['data']['url']))
    elif 'values' in spec['data']:
        facts.append('data(%s).' % (spec['data']['values']))
    else:
        raise Exception("no data found")
    if 'encodings' in spec:
        eid = 0
        for encode in spec['encodings']:
            facts.append('encoding(e%d).' % (eid))
            encFieldType = None
            encZero = None
            encBinned = None
            for k, v in encode.items():
                if v == '?':
                    continue
                if k == 'type':
                    encFieldType = v
                if k == 'bin':
                    encBinned = v
                if k == 'scale':
                    if type(v) == dict and 'zero' in v:
                        encZero = v['zero']
                        if encZero:
                            facts.append('zero(e%d).' % (eid))
                        else:
                            facts.append(':- zero(e%d).' % (eid))
                    if type(v) == dict and 'log' in v:
                        if v['log']:
                            facts.append('log(e%d).' % (eid))
                        else:
                            facts.append(':- log(e%d).' % (eid))
                elif k == 'bin':
                    if type(v) == dict and 'maxbins' in v:
                        facts.append('%s(e%d,%d).' % (k, eid, v['maxbins']))
                    elif v:
                        facts.append(':- not bin(%d,_).' % (eid))
                    else:
                        facts.append(':- bin(%d,_).' % (eid))
                elif k == 'field':
                    facts.append('%s(e%d,"%s").' % (k, eid, v))
                else:
                    if k != 'bin':
                        facts.append('%s(e%d,%s).' % (k, eid, v))
            if encFieldType == 'quantitative' and encZero is None and encBinned is None:
                facts.append('zero(e%d).' % (eid))
            eid += 1
    #example of facts :
    # ['data("./values").', 'encoding(e0).', 'field(e0,"Happiness Score").', 'type(e0,quantitative).', 'encoding(e1).', 'field(e1,"Happiness Rank").', 'type(e1,quantitative).']
    print("HASIL FACTS:")
    print('\n'.join(facts))
    return facts

def Asp2Vl(asp: list, task=None):
    Vl = {"$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "title":{"text":"","anchor":"start"}}
    # ,"width":"container","height":"container"
    pattern = r"(\w+)\(([\w\s\.\/]+)(,([\w\s\.\(\)]+))?\)"
    encodings = {}
    layer = []
    layerson = {}
    isTransform = 0
    #example of ASP
#  {'e0': {'field': 'Happiness Rank', 'type': 'quantitative', 'channel': 'y', 'aggregate': 'mean'}, 'e1': {'field': 'Happiness Score', 'type': 'quantitative', 'channel': 'x', 'bin': '10'}}
#  ['data("./values").', 'field(e0,"Happiness Rank").', 'field(e1,"Happiness Score").', 'type(e0,quantitative).', 'type(e1,quantitative).', 'channel(e0,x).', 'channel(e1,y).', 'bin(e0,10).', 'aggregate(e1,sum).', 'mark(bar).']
    for fact in asp:
        fact = fact.replace('"', '')
        NegFlag = fact.strip().startswith(":-")
        match = re.match(pattern, fact, re.M | re.I)

        if match[1] == "data":
            Vl["data"] = "vegalitedata"
        elif match[1] == "mark":
            layerson["mark"] = {"type": match[2], "tooltip": True}
            if match[2] == "boxplot":
                layerson["mark"]["extent"] = "min-max"
            elif match[2] == "errorband":
                layerson["mark"]["extent"] = "ci"
                layerson["mark"]["borders"] = True
            elif match[2] == "errorbar":
                layerson["mark"]["extent"] = "ci"
                layerson["mark"]["ticks"] = True
        elif match[1] == "transform":
            transform = match[2]
            isTransform = 1
        else:
            if not match[2] in encodings:
                encodings[match[2]] = {}
            encodings[match[2]][match[1]] = match[4] or not NegFlag
    # {'e0': {'field': 'Happiness Rank', 'type': 'quantitative'}, 'e1': {'field': 'Happiness Score', 'type': 'quantitative', 'channel': 'x', 'bin': '10'}, '5': {'channel': 'y', 'aggregate': 'count', 'type': 'quantitative'}}
    encoding = {}
    for v in encodings.values():
        if not 'channel' in v.keys():
            continue

        if v["type"] == "quantitative" and not "zero" in v and not "bin" in v:
            v["zero"] = False

        scale = {}
        if "log" in v and v["log"] == True:
            scale["type"] = "log"
        if "zero" in v:
            scale["zero"] = True if v["zero"] else False

        encoding[v["channel"]] = {}
        encoding[v["channel"]]["type"] = v["type"]
        if "aggregate" in v:
            encoding[v["channel"]]["aggregate"] = v["aggregate"]
        if "field" in v:
            encoding[v["channel"]]["field"] = v["field"]
        if "stack" in v:
            encoding[v["channel"]]["stack"] = v["stack"]
        if "sort" in v:
            encoding[v["channel"]]["sort"] = v["sort"]
        if "bin" in v:
            if int(v["bin"]) == 10:
                encoding[v["channel"]]["bin"] = True
            else:
                encoding[v["channel"]]["bin"] = {"maxbins": int(v["bin"])}
        if len(scale) > 0:
            encoding[v["channel"]]["scale"] = scale
    if layerson["mark"]["type"] == "arc":  # pie
        encoding["color"] = encoding.pop("x")
        encoding["theta"] = encoding.pop("y")

    if layerson["mark"]["type"] == "circle":  # geography
        encoding["longitude"] = encoding.pop("x")
        encoding["latitude"] = encoding.pop("y")

    if layerson["mark"]["type"] in ["errorband", "errorbar"]:  # error_range
        encoding["y"]["title"] = encoding["y"]["field"] + " (95% CIs)"

    layerson["encoding"] = encoding
    layer.append(layerson)

    if isTransform == 1:  # apply transform_type(loess;regression)
        layerSon2 = {}
        layerSon2["mark"] = {
            "type": "line",
            "color": "firebrick",
            "tooltip": True
        }
        layerSon2["transform"] = [
            {
                transform: encoding["y"]["field"],
                "on": encoding["x"]["field"]
            }
        ]
        layerSon2["encoding"] = encoding
        layer.append(layerSon2)

    if task == "deviation":  # add mean rule
        layerSon2 = deepcopy(layerson)
        layerSon2["mark"] = {"type": "rule", "tooltip": True}
        layerSon2["encoding"].pop("x")
        layerSon2["encoding"]["y"]["aggregate"] = "mean"
        layerSon2["encoding"]["color"] = {"value": "red"}
        layerSon2["encoding"]["size"] = {"value": 3}
        layer.append(layerSon2)

    # if layerson["mark"]["type"] == "arc":  # add text for arc
    #     layerSon2 = deepcopy(layerson)
    #     layerSon2["mark"] = {"type": "text", "radius": 100}
    #     layerSon2["encoding"]["text"]=layerSon2["encoding"].pop("color")
    #     layer.append(layerSon2)

    if layerson["mark"]["type"] == "rect":  # add text for rect
        layerSon2 = deepcopy(layerson)
        layerSon2["mark"] = {"type": "text", "tooltip": True}
        layerSon2["encoding"]["text"] = layerSon2["encoding"].pop("color")
        layer.append(layerSon2)

    if task == "spatial":  # spatial
        Vl["width"] = 600
        Vl["height"] = 400
        if layer[0]["mark"]["type"] == "geoshape":
            layer[0]["transform"] = [{"lookup": layer[0]["encoding"]["x"]["field"],
                                      "from": {"data": {"url": "https://vega.github.io/editor/data/us-10m.json", "format": {"type": "topojson", "feature": "states"}}, "key": "id"},
                                      "as": "geo"}]
            if not layer[0]["encoding"]["color"]["type"] in ["nominal", "ordinal"]:
                if layer[0]["encoding"]["color"]["aggregate"] == "count":
                    field_name = layer[0]["encoding"]["x"]["field"]
                else:
                    field_name = layer[0]["encoding"]["color"]["field"]
                aggregate_name = layer[0]["encoding"]["color"]["aggregate"]
                layer[0]["transform"].append({
                    "groupby": [layer[0]["encoding"]["x"]["field"]],
                    "window": [{"op": aggregate_name, "field": field_name, "as": "%s of %s" % (aggregate_name, field_name)}]})
            layer[0]["projection"] = {"type": "albersUsa"}
            layer[0]["mark"] = {"type": "geoshape"}
            layer[0]["encoding"]["shape"] = {"field": "geo", "type": "geojson"}
            if not layer[0]["encoding"]["color"]["type"] in ["nominal", "ordinal"]:
                layer[0]["encoding"]["color"]["field"] = layer[0]["transform"][1]["window"][0]["as"]
                layer[0]["encoding"]["color"].pop("aggregate")
            layer[0]["encoding"].pop("x")

        else:
            if not layer[0]["encoding"]["color"]["type"] in ["nominal", "ordinal"]:
                layerSon2 = deepcopy(layerson)
                layerSon2["mark"] = {"type": "text",
                                    #  "tooltip": True,
                                     "dy": -10, "limit": {"expr": "50"}}
                layerSon2["encoding"]["text"] = layerSon2["encoding"].pop(
                    "color")
                layer.append(layerSon2)

            Tlayer = {
                "data": {
                    "url": "https://vega.github.io/editor/data/us-10m.json",
                    "format": {
                        "type": "topojson",
                        "feature": "states"
                    }
                },
                "projection": {
                    "type": "albersUsa"
                },
                "mark": {
                    "type": "geoshape",
                    # "tooltip":True,
                    "fill": "lightgray",
                    "stroke": "white"
                },
                "encoding": {}
            }
            layer.insert(0, Tlayer)

    Vl["layer"] = layer
    cost = 0
    # cost = round(float(GraphScapeCost(Vl)), 3)
    # PrintVegaLite(Vl,cost)
    # example of V1
    #     {
    #   "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    #   "title": {
    #     "text": "",
    #     "anchor": "start"
    #   },
    #   "data": "vegalitedata",
    #   "layer": [
    #     {
    #       "mark": {
    #         "type": "bar",
    #         "tooltip": true
    #       },
    #       "encoding": {
    #         "x": {
    #           "type": "quantitative",
    #           "field": "Happiness Score",
    #           "bin": true
    #         },
    #         "y": {
    #           "type": "quantitative",
    #           "aggregate": "mean",
    #           "field": "Happiness Rank",
    #           "scale": {
    #             "zero": false
    #           }
    #         }
    #       }
    #     }
    #   ]
    # }
    return Vl, cost


def PrintVegaLite(Vl, cost):
    Tstr = str(Vl).replace('\'', '"')
    Tstr = Tstr.replace('True', 'true')
    Tstr = Tstr.replace('False', 'false')
    print("Vega-Lite:", Tstr)
    print("Cost:", cost)
    print("----------------------------")


# def GetEvalStr(Tstr, v1):
#     for k2, v2 in v1.items():
#         if not (k2 == 'field' or k2 == 'type' or k2 == 'scale'):
#             Tstr = Tstr+","+k2+"='"+str(v2)+"'"
#     Tstr += ")"
#     Tstr = Tstr.replace("'True'", "True")
#     Tstr = Tstr.replace("'False'", "False")
#     return Tstr

# def DrawVegaLite(data, Vl):
#     TypeDic = dict(quantitative='Q', ordinal='O', nominal='N', temporal='T')
#     chart = alt.Chart(data)
#     chart.mark = Vl['mark']
#     encodings = Vl['encoding']
#     encode = []
#     for k1, v1 in encodings.items():
#         if k1 == 'x':
#             xstr = "alt.X('%s:%s'" % (v1['field'], TypeDic[v1['type']])
#             xstr = GetEvalStr(xstr, v1)
#             x = eval(xstr)
#         elif k1 == 'y':
#             ystr = "alt.Y('%s:%s'" % (v1['field'], TypeDic[v1['type']])
#             ystr = GetEvalStr(ystr, v1)
#             y = eval(ystr)
#         elif k1 == 'color':
#             Cstr = "alt.Color('%s:%s'" % (v1['field'], TypeDic[v1['type']])
#             Cstr = GetEvalStr(Cstr, v1)
#             color = eval(Cstr)
#             encode.append('color')
#         elif k1 == 'size':
#             Sistr = "alt.Size('%s:%s'" % (v1['field'], TypeDic[v1['type']])
#             Sistr = GetEvalStr(Sistr, v1)
#             size = eval(Sistr)
#             encode.append('size')
#         elif k1 == 'shape':
#             Shstr = "alt.Shape('%s:%s'" % (v1['field'], TypeDic[v1['type']])
#             Shstr = GetEvalStr(Shstr, v1)
#             shape = eval(Shstr)
#             encode.append('shape')
#     ChartStr = "chart.encode(x,y"
#     for i in encode:
#         ChartStr = ChartStr+","+i
#     ChartStr += ")"
#     chart = eval(ChartStr)
#     return chart
