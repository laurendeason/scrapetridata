
# coding: utf-8

# In[52]:

from bs4 import BeautifulSoup
from selenium import webdriver
import triclass as tri
import time

def geturldict(url, startyear = 1980, endyear = 2020):
    #navigates to given url and searches html for links containing text 'result' and year between startyear and endyear
    driver = webdriver.PhantomJS(port=65000)
    driver.set_window_size(1120, 550)
    #first try finding links on main site, if this returns nothing, try navigating to overall results page
    urldict  = {}
    driver.get(url) 
    soup = BeautifulSoup(driver.page_source, "lxml")
    linklist = [link for link in soup.find_all('a') if link.string is not None] #retuns list of links that have text
    for year in range(startyear,endyear+1):
        i=0
        for link in linklist:
            if "result" in link.string.lower() and str(year) in link.string and i == 0: #for now just grab first link containing this text
                urldict[year] = link.get('href') 
                i += 1
    driver.quit()
    return urldict

def getonlineraceresults(url, city, state, triname, race_id=None):
    #Takes in either url of results site or possibly the race_id from which the url will be contructed.  Returns
    #a race object including attributes that are fed in to the function as above, as well as columns, tableattributes,
    #currpagecss, and nameformat
    if url is None:
        url = 'http://onlineraceresults.com/race/view_race.php?race_id='+str(race_id)
    driver = webdriver.PhantomJS(port=65000)
    driver.set_window_size(1120, 550)
    driver.get(url)
    #In onlineraceresults, we must navigate to type of race (i.e. individual, and then select show all) The types of races
    #should be a list under the Header "Events", will try to just iterate through these, keep track of race type
    #from link text; to start just get Individual results and return single tri.  In future, return instead a list of
    #races (for individual, relay, etc)
    driver.find_element_by_link_text("Individual").click()
    driver.find_element_by_link_text("show all results").click() #this doesnt exist for all sites, might need to choose from available 
                                                                 #li items under ul class="quicklinks"
    driver.find_element_by_link_text("all").click()  #under number of records per page
    
    
    race = tri.Race(alphacode+str(year), city, state, triname, year, 
                  columns = ,  
                  tableattributes = {},
                  currpagecss = ,               
                  nameformat = )
    driver.quit()
    return race
    
def getmetadata(baseurl, city, state, triname, baseresulturl=None):
    #takes in url of race, returns list of race objects (from triclass) with filled in attributes
    urldict = geturldict(baseurl)
    if len(urldict)==0:
        urldict = geturldict(baseresulturl) #come back to this later, for now assume urldict was found from baseurl
    trilist = []
    driver = webdriver.PhantomJS(port=65000)
    driver.set_window_size(1120, 550)
    for year in urldict.keys():
        resultformat = 'unknown'
        driver.get(urldict[year])
        #check if this sends us to oen of the known race result sites, such as onlineraceresults
        soup = BeautifulSoup(driver.page_source, "lxml")
        linklist = [link for link in soup.find_all('a') if link.string is not None] #retuns list of links that have text
        for link in linklist:
            if "onlineraceresults" in link.string.lower(): 
                resultformat = 'onlineraceresults' #note, in future, to expand to other types of races, can just
                                                   #iterate through all race_id numbers in url of onlineraceresults
                tri_attributes = getonlineraceresults(urldict[year])
        if resultformat == 'onlineraceresults':
            
            
            
        alphacode = city[:2].upper() #For now assume this will yield unique codes, later have if-else clause here to check
                                     #if it has already been used, if so, iterate to something else
        CH.append(tri.Race(alphacode+str(year), city, state, triname, year, 
                  resulturl = urldict[year], 
                  columns = ,  
                  tableattributes = {},
                  currpagecss = ,               
                  baseurl=baseurl,
                  baseresulturl=baseresulturl,
                  nameformat = ))
    driver.quit()
    return trilist
        


# In[57]:

dcurldict = geturldict("http://nationstri.com/", startyear = 2008, endyear = 2015)

print(len(dcurldict))


# In[74]:

driver = webdriver.PhantomJS(port=65000)
driver.set_window_size(1120, 550)
driver.get(dcurldict[2008])
#In onlineraceresults, we must navigate to type of race (i.e. individual, and then select show all) The types of races
#should be a list under the Header "Events", will try to just iterate through these, keep track of race type
#from link text; to start just get Individual results and return single tri.  In future, return instead a list of
#races (for individual, relay, etc)
time.sleep(5)
driver.find_element_by_link_text("Individual").click()
time.sleep(5)
driver.find_element_by_link_text("show all results").click() #this doesnt exist for all sites, might need to choose from available 
                                                                 #li items under ul class="quicklinks"
time.sleep(5)
driver.find_element_by_link_text("all").click()  #under number of records per page
soup = BeautifulSoup(driver.page_source, "lxml")

driver.quit()
tables = soup.find_all('table')
print(tables)

#next -- figure out identifying attribute of the results table (is class = "results" used for all onlineresults pages?)
#then start trying to match column headers to list of column headers I am using


# In[73]:

driver.quit()

