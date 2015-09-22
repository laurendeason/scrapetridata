# -*- coding: utf-8 -*-
#import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from ediblepickle import checkpoint
import string
import metadata as md
#from selenium.webdriver.support import expected_conditions as EC
import time

resultsdir = "./results/"

#need to add in condition based on lastpagescountdown plus alternative conditions indicating we are on last page of results for given race
#condition to indicate we are on last page of results for given year-race
#	if lastpagescountdown <= 0 or (tempdf['Place'][0] == 1 and page != 1):
#	   break

def df_pickler(df,f):
    df.to_csv(f)    
    
def df_unpickler(f):
    return pd.read_csv(f)  

@checkpoint(key = string.Template('{0}_{1}.csv'), work_dir = resultsdir, pickler=df_pickler, unpickler=df_unpickler, refresh = False)
def getresultsfromurl(triname, year, url, tableattributes, columnlist, currpagecss, maxpages = 100):
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
        
        startcountdown = 0 
        lastpagescountdown = 2
        
        for page in range(1,maxpages):
            if startcountdown == 1:
                lastpagescountdown -= 1
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
            try:
                wait.until(lambda driver: driver.find_element_by_css_selector(currpagecss).text == unicode(page))
            except TimeoutException:
                print("WARNING: Current page, %r, doesn't match counted page, %r, allowing %r more pages to be read. " % (driver.find_element_by_css_selector(currpagecss).text,page, lastpagescountdown+1))
                startcountdown = 1
            
            soup = BeautifulSoup(driver.page_source, "lxml") #, "html5lib"
            tridatalist = []
            i=0
            for row in soup('table', tableattributes)[0].tbody('tr'):
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
                  
@checkpoint(key = string.Template('{0}_allyears.csv'), work_dir = resultsdir, pickler=df_pickler, unpickler=df_unpickler, refresh = True)
def getresults(triathlon):
    #this accepts a triathlon object,
    #returns a dataframe storing the results data.

    yearcount = 0

    for year in triathlon.yearlist:  # 2004, 2005, 2008, 2009, 2010, 2011, 2012, 2013, 2014 
        print("YEAR is %d " % year)
        tempdf = getresultsfromurl(triathlon.racecode, year, triathlon.urldict[year], triathlon.tableattributes, triathlon.colnamedict[year], triathlon.currpagecss)
        tempdf['Year'] = year
        if yearcount == 0:
            df = tempdf
        else:
            df = pd.concat((df, tempdf), axis=0, ignore_index=True)
            
        yearcount += 1
        
   
    return df   

    
chicacgodf = getresults(md.CH)

#chicacgodf.to_csv(resultsdir + "chicacgo.csv")

