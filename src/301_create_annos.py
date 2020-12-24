
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

# ----------

# アノテーション

oids = ["236", "238", "240", "241", "242", "243", "244", "245", "246", "247", 
"248", "249", "250", "251", "252", "253", "254", "255", "256", "257", "258", "260", "261", "262", "263", "264", "265"]

resources2 = {}

ids = {}

errs = []

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

                # 省力
                xywh = res["on"][0]["selector"]["default"]["value"]
                res["on"] = res["on"][0]["full"] + "#" + xywh

                text = res["resource"][0]["chars"]
                cleantext = BeautifulSoup(text, "lxml").text.strip()

                if cleantext not in excel_data:
                    print("err", cleantext)
                    errs.append(cleantext)
                    continue

                m_data = excel_data[cleantext]

                url = "https://toyo-bunko.github.io/app-suikeichuuzu/item/" + cleantext

                html = "[ <a target=\"_blank\" href=\"{}\">{}</a> ]<br/>地名/記述：{}".format(url, cleantext, m_data["地名/記述"])

                res["resource"][0]["chars"] = html

                if manifest not in resources2:
                    ids[manifest] = oid
                    df2["resource"] = []
                    resources2[manifest] = df2
                resources2[manifest]["resource"].append(res)

for manifest in resources2:

    with open("annos/"+str(ids[manifest])+".json", 'w') as f:
        json.dump(resources2[manifest], f, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))