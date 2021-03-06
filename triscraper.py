
# coding: utf-8

# In[51]:

from bs4 import BeautifulSoup
import pandas as pd
import datetime
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from ediblepickle import checkpoint
import string
import metadata as md
#from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, StaleElementReferenceException
import time

resultsdir = "./results/"

#define an output log file to store output from scraping
logfile = open('./logs/triscraper.log', 'a')  #a appends here.  to overwrite previous log file, change to w

#need to add in condition based on lastpagescountdown plus alternative conditions indicating we are on last page of results for given race
#condition to indicate we are on last page of results for given year-race
#	if lastpagescountdown <= 0 or (tempdf['Place'][0] == 1 and page != 1):
#	   break

def df_pickler(df,f):
    df.to_csv(f, encoding='utf-8')    
    
def df_unpickler(f):
    return pd.read_csv(f)  
    
    
def findnextpage(driver, nextpglink):
    #this takes in given driver and a dictionary mapping type of element to the element value that identifies the link to the next page
    #can't use dictionary here instead of repeated if then else; tried already but it tries to find values in driver even when they aren't part of dictionary for given city
    #print("In findnextpage!!")                 
    if nextpglink['css'] != 'missing':
        #print ("In if for css")
        return driver.find_element_by_css_selector(nextpglink['css'])
    elif nextpglink['class'] != 'missing':
        #print ("In if for class")
        return driver.find_element_by_class_name(nextpglink['class'])
    elif nextpglink['text'] != 'missing':
        #print ("In if for text")
        return driver.find_element_by_link_text(nextpglink['text'])
    #if all fields in nextpglink are missing, it is as though we attempt to find a link and get a noelem    print("findnextpage returning NoSuchElementException")suchentexception
    else:
        return NoSuchElementException
    

