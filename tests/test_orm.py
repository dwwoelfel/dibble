# -*- coding: utf-8 -*-
import pymongo

def setup():
    con = pymongo.Connection()
    db = con['dibbletest']

