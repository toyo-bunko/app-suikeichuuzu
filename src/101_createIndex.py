import pandas as pd
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import numpy as np
import math
import sys
import argparse
import json
import urllib.parse

path = "../static/data/curation.json"

json_open = open(path, 'r')
df = json.load(json_open)

selections = df["selections"]

print(len(selections))

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

index = []

for selection in selections:
    members = selection["members"]

    manifest = selection["within"]["@id"]

    for member in members:

        metadataObj = {}

        metadata = member["metadata"]

        for m in metadata:
            label = m["label"]
            value = m["value"]

            if label == "表a裏b":
                label = "表裏"

                if value == "a":
                    value = "表"
                elif value == "b":
                    value = "裏"

            if label == "朱z墨m":
                label = "墨朱"

            if label == "地名/記述":
                value2 = value
                for key in dd:
                    if key in value2:
                        value2 = value2.replace(key, dd[key])
                metadataObj["地名"] = [value2]

            if label not in metadataObj:
                metadataObj[label] = []

            values = value if isinstance(value, list) else [str(value)]

            for value in values:

                metadataObj[label].append(value) 

        id = member["label"]

        metadataObj["_label"] = metadataObj["地名/記述"][0]

        metadataObj["_id"] = id
        metadataObj["_image"] = member["thumbnail"]

        mid = member["@id"]

        mid_spl = mid.split("#xywh=")

        canvas = mid_spl[0]
        xywh = mid_spl[1]

        related = "http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest="+manifest+"&canvas="+canvas+"&xywh="+xywh+"&xywh_highlight=border"
        metadataObj["_related"] = related

        metadataObj["_url"] = "https://w3id.org/hpdb/item/" + id

        index.append(metadataObj)

fw = open("../static/data/index.json", 'w')
json.dump(index, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))