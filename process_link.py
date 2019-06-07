import requests
import requests_toolbelt.adapters.appengine
from bs4 import BeautifulSoup


HOME_URL = "https://en.wikipedia.org"
MAX_LEVEL = 1 # max crawl depth

#START_URL = "https://en.wikipedia.org/wiki/Unus_pro_omnibus,_omnes_pro_uno"

entryList = []

def scrape(self_url, currentLevel):
    if currentLevel + 1 > MAX_LEVEL: # stops sending requests if spider is going to reach max crawl level
        return

    currentLevel += 1
    
    #print("Currently scraping " + self_url)
    page = requests.get(self_url)
    # TODO throw exception here
    soup = BeautifulSoup(page.content, 'lxml')

    self_title = soup.title.contents[0] # stores title of page

    listTags = [] # list to store all hyperlinks found

    # Use this to search only the FIRST paragraph of each page for hyperlinks
    tag = soup.find('p') # search for first paragraph
    #print(tag.get('class') != None)
    #print(tag.find('a'))
    while (tag.find('a') != None and 'Coordinates' in tag.find('a').contents) or (tag.get('class') != None): # if first search result is not a pure <p> tag nor a coordinate link
        tag = tag.findNext('p')
    """
    while (tag.find('a') != None and 'Coordinates' in tag.find('a').contents): # if first search result is not a pure <p> tag
        print("search next")
        while (tag.get('class') != None):
            print("search next2")
            tag = tag.findNext('p')
        tag = tag.findNext('p')
    """
    #print('Coordinates' in tag.find('a').contents)
    listTags.extend(tag.findAll('a'))
    
    #print(listTags)
    # Use this to search the introduction of each page only for hyperlinks
    """
    stop_at = soup.find('h2') # finds the first h2 element i.e. where the first subsection header is found
    class_extr = stop_at.find_all_previous('p') # extracts all elements before this element
    for paragraph in class_extr:
        listTags.extend(paragraph.findAll('a'))
    """
    
    # Use this to search the entire page for hyperlinks
    """
    for paragraph in soup.findAll('p'): # for each paragraph found
        listTags.extend(paragraph.findAll('a')) # stores all hyperlinks found
    """

    # cleans up list of hyperlinks; retains only relevant links
    listLinks = [] # stores the name and url of each hyperlink found
    listOfFilterKeywords = ['cite_note', 'File', 'wikimedia', 'Help', ':Verifiability', 'Wikipedia:', 'wiktionary.org'] # stores list of keywords that indicates links to be filtered out
    for tag in listTags:
        if not any(keyword in str(tag) for keyword in listOfFilterKeywords): # checks if keyword is found; if so, skip this tag
            if 'title' in tag.attrs and 'href' in tag.attrs: # checks if title and link elements exist in the tag
                listLinks.append((tag['title'], HOME_URL + tag['href'])) # appends a title-url pair to listLinks
    """
    for tag in listTags:
        for keyword in listOfFilterKeywords:
            if keyword in str(tag): # checks if keyword is found; if so, skip this tag
                continue
            if 'title' in tag.attrs and 'href' in tag.attrs: # checks if title and link elements exist in the tag
                listLinks.append((tag['title'], HOME_URL + tag['href'])) # appends a title-url pair to listLinks
                break
    """
    
    for link in listLinks: # for each hyperlink found
        entry = {"self_title": self_title, "self_url": self_url, "ext_title": link[0], "ext_url": link[1], "current_level": currentLevel} # stores a dictionary of the information regarding each hyperlink i.e. which page it is found on
        if entry not in entryList: # filters out links already present
            entryList.append(entry)
        scrape(link[1], currentLevel) # depth-search via recursion
    return entryList

def proc_data(entryList, isMobileBrowser): 
    # creates a list to store all urls found
    urls = list(set([ data['self_url'] for data in entryList ])) # removes URL duplicates from self_urls
    urls.extend(list(set([ data['ext_url'] for data in entryList ]))) # adds other URLs branches to list
   
    nodeList = [] # to store nodes
    for url in urls:
        for data in entryList:
            if url == data["self_url"]:
                entry = {"id": url, "label": data["self_title"], "level": data["current_level"] - 1}
                if entry not in nodeList:
                    nodeList.append(entry)
                break
            elif url == data["ext_url"]:
                entry = {"id": url, "label": data["ext_title"], "level": data["current_level"]}
                if entry not in nodeList:
                    nodeList.append(entry)
                break
    
    linkList = [] # to store links
    for data in entryList:
        if isMobileBrowser:
            strength = 0.6
        else:
            #strength = (0.2*data["current_level"])
            # strength formula 
            strength = 0.8 - 0.4*data["current_level"]/MAX_LEVEL
        linkList.append({"target": data["self_url"], "source": data["ext_url"], "strength": strength})
    
    return nodeList, linkList


def full_clean_up(self_url, currentLevel, max_level, isMobileBrowser):
    #requests_toolbelt.adapters.appengine.monkeypatch() # patches requests as it has compatibility issues with Google App Engine/ comment this out to test on development server

    global MAX_LEVEL
    MAX_LEVEL = int(max_level)
    
    # clears list for each new request made
    del entryList[:]

    nodeList, linkList = proc_data(scrape(self_url, currentLevel), isMobileBrowser)
    return nodeList, linkList