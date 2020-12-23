
import numpy as np
import math
import sys
import argparse
import json
import html
import requests
import os
from bs4 import BeautifulSoup
import glob
import pandas as pd
import urllib.parse

title = "水経注図"
legend = "https://nakamura196.github.io/suikeichuuzu/etc/legend.pdf"
curation_id = "https://nakamura196.github.io/suikeichuuzu/curation/test.json"

iconMap = {}

iconMap = {
    "0" : {
        "color" : "ff7f7f",
        "exp1" : "[なし]",
    },
    "1" : {
        "color" : "ff7fbf",
        "exp1" : "水",
    },
    "2" : {
        "color" : "ff7fff",
        "exp1" : "故瀆",
    },
    "3" : {
        "color" : "bf7fff",
        "exp1" : "注所敘有誤者",
    },
    "4" : {
        "color" : "7f7fff",
        "exp1" : "山谷",
    },

    "5" : {
        "color" : "7fbfff",
        "exp1" : "陂澤",
    },
    "6" : {
        "color" : "7fffff",
        "exp1" : "北魏",
        "exp2" : "州",
    },
    "7" : {
        "color" : "7fffbf",
        "exp1" : "北魏",
        "exp2" : "郡",
    },
    "8" : {
        "color" : "7fff7f",
        "exp1" : "北魏",
        "exp2" : "縣",
    },
    "9" : {
        "color" : "bfff7f",
        "exp1" : "故城",
        "exp2" : "州郡",
    },
    "10" : {
        "color" : "ffff7f",
        "exp1" : "故城",
        "exp2" : "縣",
    },
    "11" : {
        "color" : "ffbf7f",
        "exp1" : "故城",
        "exp2" : "州廢而郡縣存者",
    },
    "12" : {
        "color" : "ffa3a3",
        "exp1" : "故城",
        "exp2" : "州存而郡縣廢者",
    },
    "13" : {
        "color" : "ffa3d1",
        "exp1" : "故城",
        "exp2" : "州郡存而縣廢者",
    },
    "14" : {
        "color" : "ffa3ff",
        "exp1" : "故城",
        "exp2" : "郡存而縣廢者",
    },
    "15" : {
        "color" : "d1a3ff",
        "exp1" : "故城",
        "exp2" : "郡廢而縣存者",
    },
    "16" : {
        "color" : "a3a3ff",
        "exp1" : "故城",
        "exp2" : "其他地名及亭臺等",
    },
    "17" : {
        "color" : "a3d1ff",

        "exp1" : "[なし]",
        "exp3" : "菱形",
    },
    "18" : {
        "color" : "a3ffff",

        "exp1" : "[なし]",
        "exp3" : "二重菱形",
    },
    "19" : {
        "color" : "a3ffd1",
        "exp1" : "[なし]",
        "exp3" : "縦長四角",
    },
    "20" : {
        "color" : "a3ffa3",
        "exp1" : "[なし]",
        "exp2" : "橋・津・梁・桁",
    },

    "21" : {
        "color" : "d1ffa3",
        "exp1" : "[なし]",
        "exp2" : "井",
    },
    "22" : {
        "color" : "ffffa3",
        "exp1" : "[なし]",
        "exp2" : "長城",
    },
    "23" : {
        "color" : "ffd1a3",
        "exp1" : "[なし]",
        "exp2" : "土州",
    },
    "24" : {
        "color" : "ff7fbf",
        "exp1" : "[なし]",
        "exp2" : "陵",
    },
    "25" : {
        "color" : "ff7fbf",
        "exp1" : "[なし]",
        "exp2" : "門",
    },
    "26" : {
        "color" : "ff7fbf",
        "exp1" : "[なし]",
    },
    "27" : {
        "color" : "ff7fbf",
        "exp1" : "[なし]",
    },
    "28" : {
        "color" : "ff7fbf",
        "exp1" : "[なし]",
    },
    "29" : {
        "color" : "ff7fbf",
        "exp1" : "[なし]",
    },
    "30" : {
        "color" : "ff7fbf",
        "exp1" : "[なし]",
    },
    "31" : {
        "color" : "ff7fbf",
        "exp1" : "[なし]",
    },
    "32" : {
        "color" : "ff7fbf",
        "exp1" : "[なし]",
    },
}

for i in range(0, 33):
    if str(i) not in iconMap:
        iconMap[str(i)] = {
            "color" : "ff7f7f",
            "exp1" : "[なし]"
        }# https://cdn.mapmarker.io/api/v1/pin?size=30&background=%23{}&text={}&color=%23FFFFFF&voffset=2&hoffset=1".format("", i)

