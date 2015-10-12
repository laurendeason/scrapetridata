# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 14:32:41 2015

@author: lauren
"""
#metadata.py
from selenium import webdriver
import triclass as tri

#future generalization - have dictionary defining unique code for each race, perhaps 2 digit alphanumeric, DC1, DC2, NY, CH, etc.  Eventually a df giving, for each race, set of divisions, race date, race lengths, etc.

CHyearlist = [2004,2005,2008,2009,2010,2011,2012,2013,2014]
CHurldict =  { 2014: "http://results.active.com/events/transamerica-chicago-triathlon/international/expanded?",
               2013: "http://results.active.com/events/life-time-chicago-triathlon-results--2/international/expanded?",
               2012: "http://results.active.com/events/2012-chicago-triathlon-fleet-feet-super-sprint-and-chicago-kids-triathlon/international-individual/expanded?",
               2011: "http://results.active.com/events/life-time-chicago-triathlon-results/international-individual/expanded?",
               2010: "http://results.active.com/events/chicago-triathlon-results--2/international-individual/expanded?",
               2009: "http://results.active.com/events/chicago-triathlon-results--3/international-individual/expanded?",
               2008: "http://results.active.com/events/accenture-chicago-triathlon-mcdonald-s-kids-triathlon-and-fleet-feet-supersprint-triathlon/international-individual--3/expanded?",
               2005: "http://results.active.com/events/chicago-triathlon-results/international-individual/expanded?",
               2004: "http://results.active.com/events/chicago-triathlon-resuls/international-individual/expanded?"
               }
CHcolnamedict = { 2014 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'DIVISION', 'swim', 'bike', 'run', 'DIVplace', 'SEXplace', 'SWIMRANK', 'BIKERANK', 'MPH', 'RUNRANK', 'PENALTY', 'FinishTime', 'T1', 'T2'],
                  2013 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'DIVISION', 'swim', 'bike', 'run', 'DIVplace', 'SEXplace', 'SWIMRANK', 'BIKERANK', 'MPH', 'RUNRANK', 'FinishTime', 'T1', 'T2'],
                  2012 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                  2011 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                  2010 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                  2009 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                  2008 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                  2005 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                  2004 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],                   
               }

#make CH now be a list tri races, one for each year
CH = []
for year in CHyearlist:
    CH.append(tri.Race('CH_'+str(year), 'Chicago', 'IL', "Transamerica Chicago Triathlon", year, 
               resulturl = CHurldict[year], 
               columns = CHcolnamedict[year],  
               tableattributes = {'class':'participant-list'},
               currpagecss = 'em.current',               
               baseurl="http://www.chicagotriathlon.com/",
               nameformat = 'Firstname Lastname'))
for race in CH:
    race.addnextpglink('css','a.next_page')  
    race.addnextpglink('class','next_page')  
    race.addnextpglink('text','Next →')
               
          

#DC metadata
DCyearlist = [2012,2013,2014,2015]
DCcolnamedict = {  2015 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State', 'swim', 'T1', 'bike', 'T2', 'run', 'FinishTime'],
                   2014 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State',         'T1', 'bike', 'T2', 'run', 'FinishTime'],
                   2013 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State', 'swim', 'T1', 'bike', 'T2', 'run', 'FinishTime'],
                   2012 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State', 'swim', 'T1', 'bike', 'T2', 'run', 'FinishTime'],   
                }
DC = []
for year in DCyearlist:
    DC.append(tri.Race('DC_'+str(year), 'Washington', 'DC', "The Nation's Triathlon", year, 
         resulturl = "http://nationstri.com/results/" + str(year) + "-results/", 
         columns = DCcolnamedict[year],
         tableattributes = {'class':'data'},
         currpagecss = 'p.rpp b',
         nameformat = "Lastname, Firstname",
         baseurl="http://nationstri.com/",
         baseresulturl = "http://nationstri.com/results/"))
for race in DC:
  race.addnextpglink('text','>>')   

#NY metadata
NYyearlist = [2012,2013,2014,2015]
NYcolnamedict = {  2015 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State', 'swim', 'T1', 'bike', 'T2', 'run', 'FinishTime'],
                   2014 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State', 'swim', 'T1', 'bike', 'T2', 'run', 'FinishTime'],
                   2013 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State', 'swim', 'T1', 'bike', 'T2', 'run', 'FinishTime'],
                   2012 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State', 'swim', 'T1', 'bike', 'T2', 'run', 'FinishTime'],  
                }



NY = []
for year in NYyearlist:
    NY.append(tri.Race('NY_'+str(year), 'New York', 'NY', "New York City Triathlon", year,
         baseurl="http://nyctri.com/",
         baseresulturl = 'http://www.nyctri.com/new-york/results/',
         tableattributes = {'class':'data'},
         currpagecss = 'p.rpp b',
         nameformat = "Lastname, Firstname"))


driver = webdriver.PhantomJS(port=65000)
driver.set_window_size(1120, 550)
driver.get(NY[0].baseresulturl)  
for race in NY:
    race.addnextpglink('text','>>') 
    race.resulturl = driver.find_element_by_link_text(str(race.year)+' Results').get_attribute('href')  

driver.quit()

trilistdict = {'CH' : CH,
               'DC' : DC,
               'NY' : NY } 




     
           