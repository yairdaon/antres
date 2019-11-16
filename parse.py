import pandas as pd
import numpy as np
import seaborn as sns
from langdetect import detect
from googletrans import Translator
import os
import pickle
from langdetect import detect

if not os.path.exists('data'):
    os.mkdir('data')


    
trans = Translator()
parser = lambda x: trans.translate(x).text
cols_translate = [
    'gender',
    'name',
    'diagnosis_type',	
    'status_at_reception',
    'status_before',
    'arrived_from',
    'autolab',
    'status_before_hospitalization',
    'sample_taken_from',
    'referred_by',
    'gender_'
]    

def robust_detect(s):
    try:
        return detect(s)
    except:
        return ' '

# def col_names_dict():
    
def translate_col_names():
    admission = pd.read_csv('data/admission_r.csv')
    antibiotics = pd.read_csv('data/antibiotics_r.csv')
    cultures = pd.read_csv('data/cultures_r.csv').drop('Unnamed: 12', axis=1, errors='ignore')

    names = list(admission.columns) + list(antibiotics.columns) + list(cultures.columns)
    names = [name for name in names if robust_detect(name) == 'he']
    translated = [
        'diagnosis_type',
        'status_at_reception',
        'status_before_hospitalization',
        'arrived_from',
        'referred_by',
        'sample_taken_from',
        'autolab',
        'test_date',
        'sticker_number',
        'date_and_test_auth_time',
        'age_',
        'current_age',
        'gender_',
        'dob',
        'bacteria',
        'bacteria_original_result',
        'antibiotic',
        'antibiotic_original_result',
        'antibiotic_sensitivity']
    names = dict(zip(names,translated))

    cultures = cultures.rename(names, axis=1)
    cultures.columns = map(str.lower, cultures.columns)
    admission = admission.rename(names, axis=1)
    admission.columns = map(str.lower, admission.columns)
    antibiotics = antibiotics.rename(names, axis=1)
    antibiotics.columns = map(str.lower, antibiotics.columns)

    cultures.to_csv('data/cultures.csv', index=False)
    admission.to_csv('data/admission.csv', index=False)
    antibiotics.to_csv('data/antibiotics.csv', index=False)

    return names


def translation_dict(filename='dictionary.pickle'):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            dic = pickle.load(f)
        dic = {k:v for k,v in dic.items() if robust_detect(k) == 'he'}
    else:
        dic = dict()
    return dic


def parse_dataframe(df):
    filename = 'dictionary.pickle'
    dic = translation_dict(filename)
    
    words = set()
    for col in cols_translate:
        if not col in df.columns:
            continue
        words = words.union(df[col].unique())

    words = list(words.difference(dic.keys()))
    words = [word for word in words if robust_detect(word) == 'he']
    words = [word.replace('[','').replace(']','') for word in words if not pd.isnull(word)]
    print('Words we ask Google to translate', words)
    new_dict = dict(zip(words, [tr.text for tr in trans.translate(words)]))
    dic.update(new_dict)
    with open(filename, 'wb') as f:
        pickle.dump(dic, f)

    return df.replace(dic)

def parse_data():
    translate_col_names()
    
    cultures = parse_dataframe(pd.read_csv('data/cultures.csv'))
    admission = parse_dataframe(pd.read_csv('data/admission.csv'))
    antibiotics = parse_dataframe(pd.read_csv('data/antibiotics.csv'))

    cultures.to_csv('data/cultures.csv', index=False)
    admission.to_csv('data/admission.csv', index=False)
    antibiotics.to_csv('data/antibiotics.csv', index=False)


def load_data():
    cultures = pd.read_csv('data/cultures.csv')
    admission = pd.read_csv('data/admission.csv')
    antibiotics = pd.read_csv('data/antibiotics.csv')

    return cultures, admission, antibiotics


if __name__ == '__main__':
    try:
        parse_data()
        load_data()
    except KeyboardInterrupt:
        pass
    except:
        import pdb, sys, traceback
        _, _, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
