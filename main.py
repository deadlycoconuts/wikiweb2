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
    error = None
    source_url = request.form.get('search_body') # gets search URL from fill-in form
    max_level = request.form.get('max_level')

    # data processing
    if source_url:
        nodeList, linkList = full_clean_up(source_url, 0, max_level)
    # to edit throw error/exception

    return render_template("result.html", nodeList = nodeList, linkList = linkList)

if __name__ == "__main__":
    app.run(debug=True)