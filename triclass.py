# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 16:41:23 2015

@author: lauren
"""
#not clear that making this a subclass is at all useful since i will be assigning code, etc for each event.  is there a way to declare the instance of the subclass taking on default
#values from a particular instance of the class?  for now (10/12), getting rid of sublass idea; each race will be declared as an instance of the Race class, for now with racecode
#indicating city and year, but to be amended in future to also indicate type of race (triathlon) and distance (i.e. CH_TRI_OLY_2008)

#NEXT - decide about above, then continue editing below and update trisraper and metadata accordingly, then start getting older DC years

#need to add in some attributes (possibly year specific) for the following:
    #format of times

class Race():  
    #racecode indicates city and year (i.e. CH_2008), but to be amended in future to also indicate type of race (triathlon) and distance (i.e. CH_TRI_OLYIND_2008)
    #city is the full city name where the race takes place
    #state is the full name of the state in which the race takes place (for US races, otherwise this gives country)
    #fullname gives the full official name of the race
    #year is the year in which the race takes place (may replace this with date in future, can get year from this)
    #resultsurl is the year-race specific url where results for the given race are located
    #columns is list of column names for results in table of given year
    #tableattributes is a dictionary giving the value of given table attributes for the table of interest -- ultimately this should be optonal where code finds first table avail with certain characteristics(?)
    #currpagecss is a string for the css selector of the object that will contain in its text the unicode u`pagenum', this will be searched for and used to check that the page has updated before scraping    
    #nextpglink is a dictionary mapping keys text, css, class to the value of at least one of these.  Each will default to "missing"    
    #nameformat is a string showing how the name field is formatted.  defaults to separarated, meaning that Firstname and Lastname are already included as two separate columns
    #baseurl (optional) gives the main website of the race (independent of year)
    #baseresulturl (optional) gives the main results website for the race (independent of year)
    def __init__(self, racecode, city, state, fullname, year, resulturl=None, columns=None, tableattributes=None, currpagecss=None, nextpglink=None, nameformat=None,
        baseurl=None, baseresulturl=None ):
        #is it better to define url and colnames lists as dictionaries, or just lists that line up based on year? or maybe a full on dataframe? as of
        #10/9, changing format so that each instance is one city-race rather than the full set of races, so any lists or dictionaries will be defined at higher level
        # to have default values that are mutable objects, must be done as below.  might want to leave some defaults as None rather than putting in these misisng default values though
        
        self.racecode = racecode
        self.city = city
        self.state = state
        self.fullname = fullname
        self.year = year
        self.resulturl = resulturl
        self.columns = columns
        if tableattributes is None:
            tableattributes={}
        self.tableattributes = tableattributes
        self.currpagecss = currpagecss
        if nextpglink is None:
            nextpglink = {"text": "missing", "css": "missing", "class": "missing"}
        self.nextpglink = nextpglink
        if nameformat is None:
            nameformat = "separated"
        self.nameformat = nameformat
        self.baseurl = baseurl
        self.baseresulturl = baseresulturl
        
    def addnextpglink(self,key,val):
        self.nextpglink[key]=val


        
