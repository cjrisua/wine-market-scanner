import wineclasslib as wlib
import re
from itertools import groupby

wines = [
    wlib.Wine("2015 Quivet Cellars Sauvignon Blanc Beckstoffer Las Piedras Vineyard", "USA> California> Napa Valley", "Red"),
    wlib.Wine("2015 Quivet Cellars Red Beckstoffer Las Piedras Vineyard", "USA> California> Napa Valley", "Red")
]
for key, value in groupby(filter(lambda x: x.varaietal == "unknow", wines), key=lambda w: w.producer):
    print key
    for wine in value:
        print "\t %s %s" % (wine.vintage, wine.varaietal)