#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, request, url_for
from process_link import generate_lists

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index():
    return render_template("search.html", 
    options = ["Search for links from the 1st paragraph", "Search for links from the introduction", "Search for links from the entire page"]) # displays initial search bar

@app.route("/result", methods=['GET', 'POST'])
def result():
    #data = []
    #error = None # to implement in the future
    source_url = request.form.get('search_body') # gets search URL from fill-in form
    max_level = request.form.get('max_level') # gets max search depth
    search_type = request.form.get('comp_select') # gets search mode
    uastring = request.headers.get('user_agent') # gets browser type

    # interprets search type picked by user
    if search_type == "Search for links from the 1st paragraph":
        search_mode = 1
    elif search_type == "Search for links from the introduction":
        search_mode = 2
    elif search_type == "Search for links from the entire page":
        search_mode = 3
    else:
        search_mode = 0 # or throw some error
    
    # checks browser type of user
    isMobileBrowser = False
    if "Mobile" in uastring:
        isMobileBrowser = True

    # data processing
    if source_url: # to edit throw error/exception
        nodeList, linkList = generate_lists(source_url, max_level, isMobileBrowser, search_mode)

    return render_template("result.html", nodeList = nodeList, linkList = linkList)

if __name__ == "__main__":
    app.run(debug=True)