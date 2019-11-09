#!/usr/bin/env python
# coding: utf-8

# In[3]:


from flask import Flask
from flask_flatpages import FlatPages
# from flask_frozen import Freezer

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

