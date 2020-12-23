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

fw = open("../static/data/dict.json", 'w')
json.dump(dd, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))