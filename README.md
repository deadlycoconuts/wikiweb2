# Wikipedia Graph Mapper
<img src="https://user-images.githubusercontent.com/36802364/59440666-9fdcd880-8df7-11e9-8e5d-a266b1c12218.png" height="70%" width=70%>

This is a web application designed to visualise the links between different Wikipedia pages. Try it out at: http://www.wikiweb.appspot.com

### Background
This project is initiated in 2019 at CentraleSupélec, and has been undertaken by Zi Yi EWE and supervised by Professor Christian CHABRERIE. It has been carried out to fulfil the *Projet Innovation* (Innovation Project) course requirement in Semester 8 of the second year of the Ecole Centrale Engineering programme.

## Table of Contents

- [How to use](#how-to-use)
- [Features](#features)
- [Installation](#installation)
- [Full Documentation](#full-documentation)

## How to use
<img src="https://user-images.githubusercontent.com/36802364/59440802-d155a400-8df7-11e9-8763-4efccc1faba6.png" height="70%" width=70%>

1. Begin by entering the URL of your desired source Wikipedia page into the the first field. 
2. Enter the maximum search depth level desired*.
3. Select a search mode.
    There are 3 search modes available:
    - Search for links from the 1st paragraph  
        Uses links found within the 1st paragraph (of the introduction) of each Wikipedia page to generate a graph.
    - Search for links from the introduction      
        Uses links found within the introduction (may contain multiple paragraphs) of each Wikipedia page to generate a graph.
    - Search for links from the entire page   
        Uses links found within the entire page to generate a graph.
4. Click on 'Create my graph!'.
5. Voilà!

 *Unforunately, the maximum search level that works on the server which hosts this application is 2. Nonetheless, you should be able to run the programme to your heart's content at **any** search depth on a development server.

## Features
<img src="https://user-images.githubusercontent.com/36802364/59440838-df0b2980-8df7-11e9-9d4b-0a16b7741368.png" height="30%" width=30%> <img src="https://user-images.githubusercontent.com/36802364/59440841-e0d4ed00-8df7-11e9-8c13-9194ce8e3bdb.png" height="30%" width=30%>

- Scrapes URLs found within the first paragraph/introduction/entire document of a Wikipedia page, and repeats the process for each subsequent link found
- Offers customisation of the search depth and breadth level of the scraping
    - Breadth: Select the relevant section of each Wikipedia page to look for URLs
    - Depth: Enter the maximum search depth of the graph from the source node
- Displays the interconnections between these URLs found in an interactive graph
    - Click on a node to display only its neighbours
    - Click on the same node again to revert back to the original display
    - Drag the nodes around to rearrange and interact with them
- Supported by mobile browsers on touch devices with smaller screen resolutions
    - Resizing of webpages
    - Modification of the graph to pack nodes closer to one another to fit narrower screen dimensions

## Installation

To run the application locally, follow the steps below:
1. Clone the repository on your local device.  
    ```git clone https://github.com/DeadlyCoconuts/wikiweb2/```
    
2. Create a local environment to install the dependencies defined in requirements.txt  
    If you do not already have virtualenv installed:  
    ```pip install virtualenv```  
    ```pip install virtualenvwrapper-win```
    
    To create a virtual environment, go to the project directory and enter:  
    ```virtualenv [name of your virtual environment]```   
    
    To activate your virtual environment:  
    ```source [name of your virtual environment]/bin/activate``` 
    
    To install all dependencies indicated in requirements.txt:  
    ```pip install -r requirements.txt```     
    
3. Ensure that line 99 of your local copy of process_link.py has been commented out.  
    ```#requests_toolbelt.adapters.appengine.monkeypatch()```  
    
4. Run your local copy of main.py.  
    ```python main.py```
    
5. Visit your local application on your browser at http://127.0.0.1:5000.

## Full Documentation

Refer to the wiki of this repository at https://github.com/DeadlyCoconuts/wikiweb2/wiki for more details.
