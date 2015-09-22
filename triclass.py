# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 16:41:23 2015

@author: lauren
"""

#need to add in some attributes (possibly year specific) for the following:
    #tableattributes -- table classname
    #format of times
    #identifier for button to click through to next page
    #currpagecss -- condition to check if page has updated correctly
    #condition to indicate we are on last page of results for given year-race

class Triathlon:
    #Defines a racecode, city, state, and years in which it has triathlon results.  Optionally contains list of specific triathlons for that city and main url for that triathlon
    #racecode is a unique identifier for the given race, usually a 2 letter code for the city in which it takes place
    #baseurl is the url for the race overall (not the specific results pages)
    #urldict is a dictionary with years as keys and urls for given results
    #colnamedict is dictionary with years as keys and list of column names for results in table of given year
    #tableattributes is a dictionary (for now assumed contant across all years) giving the value of given table attributes for the table of interest -- ultimately this should be optonal where code finds first table avail with certain characteristics(?)
    #currpagecss is a string for the css selector of the object that will contain in its text the unicode u`pagenum', this will be searched for and used to check that the page has updated before scraping    
    def __init__(self, racecode, city, state, fullname, yearlist=[], urldict={}, colnamedict={}, baseurl = 'nourl', tableattributes={}, currpagecss=''):
        #is it better to define url and colnames lists as dictionaries, or just lists that line up based on year? or maybe a full on dataframe?
        self.racecode = racecode
        self.city = city
        self.state = state
        self.fullname = fullname
        self.yearlist = yearlist
        self.urldict = urldict
        self.colnamedict = colnamedict
        self.baseurl = baseurl
        self.tableattributes = tableattributes
        self.currpagecss = currpagecss
        
    def addurl(self,year,url):
        self.urldict[year] = url
        
    def addcolnamelist(self,year,colnamelist):
        self.colnamedict[year] = colnamelist

##want to create a derived class for race that is uniquely identified by its 2 digit code, and the year - eventually code can be changed to include sprint vs. olympic etc
#class TriRace(Triathlon):
#    def __init__(self, raceid, city, year, url = 'nourl', columns = []):
#        self.raceid = raceid
#        self.city = city
#        self.year = year
#        self.url = url
#        self.columns = columns
        
        
#is it better to have class and subclass, or just the one class with attributes that are dictionaries?  for now, just pick one, move on
        #with subclasses,first def would be  def __init__(self, racecode, city, fullname, yearlist=[], triraces = [], baseurl = 'nourl'): where
        #triraces is a list of TriRace objects

        
