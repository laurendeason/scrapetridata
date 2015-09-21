# -*- coding: utf-8 -*-
#import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from selenium import webdriver
import selenium.webdriver.support.ui as ui
#from ediblepickle import checkpoint
#from selenium.webdriver.support import expected_conditions as EC
import time

resultsdir = "../results/"

def getresultsfromurl(year, url, columnlist, maxpages = 100):
        #This function scrapes the results for the given year which are located at given url, returns as a dataframe
        #url = string containing url with results
        # columnlist = list of column headers in order that they appear on results page
        #maxpages is max number of pages to loop through in case break condition fails

        driver = webdriver.PhantomJS()
        driver.set_window_size(1120, 550)

        #this defines a maximium wait time of n seconds to load page after clicking next and checking condition - 10 worked before, now times out
        wait = ui.WebDriverWait(driver,60)
        #adds in an implicit wait time of 5 seconds in case where element isnt readily accesible (Default is 0) to try to avoid StaleElementReferenceException
        #doesnt seem to work since element will still be there even if stale
        #driver.implicitly_wait(5)
        
        for page in range(1,maxpages):
            print("Page is %d" % page)
            if page == 1:
                driver.get(url)
            else:
                #alternative ways to search listed below
                driver.find_element_by_css_selector('a.next_page').click()
                #driver.find_element_by_class_name('next_page').click()
                #driver.find_element_by_link_text('Next →').click()
            
            #first wait makes sure page has loaded such that i dont get StaleElementReferenceException looking for em.current
            #need to figure out to make this work! see here for js solution: http://darrellgrainger.blogspot.it/2012/06/staleelementexception.html
            #wait.until(not EC.staleness_of(driver.find_element_by_css_selector('em.current')))
            time.sleep(5)
            
            #below if condition will always return true since EC doesnt return boolean
            #if EC.staleness_of(driver.find_element_by_css_selector('em.current')):
            #    print "Stale!  waiting!"
            #    print EC.staleness_of(driver.find_element_by_css_selector('em.current'))
            #    time.sleep(5)
            #checks that new page has loaded by checking if highlighted page number is equal to page number in for loop
            wait.until(lambda driver: driver.find_element_by_css_selector('em.current').text == unicode(page))
            print("em.current text is %r " % driver.find_element_by_css_selector('em.current').text)
            
            soup = BeautifulSoup(driver.page_source, "lxml") #, "html5lib"
            
            tridatalist = []
            i=0
            for row in soup('table', {'class': 'participant-list'})[0].tbody('tr'):
                tridatalist.append([])
                tds = row('td')
                for j in range(len(tds)):
                    if (tds[j].string) is None:
                        tridatalist[i].append(None)
                    elif (tds[j].string).strip() == '':
                        tridatalist[i].append(None)
                    elif columnlist[j] in ['Place', 'Bib','Age','DIVplace', 'SEXplace', 'SWIMRANK', 'BIKERANK', 'RUNRANK', 'PENALTY']:
                        tridatalist[i].append(int(tds[j].string))
                    elif columnlist[j] == 'MPH':
                        tridatalist[i].append(float(tds[j].string)) 
                    elif columnlist[j] in ['swim', 'bike', 'run','FinishTime', 'T1', 'T2']:
                        if tds[j].string.strip() == '0' or tds[j].string.strip()[2] != ":" or tds[j].string.strip()[5] != ":":
                            tridatalist[i].append(None)
                        else:
                            t = datetime.datetime.strptime((tds[j].string).strip(), "%H:%M:%S")
                            tridatalist[i].append(datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second))
                    else:
                        tridatalist[i].append(unicode(tds[j].string))
                        
                i += 1
    			
    	
            tempdf = pd.DataFrame(tridatalist, columns = columnlist)
            tempdf['FinishTimeinHours'] = pd.TimedeltaIndex(tempdf['FinishTime']).days*24 + pd.TimedeltaIndex(tempdf['FinishTime']).seconds.astype(float)/3600 + pd.TimedeltaIndex(tempdf['FinishTime']).microseconds.astype(float)/3600000000
            tempdf['swiminHours'] = pd.TimedeltaIndex(tempdf['swim']).days*24 + pd.TimedeltaIndex(tempdf['swim']).seconds.astype(float)/3600 + pd.TimedeltaIndex(tempdf['swim']).microseconds.astype(float)/3600000000
            tempdf['bikeinHours'] = pd.TimedeltaIndex(tempdf['bike']).days*24 + pd.TimedeltaIndex(tempdf['bike']).seconds.astype(float)/3600 + pd.TimedeltaIndex(tempdf['bike']).microseconds.astype(float)/3600000000
            tempdf['runinHours'] = pd.TimedeltaIndex(tempdf['run']).days*24 + pd.TimedeltaIndex(tempdf['run']).seconds.astype(float)/3600 + pd.TimedeltaIndex(tempdf['run']).microseconds.astype(float)/3600000000
            
            #print tempdf
            
            if page == 1:
                df = tempdf
            else:
                df = pd.concat((df, tempdf), axis=0, ignore_index=True)
                
            #condition to indicate we are on last page of results for given year-race
            if len(driver.find_elements_by_css_selector('span.next_page.disabled')) > 0:
                break
            
            #quit should close all phantomjs windows (could use close() to just close the one tab)				
        driver.quit()	 
        return df
                  