# manifest = "https://nakamura196.github.io/suikeichuuzu/iiif/main/manifest.json"

# ----------

# メタデータ
names = ["水経注図地名アノテーション01-04-matome20201217", "水経注図地名アノテーション09Saiiki-matome20201217", "水経注図地名アノテーション11Etsunan-matome20201217"]
excel_data = {}

for name in names:



    excel_path = "/Users/nakamurasatoru/git/d_toyo/suikeichuuzu/data_20201220/"+name+".xlsx"

    df = pd.read_excel(excel_path, sheet_name=0, header=None, index_col=None, engine='openpyxl')

    r_count = len(df.index)
    c_count = len(df.columns)



    for j in range(1, r_count):
        id = df.iloc[j, 0]
        # print(id)
        excel_data[id] = {
            "冊" : df.iloc[j, 1],
            "図" : df.iloc[j, 2],
            "区画南北" : df.iloc[j, 3],
            "区画東西" : df.iloc[j, 4],
            "表裏" : df.iloc[j, 5],
            "詳細区画" : df.iloc[j, 6],
            "墨朱" : df.iloc[j, 7],
            "記号" : df.iloc[j, 8],
            "地名/記述" : df.iloc[j, 9],
            "備考" : df.iloc[j, 10],
        }

# ---------

# 辞書

import csv

f = open('data/dict.csv', 'r')

dd = {}

reader = csv.reader(f)
header = next(reader)
for row in reader:
    key = row[0]
    for i in range(1, len(row)):
        if row[i] != "":
            dd[row[i]] = key

f.close()

# ----------

# 水名


excel_path = "/Users/nakamurasatoru/git/d_toyo/suikeichuuzu/data_20201220/水経注図巻・水名-冊・図名対応20201208.xlsx"

df = pd.read_excel(excel_path, sheet_name=0, header=None, index_col=None, engine='openpyxl')

r_count = len(df.index)
c_count = len(df.columns)

fields = {}

for i in range(3, c_count):
    fields[i] = {
        "巻" : df.iloc[2, i],
        "水名" : df.iloc[3, i]
    }

excel_data2 = {}

for j in range(4, r_count):
    key = df.iloc[j, 2]

    excel_data2[key] = {}
    
    for i in fields:
        if not pd.isnull(df.iloc[j, i]):
            excel_data2[key][i] = {
                "order" : df.iloc[j, i],
                "value" : fields[i]["水名"],
                "vol" : fields[i]["巻"]
            }

# ----------

# アノテーション

oids = ["236", "238", "240", "241", "242", "243", "244", "245", "246", "247", 
"248", "249", "250", "251", "252", "253", "254", "255", "256", "257", "258", "260", "261", "262", "263", "264", "265"]

resources2 = {}

for oid in oids:
    files = glob.glob("/Users/nakamurasatoru/git/d_omeka/omekac_diyhistory/docs/oa/collections/"+oid+"/manifest.json")

    for file in files:

        with open(file) as f:
            df = json.load(f)

        manifest = df["metadata"][0]["value"]
        print(manifest)

        canvases = df["sequences"][0]["canvases"]

        for canvas in canvases:

            uri = canvas["otherContent"][0]["@id"]
            oid2 = uri.split("/")[-2]

            file2 = "/Users/nakamurasatoru/git/d_omeka/omekac_diyhistory/docs/oa/items/"+oid2+"/annolist.json"

            with open(file2) as f:
                df2 = json.load(f)

            _resources = df2["resources"]

            for res in _resources:
                res["image"] = canvas["images"][0]["resource"]["service"]["@id"]
                
                

                if manifest not in resources2:
                    resources2[manifest] = []
                resources2[manifest].append(res)

# ----------

# ----------



errs = []

selections = []

