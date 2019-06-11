# Wikipedia Graph Mapper

<img src="https://raw.githubusercontent.com/DeadlyCoconuts/wikiweb2/master/preview.png" height="70%" width=70%>

This is a web application designed to visualise the links between different Wikipedia pages. Try it out at: http://www.wikiweb.appspot.com

## How to use
<img src="https://raw.githubusercontent.com/DeadlyCoconuts/wikiweb2/d8a9d46695e0898d946486ee12eaea6042242999/preview2.png">

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

## Support
<img src="https://raw.githubusercontent.com/DeadlyCoconuts/wikiweb2/master/mobilepreview1.png" height="30%" width=30%> <img src="https://raw.githubusercontent.com/DeadlyCoconuts/wikiweb2/master/mobilepreview2.png" height="30%" width=30%>

The application is also supported on mobile browsers on touch devices. In addition, the graph is modified to pack the nodes closer to one another in order to fit within the narrower screen dimensions.

## How to run the application locally
1. Clone the repository on your local device.

    `git clone https://github.com/DeadlyCoconuts/wikiweb2/`

2. Create a local environment to install the dependencies defined in requirements.txt
    
    If you do not already have virtualenv installed:
    
    `pip install virtualenv`
    
    `pip install virtualenvwrapper-win`
    
    To create a virtual environment, go to the project directory and enter:
    
    `virtualenv [name of your virtual environment]`
    
    To activate your virtual environment:
    
    `source [name of your virtual environment]/bin/activate`
    
    To install all dependencies indicated in requirements.txt:
    
    `pip install -r requirements.txt`
    
3. Ensure that line 105 of your local copy of process_link.py has been commented out.

    `#requests_toolbelt.adapters.appengine.monkeypatch()`
    
4. Run your local copy of main.py.

    `python main.py`
    
5. Visit your local application on your browser at http://127.0.0.1:5000.

