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
    #resultsurl is the url of a main results page which links to different years
    #urldict is a dictionary with years as keys and urls for given results
    #colnamedict is dictionary with years as keys and list of column names for results in table of given year
    #tableattributes is a dictionary (for now assumed constant across all years) giving the value of given table attributes for the table of interest -- ultimately this should be optonal where code finds first table avail with certain characteristics(?)
    #currpagecss is a string for the css selector of the object that will contain in its text the unicode u`pagenum', this will be searched for and used to check that the page has updated before scraping    
    #nextpglink is a dictionary mapping keys text, css, class to the value of at least one of these.  Each will default to "missing"    
    #nameformat is a string showing how the name field is formatted.  defaults to Firstname Lastname
    def __init__(self, racecode, city, state, fullname, yearlist=None, urldict=None, colnamedict=None, baseurl = None, resultsurl=None, tableattributes=None, currpagecss=None, 
                 nextpglink=None, nameformat=None):
        #is it better to define url and colnames lists as dictionaries, or just lists that line up based on year? or maybe a full on dataframe?
        # to have default values that are mutable objects, must be done as below.  might want to leave some defaults as None rather than putting in these misisng default values though
        self.racecode = racecode
        self.city = city
        self.state = state
        self.fullname = fullname
        if yearlist is None:
            yearlist=[]
        self.yearlist = yearlist
        if urldict is None:
            urldict={}
        self.urldict = urldict
        if colnamedict is None:
            colnamedict={}
        self.colnamedict = colnamedict
        self.baseurl = baseurl
        self.resultsurl = resultsurl
        if tableattributes is None:
            tableattributes={}
        self.tableattributes = tableattributes
        self.currpagecss = currpagecss
        if nextpglink is None:
            nextpglink = {"text": "missing", "css": "missing", "class": "missing"}
        self.nextpglink = nextpglink
        if nameformat is None:
            nameformat = "Firstname Lastname"
        self.nameformat = nameformat
        
    def addurl(self,year,url):
        self.urldict[year] = url
        
    def addcolnamelist(self,year,colnamelist):
        self.colnamedict[year] = colnamelist
        
    def addnextpglink(self,key,val):
        self.nextpglink[key]=val

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

        
