#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, request, url_for
from process_link import full_clean_up

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index():
    return render_template("search.html") # displays initial search bar

@app.route("/result", methods=['GET', 'POST'])
def result():
    data = []
    #error = None # to implement in the future
    source_url = request.form.get('search_body') # gets search URL from fill-in form
    max_level = request.form.get('max_level')
    uastring = request.headers.get('user_agent')
    isMobileBrowser = False
    if "Mobile" in uastring:
        isMobileBrowser = True
    # data processing
    if source_url: # to edit throw error/exception
        nodeList, linkList = full_clean_up(source_url, 0, max_level, isMobileBrowser)

    return render_template("result.html", nodeList = nodeList, linkList = linkList)

if __name__ == "__main__":
    app.run(debug=True)