for manifest in resources2:

    print(manifest)

    members = []

    resources = resources2[manifest]

    for i in range(len(resources)):
        index = str(i + 1)

        if i % 1000 == 0:
            print(index, len(resources))

        resource = resources[i]

        canvas = resource["on"][0]["full"]
        xywh = resource["on"][0]["selector"]["default"]["value"]

        memberId = canvas + "#" + xywh
        text = resource["resource"][0]["chars"]
        
        cleantext = BeautifulSoup(text, "lxml").text.strip()

        # -----------

        if cleantext not in excel_data:
            print("err", cleantext)
            errs.append(cleantext)
            continue

        m_data = excel_data[cleantext]

        # -------

        # マーカー
        
        label = "Marker "+index

        no = str(m_data["記号"])


        if no not in iconMap:
            print("icon err", cleantext)
            continue
        iconInfo = iconMap[no]

        # icon = iconMap[str(no)]+"#xy=15,15"

        icon = "https://cdn.mapmarker.io/api/v1/pin?size=30&background=%23{}&text={}&color=%23FFFFFF&voffset=2&hoffset=1#xy=15,15".format(iconInfo["color"], no)

        

        # -------

        icc2 = "https://nakamura196.github.io/icc2/item?id=" + urllib.parse.quote(memberId) + "&u=" + curation_id 

        iconExp = iconInfo["exp1"] + (" - {}".format(iconInfo["exp2"]) if "exp2" in iconInfo else "") + ("（{}）".format(iconInfo["exp2"]) if "exp2" in iconInfo else "")

        html = "[ <a target=\"_blank\" href=\"{}\">{}</a> ]<br/>地名/記述：{}<br/>図記号：{}".format(icc2, cleantext, m_data["地名/記述"], iconExp)

        location = m_data["地名/記述"]

        
        location2 = location
        for key in dd:
            if key in location2:
                location2 = location2.replace(key, dd[key])

        metadata = [
            {
                "value": [
                {
                    "motivation": "sc:painting",
                    "resource": {
                    "chars": html,
                    "@type": "cnt:ContentAsText",
                    "format": "text/html",
                    "marker": {
                        "@id": icon,
                        "@type": "dctypes:Image"
                    }
                    },
                    "@id": memberId+"_",
                    "on": memberId,
                    "@type": "oa:Annotation"
                }
                ],
                "label": "Annotation"
            },
            {
                "value": m_data["冊"],
                "label": "冊"
            },
            {
                "value": m_data["図"],
                "label": "図"
            },
            {
                "value": m_data["区画南北"],
                "label": "区画南北"
            },
            {
                "value": m_data["区画東西"],
                "label": "区画東西"
            },
            {
                "value": "表" if m_data["表裏"] == "a" else "裏",
                "label": "表裏"
            },
            {
                "value": m_data["詳細区画"],
                "label": "詳細区画"
            },
            {
                "value": m_data["墨朱"],
                "label": "墨朱"
            },
            {
                "value": m_data["記号"],
                "label": "図記号"
            },
            {
                "value": iconExp,
                "label": "図説明"
            },
            {
                "value": location,
                "label": "地名/記述"
            },{
                "value": location2,
                "label": "地名"
            }
            
        ]

        if not pd.isnull(m_data["備考"]):
            metadata.append({
                "value":  m_data["備考"],
                "label": "備考"
            })

        # -------

        # 水名

        loc = "{}{}".format(m_data["区画南北"],m_data["区画東西"])
        

        #### 注意！存在しないものあり
        if loc in excel_data2:

            etc = excel_data2[loc]

            vols = []
            names = []

            for etc_index in etc:

                vols.append(etc[etc_index]["vol"])
                names.append(etc[etc_index]["value"])

                '''
                metadata.append({
                    "label":  "巻",
                    "value": etc[etc_index]["vol"]
                })

                metadata.append({
                    "label":  "水名",
                    "value": etc[etc_index]["value"]
                })
                '''

            if len(vols):
                metadata.append({
                    "label":  "水名",
                    "value": names
                })

                metadata.append({
                    "label":  "水経注：巻",
                    "value": vols
                })

        # -------        

        member = {
            "label": cleantext,
            "@type": "sc:Canvas",
            "metadata": metadata,
            "@id": memberId,
            "thumbnail" : resource["image"] + "/"+xywh.split("=")[1]+"/256,/0/default.jpg"
            }

        members.append(member)

    selections.append({
      "within": {
        "@id": manifest,
        "@type": "sc:Manifest"
      },
      "@id": curation_id + "/range"+str(len(selections)+1),
      "label": "Markers",
      "members": members,
      "@type": "sc:Range"
    })

curation = {
  "@type": "cr:Curation",
  "viewingHint": "annotation",
  "@context": [
    "http://iiif.io/api/presentation/2/context.json",
    "http://codh.rois.ac.jp/iiif/curation/1/context.json"
  ],
  "label": title,
  "selections": selections,
  "@id": curation_id,
  "related": {
    "@type": "cr:MarkerLegend",
    "@id": legend
  }
}

with open("../static/data/curation.json", 'w') as f:
    json.dump(curation, f, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))

# print("errs", errs)