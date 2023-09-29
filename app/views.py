import yaml
import requests
import json
from lxml import etree
from bs4 import BeautifulSoup
from flask import render_template, request, abort

from app import app, basic_auth
from app.models import Source
from app.forms import TestForm, DebugForm
from app.ulti import *



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/playground', methods=['GET', 'POST'])
@basic_auth.required
def playground():
    form = TestForm(request.form)
    results = []
    if request.method == 'POST' and form.validate():
        config = yaml.safe_load(form.config.data)
        root, _, fetch_error = fetch_and_parse(form.url.data)
        if root:
            results, error = extract_data_from(root, config)
            if error:
                form.config.errors.append(error)
        else:
            form.config.errors.append(fetch_error)

    return render_template('playground.html', form=form, results=json.dumps(results, indent=2))


@app.route('/debug', methods=['GET', 'POST'])
@basic_auth.required
def debug():
    form = DebugForm(request.form)
    html = ""
    if request.method == 'POST' and form.validate():
        root, tree, error = fetch_and_parse(form.url.data)
        if error:
            form.url.errors.append(error)
            return render_template("debug.html", html=html, form=form)

        for element in root.iter():
            if type(element) is etree._Element:
                element.set("title", tree.getelementpath(element))
                if element.text is None:
                    element.text = ''
        html = etree.tostring(root.xpath("//body")[0],  method='html', pretty_print=True).decode()

    return render_template("debug.html", html=html, form=form)


@app.route('/rss/<slug>', methods=['GET', 'POST'])
def rss(slug=None):
    source = Source.query.filter_by(slug=slug).first_or_404()
    root, _, error = fetch_and_parse(source.url)
    if error:
        return abort(500, error)
    
    config = yaml.safe_load(source.config)
    results, error = extract_data_from(root, config)
    if error:
        return abort(500, error)

    return gen_feed(source.name, source.url, config['date_format'], results)