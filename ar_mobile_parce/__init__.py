import re
import csv
import os 

class ar_mobile_parce(object):
    default_indicativo = ''
    codigo_indicativo = {}
    dict_indicativos = {}
    known_structures = [
        ('(0)*(2[0-9][0-9][0-9]|[0-9][0-9][0-9]|11)*(\-)*(15)*(\-)*([3|4|5|6])(\-)*([0-9][0-9][0-9][0-9][0-9][0-9])',
            {
                'indicativo':1,
                'numero':[5,7]
            }
        ),
        ('(15)*(\-)*([4|5|6])(\-)*([0-9][0-9][0-9][0-9][0-9][0-9])',
            {
                'indicativo':False,
                'numero':[2,4]
            }
        )
    ]
 
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + '/data/enacom.csv', 'r') as csvfile:
         spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
         for row in spamreader:
            if row[1] !='SBT':
                self.add_dict_indicativos(row[4],row[5])
        with open(path + '/data/cp_indicativos.csv', 'r') as csvfile:
             spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
             for row in spamreader:
                self.set_codigo_indicativo(str(row[0]),str(row[1]))


    def set_default_indicativo(self,indicativo):
        self.default_indicativo = indicativo

    def set_codigo_indicativo(self,code,indicativo):
        self.codigo_indicativo[code] = indicativo

    def get_codigo_indicativo(self,code):
        if code and code in self.codigo_indicativo :
            return self.codigo_indicativo[code]
        else :
            return self.default_indicativo

    def add_dict_indicativos(self,indicativo,bloque):
        if indicativo in self.dict_indicativos :
            self.dict_indicativos[indicativo].append(bloque)
        else :
            self.dict_indicativos[indicativo]=[bloque]

    def is_mobile(self,indicativo,bloque):
        if indicativo in self.dict_indicativos and  bloque in self.dict_indicativos[indicativo]:
            return True
        return False
    def make_dict(self,structure,mob):
        if structure == False:
             return ''
        if type(structure) is int:
            return mob[structure]
        elif type(structure) is list:
            rtn =[mob[x] for x in structure]
            return ''.join(rtn)

    def parce_text(self,text,it=0):
        mob = re.compile(self.known_structures[it][0]).findall(text)
        if len(mob):    
            return [{'indicativo': self.make_dict(self.known_structures[it][1]['indicativo'],x),
                    'numero': self.make_dict(self.known_structures[it][1]['numero'],x)} for x in mob]

    def format_e164(self,indicativo, number,country='54',mobile='9'):
        return "+%s%s%s%s"%(country,mobile,indicativo,number)
    def get_phones(self,text,code=False):
        rtn = []
        it = 0 
        while it < len(self.known_structures):
        
            phones =  self.parce_text(text,it)
            if phones:
                for phone in phones:
                    indicativo = phone['indicativo'] or self.get_codigo_indicativo(code)
                    bloque = phone['numero'][:3]
                    if self.is_mobile(indicativo,bloque):
                        rtn.append(self.format_e164(indicativo,phone['numero']))
                if len(rtn):
                    return rtn
            it += 1

