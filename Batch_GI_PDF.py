#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pytictoc
t = pytictoc.TicToc()
t.tic()


# In[2]:


from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
from pymongo import MongoClient
import pandas as pd
import re
import gridfs
import datetime

import warnings
warnings.filterwarnings('ignore')


# In[3]:


client = MongoClient("localhost", 27017)
db = client["Batch_GI"]
coll = "Batch_GI"
db_coll = db[coll]

fs = gridfs.GridFS(db)


# In[4]:


path = "/home/controllingde/G/Batch_GI/"


# In[5]:


files = os.listdir(path)


# In[6]:


pdffiles = [path + x for x in files if x.find(".pdf") > 0]


# In[7]:


colnames = ['batch', 'item', '_id', 'FS', 'GI', 'MHD', 'filename']
total_df = pd.DataFrame(columns=colnames)


# In[8]:


datepattern = ".(1[0-2]|0[1-9]|\d)\/([2-9]\d[1-9]\d|[1-9]\d)."
batchsign = "Ch.-B.:"
i = 1
tl = len(pdffiles)

timestamp = str(datetime.datetime.now()).replace(" ", "_")
timestamp = timestamp.replace(":", "-")
timestamp = timestamp[0:19]

new_filename = "Matching_Batch_" + timestamp + ".csv"

for f in pdffiles:
    
    t2 = pytictoc.TicToc()
    t2.tic()
    
    pages = convert_from_path(f, 500)     
    
    image_counter = 1
    
    for p in pages:
        filename = "page_" + str(image_counter) + ".jpg"
        p.save(filename, "JPEG")
        image_counter += 1
    filelimit = image_counter-1
    
    impdict = {}
    for i in range(1, filelimit + 1):
        filename = "page_"+str(i)+".jpg"
        text = str(((pytesseract.image_to_string(Image.open(filename)))))
        text = text.replace('-\n', '')  
    
        batchind_start = text.rindex(batchsign)
    
        batchsub1 = text[(batchind_start + len(batchsign) + 1) : ]
        impdict["batch"] = batchsub1[0: batchsub1.find(" ")]
        impdict["item"] = batchsub1[(batchsub1.find(" ") + 1): batchsub1.find("\n")]
    
        impdict["_id"] = impdict["batch"] + "_" + impdict["item"]
    
        FSsub = batchsub1[batchsub1.find("FS-"): ]
        impdict["FS"] = FSsub[0: FSsub.find("\n")]

        GIsub = batchsub1[batchsub1.find("GI-"): ]
        impdict["GI"] = GIsub[0: GIsub.find("\n")]

        #FOLsub = batchsub1[batchsub1.find("FOL-"): ]
        #impdict["FOL"] = FOLsub[0: FOLsub.find("\n")]
        
        MHD = re.search(datepattern, text)
        impdict["MHD"] = text[MHD.start() : MHD.end()-1]
             
        impdict["filename"] = f
        impdict["fulltext"] = text.split("\n")
        
        impdict["pdffile"] = fs.put(open(f, 'rb'))
        
    db_coll.remove({"_id": impdict["_id"]})
    db_coll.insert_one(impdict)
    
    del impdict["fulltext"]
    del impdict["pdffile"]
    pre_df = pd.DataFrame.from_dict(impdict, orient="index").transpose()
    total_df = pd.concat([total_df, pre_df])
    
    print("{} of {} processed".format(i, tl))
    
    i += 1
    
    t2.toc()
    
total_df.to_csv(path + "test01.csv")
total_df.set_index(["_id"], inplace=True, verify_integrity=True)
t.toc()
#total_df.head()


# In[ ]:


#for checkng monodb
#r = db_coll.find()
#for l in r:
#    print(l)
#    print("\n")


# In[ ]:




