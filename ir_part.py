# -*- coding: utf-8 -*-
"""
@author: zicheng
"""

from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search, Q
import json

es = Elasticsearch()

index_name = 'subtitle_py'

if es.indices.exists(index=index_name):
    print("{} already exists; let's get rid of it...".format(index_name))
    es.indices.delete(index=index_name)

# comprehensive analyzer

es.indices.create(index=index_name, body={
  "settings": {
    "analysis": {
      "filter": {
        "english_stop": {
          "type":       "stop",
          "stopwords":  "_english_"
        },
        "english_stemmer": {
          "type":       "stemmer",
          "language":   "english"
        },
        "english_possessive_stemmer": {
          "type":       "stemmer",
          "language":   "possessive_english"
        }
      },
      "analyzer": {
        "cjk": {
          "tokenizer":  "standard",
          "filter": [
            "cjk_width",
            "lowercase",
            "cjk_bigram",
            "english_stop"
          ]
        },
        "english": {
          "tokenizer":  "standard",
          "filter": [
            "english_possessive_stemmer",
            "lowercase",
            "english_stop",
            "english_stemmer"
          ]
        }
      }
    }
  }
})


    
# if we've got a larger number of documents, we want to use the bulk API:

"""
with open('data.json', 'r') as f :
    output = json.load(f)
    for line in output:
        print(line)
"""

def subtitle_source(idx_name):
    with open('data.json', 'r') as f:
        for output in f:
            line = json.loads(output)
            #print(line)
            yield {'_index': idx_name, '_id': line['line_id'], '_type': 'document', '_source': line}
    
helpers.bulk(es, subtitle_source(index_name))

# helpers.bulk takes a Python iterable that produces action specifications, so we can stream a large data 
# set and not have to load it all into memory at once.


# either way, we'll want to refresh the index
es.indices.refresh(index=index_name)

####################### Time to query!

with open('input.txt','r') as f_in:
    query_fr = f_in.read().decode('utf8')
with open('output.txt','r') as f_out:
    query_en = f_out.read().decode('utf8')

#query = '姐姐'

#q = Q("multi_match", query = str('妹妹'), fields=["sub_zh", "sub_en"])
q = Q({"query_string":{"default_field":"sub_fr", "query": str(query_fr)}}) | \
    Q ({"query_string":{"default_field":"sub_en", "query": str(query_en)}})

this_search = Search(using=es, index=index_name)
this_search = this_search.highlight("line_id", "sub_en", "sub_fr", fragment_size=50)
this_search = this_search.query(q)

response = this_search.execute()
print("There were {} results!".format(response.hits.total))

# open an html file and save the results in it


with open('./templates/save_res.html', 'w') as f:
    f.write('<!DOCTYPE html> \n')
    f.write('<html> \n')
    f.write('<body> \n')
    f.write('<table style="width:70%"> \n')
    f.write('<tr> \n')
    f.write('<th>id</th> \n')
    f.write('<th>highlight</th>')
    f.write('</tr> \n')
    for hit in response:
        f.write('<tr><th>' + str(hit.line_id) + '</th>')
        f.write('<th>')
        
        for field in hit.meta.highlight:
            if field == "line_id":
                for fragment_title in hit.meta.highlight.line_id:
                    f.write("title:" + fragment_title)
                    #print("trial:" + hit.trials)
            if field == "sub_fr" :
                for fragment_fr in hit.meta.highlight.sub_fr:
                    f.write("\tfr:" + fragment_fr.encode('utf-8'))
                    #print(fragment_fr)
                    #f.write("fr:" + fragment_fr)
                    f.write("\ten:" + hit.sub_en.encode('utf-8'))
            if field == "sub_en" :
                for fragment_en in hit.meta.highlight.sub_en:
                    f.write("\ten:" + fragment_en.encode('utf-8'))
                    f.write("\tfr:" + hit.sub_fr.encode('utf-8'))
            
        f.write('</th></tr>')
    f.write('</table> \n')
    f.write('</body> \n')
    f.write('</html> \n')
