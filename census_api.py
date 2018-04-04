#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 09:57:50 2018

@author: elenabg
"""
import json
import requests
import urllib3
from urllib.parse import urlparse
from census import Census
from us import states
from ast import literal_eval

census_var_lst = {'Total Population':'B01003_001E','Income in the past 12 months below poverty level:':'B17005_002E',\
                  'Bachelor degree or higher':'B23006_023E', 'Number of whites':'B02001_002E'}
key ='1c775b832899a80d4481940aff6a6c27ccaa9623'
c = Census(key)

def process_coord(loc):
    loc = literal_eval(loc)
    lat = str(loc[0])
    long = str(loc[1])
    url = 'https://www.broadbandmap.gov/broadbandmap/census/tract?latitude='+lat+'&longitude='+long+'&format=json'
    resp = requests.get(url)
    d_resp = json.loads(resp.text)
    d = d_resp["Results"]["censusTract"][0]
    state= d["stateFips"]
    fips= d["fips"]
    name = d["name"]
    return fips, name, stateFips

def get_educ(loc):
    cnt = 0
    fips, name, state = process_coord(loc)
    county = fips[2:5]
    tract = fips[5:]
    res = c.acs5.state_county_tract('B01003_001E,B23006_023E', state, county, tract, year=2015)
    tot = res[0]['B01003_001E']
    if tot == 0:
        return 'NaN'
    else:
        coll = res[0]['B23006_023E']
        cnt +=1
        print(str(cnt))
        return coll / tot
        

def get_pov(loc):
    fips, name, state = process_coord(loc)
    county = fips[2:5]
    tract = fips[5:]
    res = c.acs5.state_county_tract('B01003_001E,B17005_002E', state, county, tract,  year=2015)
    tot = res[0]['B01003_001E']
    
    if tot == 0:
        return 'NaN'  
    else:
        pov = res[0]['B17005_002E']
        return pov / tot
    

def get_whites(loc):
    fips, name, state = process_coord(loc)
    county = fips[2:5]
    tract = fips[5:]
    res = c.acs5.state_county_tract('B01003_001E,B02001_002E', state, county, tract,  year=2015)
    tot = res[0]['B01003_001E']
    
    if tot == 0:
        return 'NaN'
    else:
        whites = res[0]['B02001_002E']
        return whites / tot
        
