# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 14:32:41 2015

@author: lauren
"""
#metadata.py

import triclass as tri

#future generalization - have dictionary defining unique code for each race, perhaps 2 digit alphanumeric, DC1, DC2, NY, CH, etc.  Eventually a df giving, for each race, set of divisions, race date, race lengths, etc.

#create empty dictionaries of urls and column names
#url = {}
#columns = {}
#
#url['chicago'] =  { 2014: "http://results.active.com/events/transamerica-chicago-triathlon/international/expanded?",
#                    2013: "http://results.active.com/events/life-time-chicago-triathlon-results--2/international/expanded?",
#                    2012: "http://results.active.com/events/2012-chicago-triathlon-fleet-feet-super-sprint-and-chicago-kids-triathlon/international-individual/expanded?",
#                    2011: "http://results.active.com/events/life-time-chicago-triathlon-results/international-individual/expanded?",
#                    2010: "http://results.active.com/events/chicago-triathlon-results--2/international-individual/expanded?",
#                    2009: "http://results.active.com/events/chicago-triathlon-results--3/international-individual/expanded?",
#                    2008: "http://results.active.com/events/accenture-chicago-triathlon-mcdonald-s-kids-triathlon-and-fleet-feet-supersprint-triathlon/international-individual--3/expanded?",
#                    2005: "http://results.active.com/events/chicago-triathlon-results/international-individual/expanded?",
#                    2004: "http://results.active.com/events/chicago-triathlon-resuls/international-individual/expanded?"
#                   }
#               
#columns['chicago'] =  { 2014 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'DIVISION', 'swim', 'bike', 'run', 'DIVplace', 'SEXplace', 'SWIMRANK', 'BIKERANK', 'MPH', 'RUNRANK', 'PENALTY', 'FinishTime', 'T1', 'T2'],
#                        2013 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'DIVISION', 'swim', 'bike', 'run', 'DIVplace', 'SEXplace', 'SWIMRANK', 'BIKERANK', 'MPH', 'RUNRANK', 'FinishTime', 'T1', 'T2'],
#                        2012 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
#                        2011 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
#                        2010 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
#                        2009 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
#                        2008 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
#                        2005 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
#                        2004 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],                   
#                       }
#
#columns['dc'] =      {  2014 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State', 'T1', 'bike', 'T2', 'run', 'FinishTime'],
#                        2013 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State', 'swim', 'T1', 'bike', 'T2', 'run', 'FinishTime'],
#                        2012 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State', 'swim', 'T1', 'bike', 'T2', 'run', 'FinishTime'],   
#                      }
#
#url['dc']= {}
#for year in columns['dc'].keys():                     
#    url['dc'][year] = "http://nationstri.com/results/" + str(year) + "-results/"  

CH = tri.Triathlon('CH', 'Chicago', 'IL', "Transamerica Chicago Triathlon", 
               yearlist = [2004,2005,2008,2009,2010,2011,2012,2013,2014],
               urldict = { 2014: "http://results.active.com/events/transamerica-chicago-triathlon/international/expanded?",
                           2013: "http://results.active.com/events/life-time-chicago-triathlon-results--2/international/expanded?",
                           2012: "http://results.active.com/events/2012-chicago-triathlon-fleet-feet-super-sprint-and-chicago-kids-triathlon/international-individual/expanded?",
                           2011: "http://results.active.com/events/life-time-chicago-triathlon-results/international-individual/expanded?",
                           2010: "http://results.active.com/events/chicago-triathlon-results--2/international-individual/expanded?",
                           2009: "http://results.active.com/events/chicago-triathlon-results--3/international-individual/expanded?",
                           2008: "http://results.active.com/events/accenture-chicago-triathlon-mcdonald-s-kids-triathlon-and-fleet-feet-supersprint-triathlon/international-individual--3/expanded?",
                           2005: "http://results.active.com/events/chicago-triathlon-results/international-individual/expanded?",
                           2004: "http://results.active.com/events/chicago-triathlon-resuls/international-individual/expanded?"
               },
               colnamedict = { 2014 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'DIVISION', 'swim', 'bike', 'run', 'DIVplace', 'SEXplace', 'SWIMRANK', 'BIKERANK', 'MPH', 'RUNRANK', 'PENALTY', 'FinishTime', 'T1', 'T2'],
                               2013 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'DIVISION', 'swim', 'bike', 'run', 'DIVplace', 'SEXplace', 'SWIMRANK', 'BIKERANK', 'MPH', 'RUNRANK', 'FinishTime', 'T1', 'T2'],
                               2012 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                               2011 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                               2010 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                               2009 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                               2008 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                               2005 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                               2004 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],                   
               },
               baseurl="http://www.chicagotriathlon.com/",
               tableattributes = {'class':'participant-list'},
               currpagecss = 'em.current' )


DC = tri.Triathlon('DC', 'Washington', 'DC', "The Nation's Triathlon", 
               yearlist = [2012,2013,2014,2015],
               colnamedict = {  2014 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State', 'T1', 'bike', 'T2', 'run', 'FinishTime'],
                        2013 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State', 'swim', 'T1', 'bike', 'T2', 'run', 'FinishTime'],
                        2012 : ['Place', 'DIVISION', 'DIVplace', 'Name', 'Age', 'City', 'State', 'swim', 'T1', 'bike', 'T2', 'run', 'FinishTime'],   
                      },
               baseurl="http://nationstri.com/",
               tableattributes = {'class':'data'},
               currpagecss = 'p.rpp b')

for year in DC.yearlist:               
    DC.addurl(year, "http://nationstri.com/results/" + str(year) + "-results/")



     
           