@checkpoint(key = string.Template('{1}.csv'), work_dir = resultsdir, pickler=df_pickler, unpickler=df_unpickler, refresh = False)
def getresults(triathlon, savename, maxpages = 100):
        #This function scrapes the results for the given year which are located at given url, returns as a dataframe
        #url = string containing url with results
        # columnlist = list of column headers in order that they appear on results page
        #maxpages is max number of pages to loop through in case break condition fails

        driver = webdriver.PhantomJS()
        driver.set_window_size(1120, 550)

        #this defines a maximium wait time of n seconds to load page after clicking next and checking condition - 10 worked before, now times out
        wait = ui.WebDriverWait(driver,100)
        #adds in an implicit wait time of 5 seconds in case where element isnt readily accesible (Default is 0) to try to avoid StaleElementReferenceException
        #doesnt seem to work since element will still be there even if stale
        #driver.implicitly_wait(5)
        
        startcountdown = 0 
        lastpagescountdown = 2
        
        for page in range(1,maxpages):
            if startcountdown == 1:
                lastpagescountdown -= 1
            logfile.write(("Page is %d" % page))
            print("Page is %d" % page)
            if page == 1:
                driver.get(triathlon.resulturl)
            else:
                try:
                    #wait.until(lambda driver: findnextpage(driver, nextpglink).click() not in [WebDriverException, StaleElementReferenceException])
                    findnextpage(driver, triathlon.nextpglink).click()
                    #this should be modified to go back and try other elements identifying nextpglink before resorting to exception below, maybe just an if statement in findnextpage above
                    #before first return , if nextpagmap[key].click() != NoSuchElementException
                except NoSuchElementException:
                    driver.find_element_by_link_text(str(page)).click();
            
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
                wait.until(lambda driver: driver.find_element_by_css_selector(triathlon.currpagecss).text == unicode(page))
            except TimeoutException:
                logfile.write("WARNING: Current page, %r, doesn't match counted page, %r, allowing %r more pages to be read. \n" % (driver.find_element_by_css_selector(triathlon.currpagecss).text,page, lastpagescountdown+1))
                startcountdown = 1
            
            soup = BeautifulSoup(driver.page_source, "lxml") #, "html5lib"
            tridatalist = []
            i=0
            rowgen = (row for row in soup('table', triathlon.tableattributes)[0].tbody('tr') if len(row('td')) >  0)
            for row in rowgen:
                tridatalist.append([])
                tds = row('td')
                for j in range(len(tds)):
                    if tds[j].stripped_strings is None:
                        tridatalist[i].append(None)
                    elif "".join(tds[j].stripped_strings) == '':
                        tridatalist[i].append(None)
                    elif triathlon.columns[j] in ['Place', 'Bib','Age','DIVplace', 'SEXplace', 'SWIMRANK', 'BIKERANK', 'RUNRANK', 'PENALTY']:
                        tridatalist[i].append(int("".join(tds[j].stripped_strings)))
                    elif triathlon.columns[j] == 'MPH':
                        tridatalist[i].append(float("".join(tds[j].stripped_strings))) 
                    elif triathlon.columns[j] in ['swim', 'bike', 'run','FinishTime', 'T1', 'T2']:
                        #for now just use explicit if statement for which city--should be able to merge conditions into one set of more universal
                        if triathlon.racecode.split('_')[0] == 'CH':
                            if "".join(tds[j].stripped_strings) == '0' or "".join(tds[j].stripped_strings)[2] != ":" or "".join(tds[j].stripped_strings)[5] != ":":
                                tridatalist[i].append(None)
                            else:
                                t = datetime.datetime.strptime("".join(tds[j].stripped_strings), "%H:%M:%S")
                                tridatalist[i].append(datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second))
                        elif triathlon.racecode.split('_')[0] == 'DC' or triname == 'NY':
                            if "".join(tds[j].stripped_strings).count(':') == 0:
                                tridatalist[i].append(None)
                            elif "".join(tds[j].stripped_strings).count(':') == 1:    
                                t = datetime.datetime.strptime("".join(tds[j].stripped_strings), "%M:%S")
                                tridatalist[i].append(datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second))
                            elif "".join(tds[j].stripped_strings).count(':') == 2:    
                                t = datetime.datetime.strptime("".join(tds[j].stripped_strings), "%H:%M:%S")
                                tridatalist[i].append(datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second))
                    else:
                        #tridatalist[i].append(unicode(tds[j].string))
                        tridatalist[i].append(unicode("".join(tds[j].stripped_strings))) 
                        
                i += 1
    			
    	
            tempdf = pd.DataFrame(tridatalist, columns = triathlon.columns)
            tempdf['FinishTimeinHours'] = pd.TimedeltaIndex(tempdf['FinishTime']).days*24 + pd.TimedeltaIndex(tempdf['FinishTime']).seconds.astype(float)/3600 + pd.TimedeltaIndex(tempdf['FinishTime']).microseconds.astype(float)/3600000000
            tempdf['bikeinHours'] = pd.TimedeltaIndex(tempdf['bike']).days*24 + pd.TimedeltaIndex(tempdf['bike']).seconds.astype(float)/3600 + pd.TimedeltaIndex(tempdf['bike']).microseconds.astype(float)/3600000000
            tempdf['runinHours'] = pd.TimedeltaIndex(tempdf['run']).days*24 + pd.TimedeltaIndex(tempdf['run']).seconds.astype(float)/3600 + pd.TimedeltaIndex(tempdf['run']).microseconds.astype(float)/3600000000
            
            if 'T1' in triathlon.columns:
                tempdf['T1inHours'] = pd.TimedeltaIndex(tempdf['T1']).days*24 + pd.TimedeltaIndex(tempdf['T1']).seconds.astype(float)/3600 + pd.TimedeltaIndex(tempdf['T1']).microseconds.astype(float)/3600000000
            if 'T2' in triathlon.columns:            
                tempdf['T2inHours'] = pd.TimedeltaIndex(tempdf['T2']).days*24 + pd.TimedeltaIndex(tempdf['T2']).seconds.astype(float)/3600 + pd.TimedeltaIndex(tempdf['T2']).microseconds.astype(float)/3600000000	

            
            #assume that if swim is misisng, it was cancelled (such as DC 2014)
            if 'swim' in triathlon.columns:
                tempdf['swiminHours'] = pd.TimedeltaIndex(tempdf['swim']).days*24 + pd.TimedeltaIndex(tempdf['swim']).seconds.astype(float)/3600 + pd.TimedeltaIndex(tempdf['swim']).microseconds.astype(float)/3600000000
            #else: 
            #    tempdf['swiminHours'] = tempdf['FinishTimeinHours']-tempdf['T1inHours']-tempdf['bikeinHours']-tempdf['T2inHours']-tempdf['runinHours']
            #    tempdf['swim'] = pd.to_timedelta(tempdf['swiminHours'],unit='h')
            
            if page == 1:
                df = tempdf
            else:
                df = pd.concat((df, tempdf), axis=0, ignore_index=True)
            
            logfile.write(tempdf.head().to_string())
                
            #condition to indicate we are on last page of results for given year-race -- currently this just adds together conditions from all 3 cities
            if len(driver.find_elements_by_css_selector('span.next_page.disabled')) > 0 or lastpagescountdown <= 0 or (tempdf['Place'][0] == 1 and page != 1):
                break
            
        #quit should close all phantomjs windows (could use close() to just close the one tab)				
        driver.quit()	
        df.drop_duplicates(inplace=True)
        return df
                  
