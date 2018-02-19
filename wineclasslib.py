from enum import Enum
import re

# Wine class definition
class Type(Enum):
    Red = 1
    White = 2
    Rose = 3
    Other = 0

class VaraietalType(object):
    grapes = ['Pinot Noir', 'Grenache','Merlot','Sangiovese','Nebbiolo','Tempranillo','Cabernet Sauvignon',
    'Syrah','Malbec','Pinot Grigio','Riesling','Sauvignon Blanc','Chenin Blanc','Moscato','Gewurztraminer','Semillon',
    'Viognier','Chardonnay','Zinfandel','Cabernet Franc','Petit Verdot','Mourvedre','Petite Sirah', 'Proprietary Red',
    'Garnacha']

def lazy_property(fn):
    attr_name = "lazy_" + fn.__name__
    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property

class Wine:
    def __init__(self, name, region, winetype):
        
        self.__score = ""
        self.__bottlecount = 0
        self.__rawname = name
        self.__rawtype = winetype.lower()

        self.__vb = []
        self.__varaietal = []
        self.__producer = []
        
        
        self.__rawterroir  = list(map(lambda x: x.strip(), region.split(">")))

        if self.__rawterroir:
            if len(self.__rawterroir) > 0:
                self.__country = self.__rawterroir[0] 
            if len(self.__rawterroir) > 1:
                self.__region = self.__rawterroir[1]
            if len(self.__rawterroir) > 2:
                self.__appelation = self.__rawterroir[len(self.__rawterroir) - 2]
            if len(self.__rawterroir) > 3:
                self.__appelation = self.__rawterroir[len(self.__rawterroir) - 1]
        
        if self.__rawterroir[0] == "France":
            if len(self.__rawterroir) > 1  and self.__rawterroir[1] == "Bordeaux":
                self.__varaietal = "Red Blend"

    #vintage Bottle
    @lazy_property
    def vintage(self):
        match = re.search('^(?P<vintage>([0-9]+|NV))\s+(?P<name>.+?)$', self.__rawname)
        
        if match is None:
            self.__vb = 0
        else:
            year = match.group('vintage')
            if year == "NV" or year.isdigit():
                self.__rawname = self.__rawname.replace(year,"|:|YEAR|:|")
                self.__vb = year
            else:
                self.__vb = 0
        return self.__vb

    #Producer
    @lazy_property
    def producer(self):
        #print (self.__rawname)

        if not self.__vb:
            self.vintage
        if not self.__varaietal:
            self.varaietal
        
        if self.__country == "France":
            match = re.search('^\|\:\|YEAR\|\:\|(?P<producer>.+?)$', self.__rawname)
        else:
            match = re.search('^\|\:\|YEAR\|\:\|(?P<producer>.+?)((\|\:\|VARAIETAL\|\:\|)(.+?)|(\|\:\|VARAIETAL\|\:\|)|$)$', self.__rawname)
        house = match.group('producer').strip()
        return house
    
    @lazy_property
    def varaietal(self):
        grapes = []
        pword = ""

        if self.country == "France":
            return "Red Blend"

        for word in re.split("\\s+", self.__rawname):
            grapes = self.findvaraietal("%s %s" % (pword,word))
            if grapes:
                if(len(grapes) > 1):
                    pword = word
                    continue
                self.__rawname = self.__rawname.replace(grapes[0],"|:|VARAIETAL|:|")
                return grapes[0]
        return "unknow"
    #Type 
    @lazy_property
    def type(self):
        if "red" in self.__rawtype:
            return Type.Red
        elif "white" in self.__rawtype:
            return Type.White
        else:
            return Type.Other
    
    @lazy_property
    def country(self):
        if len(self.__rawterroir) > 0:
            return self.__rawterroir[0]
        else:
            return "unknow"

    @lazy_property
    def region(self):
        if len(self.__rawterroir) > 1:
            return self.__rawterroir[1]
        else:
            return "unknow"

    @lazy_property
    def subregion(self):
        if len(self.__rawterroir) > 2:
            return self.__rawterroir[2]
        else:
            return "unknow"
    @lazy_property
    def appelation(self):
        if len(self.__rawterroir) > 3:
            return self.__rawterroir[3]
        else:
            return "unknow"
    @lazy_property
    def score(self):
        return self.__score

    @lazy_property
    def count(self):
        return self.__bottlecount

    def addscore(self, winescore):
        self.__score =  float(winescore)

    def updatebottlecount(self, bottlecount):
        self.__bottlecount =  int(bottlecount)
        
    def findvaraietal(self, name):
        results = list(filter(lambda g: g.startswith(name.strip()) , VaraietalType.grapes))  
        return results