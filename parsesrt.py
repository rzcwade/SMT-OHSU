# -*- coding: utf-8 -*-
"""
Created on Wed May 24 06:50:41 2017

@author: rzcwa
"""

import json
import pysrt
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#subs = pysrt.open('test1_zh_en.srt')
subs = pysrt.open('ib.srt', encoding='iso-8859-1')


# Writing JSON data
with open('data_fr_en.json', 'w') as f:
    #input = []
    for i in range(len(subs)):
        idx = subs[i].index
        strs = subs[i].text
        strs_sep = re.split(r'\n',strs)
        temp_en = ''
        temp_fr = ''
        for j in range(len(strs_sep)):
            strs_sep_sep = re.split("\s+\.\.\s+", strs_sep[j])
            temp_en += str(strs_sep_sep[0]).decode('utf8')
            temp_fr += str(strs_sep_sep[1]).decode('utf8')
        dict = {"line_id" : idx, "sub_en" : temp_en, "sub_fr" : temp_fr}
        #input.append(dict)
        json.dump(dict, f)
        f.write('\n')