def getresults_urllist(triname, urldict, coldict):
    #this accepts a triname,
    #urldict = dictionary of urls for result data in each year where key values are years 
    #coldict = dictionary of columnname lists in each year where key values are years 

    #returns a dataframe storing the results data.

    yearcount = 0

    for year in (urldict.keys()):  # 2004, 2005, 2008, 2009, 2010, 2011, 2012, 2013, 2014 
        print("YEAR is %d " % year)
        tempdf = getresultsfromurl(year, urldict[year], coldict[year])
        tempdf['Year'] = year
        if yearcount == 0:
            df = tempdf
        else:
            df = pd.concat((df, tempdf), axis=0, ignore_index=True)
            
        yearcount += 1
        
   
    return df
    
    

    
chicagourl = { 2014: "http://results.active.com/events/transamerica-chicago-triathlon/international/expanded?",
               2013: "http://results.active.com/events/life-time-chicago-triathlon-results--2/international/expanded?",
               2012: "http://results.active.com/events/2012-chicago-triathlon-fleet-feet-super-sprint-and-chicago-kids-triathlon/international-individual/expanded?",
               2011: "http://results.active.com/events/life-time-chicago-triathlon-results/international-individual/expanded?",
               2010: "http://results.active.com/events/chicago-triathlon-results--2/international-individual/expanded?",
               2009: "http://results.active.com/events/chicago-triathlon-results--3/international-individual/expanded?",
               2008: "http://results.active.com/events/accenture-chicago-triathlon-mcdonald-s-kids-triathlon-and-fleet-feet-supersprint-triathlon/international-individual--3/expanded?",
               2005: "http://results.active.com/events/chicago-triathlon-results/international-individual/expanded?",
               2004: "http://results.active.com/events/chicago-triathlon-resuls/international-individual/expanded?"
               }
               
chicagocolumns = { 2014 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'DIVISION', 'swim', 'bike', 'run', 'DIVplace', 'SEXplace', 'SWIMRANK', 'BIKERANK', 'MPH', 'RUNRANK', 'PENALTY', 'FinishTime', 'T1', 'T2'],
                   2013 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'DIVISION', 'swim', 'bike', 'run', 'DIVplace', 'SEXplace', 'SWIMRANK', 'BIKERANK', 'MPH', 'RUNRANK', 'FinishTime', 'T1', 'T2'],
                   2012 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                   2011 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                   2010 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                   2009 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                   2008 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                   2005 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],
                   2004 : ['Place', 'Bib', 'Name', 'City', 'State', 'Age', 'Gender', 'swim', 'bike', 'run', 'FinishTime'],                   
                   }
    
chicacgodf = getresults_urllist('chicago',chicagourl, chicagocolumns)

chicacgodf.to_csv(resultsdir + "chicacgo.csv")