@checkpoint(key = string.Template('{1}_allyears.csv'), work_dir = resultsdir, pickler=df_pickler, unpickler=df_unpickler, refresh = True)
def getresultsallyears(trilist, savename):
    #this accepts a triathlon object,2nd argument is simply the string under which you would like the results saved
    #returns a dataframe storing the results data.

    yearcount = 0

    for tri in trilist:  
        logfile.write("CITY: %r ; YEAR: %d \n" % (tri.city, tri.year) )
        print("CITY: %r ; YEAR: %d " % (tri.city, tri.year) )
        tempdf = getresults(tri.year, tri.racecode) #second argument sent separately so that it can be used in naming csv file produced by ediblepickle
        tempdf['Year'] = tri.year
        tempdf['racecode'] = tri.racecode
        tempdf['yearborn'] = (tempdf['Year']-tempdf['Age']).fillna(0.0).astype(int)  #assume bday has happened already in current year; later can match on yearborn or yearborn+1
        tempdf[tempdf['yearborn'] == tempdf['Year']]['yearborn'] = None
        if tri.nameformat == "Firstname Lastname":
            tempdf['firstname'] = tempdf['Name'].str.rsplit(' ',expand=True,n=1)[0].str.strip().str.upper()
            tempdf['lastname'] = tempdf['Name'].str.rsplit(' ',expand=True,n=1)[1].str.strip().str.upper()
        elif tri.nameformat == "Lastname, Firstname":
            tempdf['firstname'] = tempdf['Name'].str.split(',',expand=True,n=1)[1].str.strip().str.upper()
            tempdf['lastname'] = tempdf['Name'].str.split(',',expand=True,n=1)[0].str.strip().str.upper() 
        
        if yearcount == 0:
            df = tempdf
        else:
            df = pd.concat((df, tempdf), axis=0, ignore_index=True)
            
        yearcount += 1
        
    #print('Returning df now')
    return df   
    
@checkpoint(key = string.Template('allresults.csv'), work_dir = resultsdir, pickler=df_pickler, unpickler=df_unpickler, refresh = True)
def aggregateresults(trilistdict):  
    i = 0
    for tri in trilistdict.keys():  #.keys() here isnt needed
        if i == 0:
            allresults = getresultsallyears(trilistdict[tri], tri)
        else:
            allresults = pd.concat((allresults, getresultsallyears(trilistdict[tri], tri)), axis=0, ignore_index=True)  
        i+=1
    return allresults
   
#trilistdict is now a dictionary of lists (of races)  
allresults = aggregateresults(md.trilistdict)

logfile.close()
    

