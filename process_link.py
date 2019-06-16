import requests
import requests_toolbelt.adapters.appengine
from bs4 import BeautifulSoup


HOME_URL = "https://en.wikipedia.org"
MAX_LEVEL = 1 # max crawl depth
SEARCH_MODE = 1 # default search mode

entryList = []

def scrape(self_url, currentLevel):
    currentLevel += 1
    
    print("Currently scraping " + self_url)
    page = requests.get(self_url)
    # TODO throw exception here
    soup = BeautifulSoup(page.content, 'lxml')

    ### Gets page title
    self_title = soup.title.contents[0] # stores title of page
    
    ### Gets page image
    divTag = soup.find('div', {"class": "mw-parser-output"})
    if divTag != None:
        self_img = divTag.find('img')
    else:
        self_img = soup.find('img')
    if(self_img == None):
        self_img = None
    else:
        listOfIMGFilterKeywords = ["Edit-clear.svg", "book-new.svg", "Ambox_important.svg", "Ambox_current_red.svg", "red_question_mark.svg"]
        while any(keyword in str(self_img.get("src")) for keyword in listOfIMGFilterKeywords):
            self_img = self_img.findNext('img')
        self_img = "https:" + self_img.get('src')

    # Terminates scraping here if max search depth reached
    if currentLevel > MAX_LEVEL:
        entry = {"self_title": self_title, "self_url": self_url, "self_img": self_img, "ext_title": None, "ext_url": None, "current_level": currentLevel} # stores a dictionary of the information regarding each hyperlink i.e. which page it is found on
        if entry not in entryList: # filters out entries already present
            entryList.append(entry)
        return

    listTags = [] # list to store all hyperlinks found

    if SEARCH_MODE == 1: # OPTION 1: Use this to search only the FIRST paragraph of each page for hyperlinks
        tag = soup.find('p') # search for first paragraph
        table = tag.findParents('table')
        while table or 'class' in tag.attrs: # table is not empty; tag is found in a table
            tag = tag.findNext('p')
            table = tag.findParents('table')
        while (tag.find('a') != None and 'Coordinates' in tag.find('a').contents) or ((tag.get('class') != "mw-redirect") and (tag.get('class') != None)): # if first search result is not a pure <p> tag nor a coordinate link
            tag = tag.findNext('p')
        listTags.extend(tag.findAll('a'))
    elif SEARCH_MODE == 2: # OPTION 2: Use this to search the introduction of each page only for hyperlinks
        stop_at = soup.find('h2') # finds the first h2 element i.e. where the first subsection header is found
        class_extr = stop_at.find_all_previous('p') # extracts all elements before this element
        for paragraph in class_extr:
            listTags.extend(paragraph.findAll('a'))
    elif SEARCH_MODE == 3: # OPTION 3: Use this to search the entire page for hyperlinks
        for paragraph in soup.findAll('p'): # for each paragraph found
            listTags.extend(paragraph.findAll('a')) # stores all hyperlinks found

    # cleans up list of hyperlinks; retains only relevant links
    #listLinks = [] # stores the name and url of each hyperlink found
    listOfFilterKeywords = ['cite_note', 'File', 'wikimedia', 'Help', ':Verifiability', 'Wikipedia:', 'wiktionary.org'] # stores list of keywords that indicates links to be filtered out
    for tag in listTags:
        if not any(keyword in str(tag) for keyword in listOfFilterKeywords): # checks if keyword is found; if so, skip this tag
            if 'title' in tag.attrs and 'href' in tag.attrs: # checks if title and link elements exist in the tags
                #listLinks.append((tag['title'], HOME_URL + tag['href'])) # appends a title-url pair to listLinks
                entry = {"self_title": self_title, "self_url": self_url, "self_img": self_img, "ext_title": tag['title'], "ext_url": HOME_URL + tag['href'], "current_level": currentLevel} # stores a dictionary of the information regarding each hyperlink i.e. which page it is found on
                if entry not in entryList: # filters out entries already present
                    entryList.append(entry)
                scrape(entry["ext_url"], currentLevel) # depth-search via recursion
    return entryList

def proc_data(entryList, isMobileBrowser): 
    # creates a list to store unique urls found
    urls = list(set([ data['self_url'] for data in entryList ])) # removes URL duplicates from self_urls
    urls.extend(list(set([ data['ext_url'] for data in entryList ]))) # adds other URLs branches to list
    
    
    #print(entryList)
    nodeList = [] # to store nodes
    for url in urls:
        for data in entryList:
            if url == data["self_url"]:
                entry = {"id": url, "label": data["self_title"], "level": data["current_level"] - 1, "img": data["self_img"]}
                if entry not in nodeList:
                    nodeList.append(entry)
                break
            """
            elif url == data["ext_url"]: # search again from self_urls?
                entry = {"id": url, "label": data["ext_title"], "level": data["current_level"], "img": None} # fix
                if entry not in nodeList:
                    nodeList.append(entry)
                break
            """
    
    linkList = [] # to store links
    for data in entryList:
        if isMobileBrowser:
            strength = 0.6
        else:
            # strength formula 
            strength = 0.8 - 0.4*data["current_level"]/MAX_LEVEL
        if data["ext_url"] != None:
            linkList.append({"target": data["self_url"], "source": data["ext_url"], "strength": strength})
    
    return nodeList, linkList


def generate_lists(self_url, max_level, isMobileBrowser, search_mode):
    #requests_toolbelt.adapters.appengine.monkeypatch() # patches requests as it has compatibility issues with Google App Engine/ comment this out to test on development server

    # Changes HOME_URL 
    new_wikipedia_region = self_url.split("wikipedia.org", 1)[0]
    new_home_url = new_wikipedia_region + "wikipedia.org"
    global HOME_URL
    HOME_URL = new_home_url

    # Sets MAX_LEVEL
    global MAX_LEVEL
    MAX_LEVEL = int(max_level)
    
    # Sets SEARCH_MODE
    global SEARCH_MODE
    SEARCH_MODE = int(search_mode)

    # clears list for each new request made
    del entryList[:]

    nodeList, linkList = proc_data(scrape(self_url, currentLevel = 0), isMobileBrowser)
    return nodeList, linkList