#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import sqlite3
import csv
import re
import os

#setup connection and cursor
connection = sqlite3.connect('/Users/Akbar/Desktop/Gold_Binar/Gold_Binar.db')
cursor = connection.cursor()

#read sql & make dataframe
Tweet = pd.read_sql_query("select Tweet from data", connection)
Tweet = pd.DataFrame(Tweet, columns = ['Tweet'])
abusive = pd.read_sql_query("select * from abusive", connection)
abusive = pd.DataFrame(abusive, columns =['ABUSIVE'])
alay = pd.read_sql_query("select * from new_kamusalay", connection)
alay = pd.DataFrame(alay, columns =['alay', 'fix_alay'])


#to list
list_tweet = Tweet['Tweet'].str.lower().tolist()
list_abusive = abusive['ABUSIVE'].str.lower().tolist()
list_alay = alay['alay'].str.lower().tolist()
list_alay_fix = alay['fix_alay'].str.lower().tolist()

#necessary step try
alay_map = dict(zip(alay['alay'], alay['fix_alay']))
def kbbi(kalimat):
    for kata_alay in alay_map:
        return ' '.join([alay_map[kata_alay] if kata_alay in alay_map else kata_alay for kata_alay in kalimat.split(' ')])

"""
for kata_alay in kalimat.split(' '):
    if kata_alay in alay_map:
        return(' '.join([alay_map[kata_alay])
    else:
        return(' '.join(kata_alay)
"""
#main process
def cleanse():
    operasi = input('Masukkan operasi cleansing yang dibutuhkan: (1) untuk clean csv (2) untuk clean kalimat:')
    if operasi == '1':
        upload = input('Masukkan path csv yang ingin dicleansing:')
        read_upload = pd.read_csv(
            filepath_or_buffer = upload, dtype={'Tweet': str}, delimiter=';', skiprows=0, low_memory=False, encoding='latin-1',
            header = 0
        )
        read_upload.to_sql
        tweet_csv = pd.DataFrame(data=read_upload, columns =['Tweet'])
        list_tweet_csv = tweet_csv['Tweet'].str.lower().tolist()
        for kalimat in list_tweet_csv:
            kalimat = re.sub('\n',' ', kalimat)
            kalimat = re.sub('rt',' ', kalimat)
            kalimat = re.sub('user',' ', kalimat)
            kalimat = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',kalimat)
            kalimat = re.sub('  +',' ', kalimat)
            kalimat = re.sub('[^0-9a-zA-Z]+', ' ', kalimat)
            kalimat = re.sub('  +',' ', kalimat)
            kalimat = kbbi(kalimat)
            for kalimat in list_tweet_csv :
                kalimat = re.split(" ", kalimat)
                for kata in kalimat :
                    if kata in list_abusive :
                        kalimat[kalimat.index(kata)] = kalimat[kalimat.index(kata)].replace(kata, "**")
                        tweet_fix = " ".join(kalimat)
                        tweet_fix = kalimat
                        cursor.execute('''CREATE TABLE IF NOT EXISTS Tweet(tweet TEXT, tweet_fix TEXT)''')
                        cursor.execute('''insert into Tweet (tweet,tweet_fix) values (?, ?) (kalimat, tweet_fix)''')
                        connection.commit()
                        print('data cleansing csv selesai')

                            
    elif operasi == '2':
        kalimat = input('Masukkan kata yang ingin dicleansing:')
        kalimat = kalimat.lower()
        kalimat = re.sub('\n',' ', kalimat)
        kalimat = re.sub('rt',' ', kalimat)
        kalimat = re.sub('user',' ', kalimat)
        kalimat = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',kalimat)
        kalimat = re.sub('  +',' ', kalimat)
        kalimat = re.sub('[^0-9a-zA-Z]+', ' ', kalimat)
        kalimat = re.sub('  +',' ', kalimat)
        kalimat = kbbi(kalimat)
        kata = kalimat.split()
        for k in kata:
            for a in list_abusive:
                if a in k:
                    kata[kata.index(k)] = kata[kata.index(k)].replace(k, "**")
                    kalimat = " ".join(kata)
                    print('kalimat yang telah dicleansing:')
                    print(kalimat)
cleanse()


# In[ ]:





# In[ ]:




