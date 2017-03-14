from urllib.request import urlopen
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import requests
import time
import base64
from random import randint
from itertools import islice
import sys
import urllib.request
import sqlite3 as lite
from datetime import date
import urllib
import re


class vpsscraper(object):
    def __init__(self):
        self.total_req = 0
        self.result_pointer = None
        self.resultdb = None
        self.today = date.today()
        self.url = ["http://www.slak.nl/platform/evenementen/locaties/?pno=1"]

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Accept':"application/json, text/javascript, */*; q=0.01",
            "X-Requested-With:":"XMLHttpRequest"
        }


    def create_table(self):
        try:
            self.resultdb = lite.connect('D:/database/vast-goed-beschermer/vast-goed-beschermer.db')
            self.result_pointer = self.resultdb.cursor()
        except lite.Error as e:
            print(e)
            sys.exit(1)

        antikraakpanden = "CREATE TABLE IF NOT EXISTS antikraak_woning (id TEXT PRIMARY KEY NOT NULL,stad TEXT,postcode TEXT, prijs TEXT, kortebeschrijving TEXT,omschrijving TEXT," \
                          "link TEXT, " \
                          "created_at DATE)"
        antikraakfoto = "CREATE TABLE IF NOT EXISTS fotoid (id TEXT,foto_naam TEXT NOT NULL, FOREIGN KEY(id) REFERENCES antikraak_woning(id))"
        self.result_pointer.execute(antikraakpanden)
        self.result_pointer.execute(antikraakfoto)


    def scrapy(self):
        scrape_links = []
        return


    def scrape_data(self):
        array_links = self.scrapy()

        for links in array_links:
            print()
        return


    def connectieopen(self,link):
        time.sleep(1)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Language": "en-US,en;q=0.5",
                'Accept-Encoding':'utf-8'}


        self.total_req += 1
        slapen = randint(1, 2)

        time.sleep(slapen)

        print(self.total_req)

        try:
            session = requests.Session()

            req = session.get(link, headers=headers)
            content = req.content
        except HTTPError as fout:
            print(fout + link)
        except URLError as fout:
            print("cant find url")
        except ConnectionError as e:
            print(e)
            print(link)
        else:
            return content
        print("Hallo")


scraper = vpsscraper()

scraper.scrape_date()