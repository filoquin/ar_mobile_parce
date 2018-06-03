import re
import csv
import os 


class ar_mobile_parce(object):
    default_indicativo = ''
    codigo_indicativo = {'9120': [], '8361': [], '8363': [], '8364': [], '9203': [], '8360': [], '9107': [], '9105': [], '8153': [], '3630': ['3715'], '8307': [], '9015': [], '8305': ['299'], '8160': [], '8303': ['299'], '8328': [], '8301': ['299'], '8300': ['299'], '8324': ['299'], '8136': [], '8326': [], '8347': [], '8132': [], '9200': [], '8520': [], '8370': [], '0': [], '9400': ['2902'], '8309': ['299'], '9420': [], '9220': [], '7530': [], '8105': ['291'], '8148': [], '3600': ['370'], '8101': [], '8103': ['299'], '9111': [], '8142': [], '8109': [], '9103': [], '8315': ['2942'], '8316': ['299'], '8336': [], '9100': [], '9001': [], '9000': ['297'], '8146': [], '8000': ['291'], '9020': ['297'], '3400': ['379'], '9410': [], '9017': [], '7540': [], '9011': []}
    dict_indicativos = {}
    known_structures = [
        ('(0)*([0-9][0-9][0-9]|11)*(\-)*(15)*(\-)*([3|4|5|6])(\-)*([0-9][0-9][0-9][0-9][0-9][0-9])',
            {
                'indicativo':1,
                'numero':[5,7]
            }
        ),
        ('(0)*([0-9][0-9][0-9][0-9])*(\-)*(15)*(\-)*([3|4|5|6])(\-)*([0-9][0-9][0-9][0-9][0-9])',
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
        ),
        ('(15)*(\-)*([4|5|6])(\-)*([0-9][0-9][0-9][0-9][0-9])',
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


    def set_default_indicativo(self,indicativo):
        self.default_indicativo = indicativo

    def set_codigo_indicativo(self,code,indicativo):
        self.codigo_indicativo[code] = indicativo

    def get_codigo_indicativo(self,code):
        if code and code in self.codigo_indicativo :
            return self.codigo_indicativo[code]
        else :
            return [self.default_indicativo]

    def get_indicativo_bloques_size(self,indicativo):
        if indicativo in self.dict_indicativos :
            size = [len(x) for x in self.dict_indicativos[indicativo]]
            return list(set(size))
        else :
            return [0]

    def add_dict_indicativos(self,indicativo,bloque):
        if indicativo in self.dict_indicativos :
            self.dict_indicativos[indicativo].append(bloque)
        else :
            self.dict_indicativos[indicativo]=[bloque]

    def is_mobile(self,indicativo,bloque):
        if indicativo in self.dict_indicativos and \
            bloque in self.dict_indicativos[indicativo]:
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
                    if phone['indicativo']: 
                        indicativos= [phone['indicativo']]
                    else:     
                        indicativos = self.get_codigo_indicativo(code)

                    for indicativo in indicativos:
                        for  bloque_size in self.get_indicativo_bloques_size(indicativo):
                            bloque = phone['numero'][:bloque_size]
                            if self.is_mobile(indicativo,bloque):
                                rtn.append(self.format_e164(indicativo,phone['numero']))
                if len(rtn):
                    return rtn
            it += 1
