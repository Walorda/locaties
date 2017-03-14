from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import requests
import time
from random import randint
from requests import session
import sys
import sqlite3 as lite
from datetime import date
import re




class vpsscraper(object):
    def __init__(self):
        self.total_req = 0
        self.result_pointer = None
        self.resultdb = None
        self.today = date.today()
        self.s = requests.session()




        self.headers = {
            "Host": "www.gapph.nl",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Accept": "*/*",
            "Accept-Encoding":"gzip, deflate, br",
            "X-Requested-With":"XMLHttpRequest",
            "Referer": "https://www.gapph.nl/overzicht-aanbod.aspx",
            "Cookie": "ASP.NET_SessionId=aobiwxbtykffpr45uv4pud55; _gat=1",
            "Connection": "keep-alive"


        }

    def create_table(self):
        try:
            self.resultdb = lite.connect('D:/database/vps-nl/vps.db')
            self.result_pointer = self.resultdb.cursor()
        except lite.Error as e:
            print(e)
            sys.exit(1)

        antikraakpanden = "CREATE TABLE IF NOT EXISTS antikraak_woning (id TEXT PRIMARY KEY NOT NULL,stad TEXT,lat TEXT,lng TEXT,omscrhijving TEXT, prijs TEXT, beschikbaar TEXT,type TEXT," \
                          "kosten TEXT,btw TEXT,servicekosten TEXT,schuur TEXT,parkeerplaats TEXT,tuin_bakon TEXT,twee_persoon_aanmelding TEXT,inkomensverklaring TEXT, link TEXT,img TEXT, " \
                          "created_at DATE)"
        antikraakfoto = "CREATE TABLE IF NOT EXISTS fotoid (id TEXT,foto_naam TEXT NOT NULL, FOREIGN KEY(id) REFERENCES antikraak_woning(id))"
        self.result_pointer.execute(antikraakpanden)
        self.result_pointer.execute(antikraakfoto)


    def scrapy(self):

        url = "https://www.gapph.nl"
        r = self.s.get(url)
        dic = r.headers
        self.headers['Cookie'] = dic['Set-Cookie']







        url = "https://www.gapph.nl/GetList.aspx?x1=50,359010490830606&x2=53,73528010549542&y1=1,2835392578124356&y2=9,050873242187436"




        r = requests.request('GET',url,headers=self.headers)
        bsObj = BeautifulSoup(r.content.decode('utf-8','ignore'), "html.parser")
        link = bsObj.findAll('div',attrs={'class':'more'})
        array_links = []
        for each in link:
            links = each.find('a')
            array_links.append(links['href'])


        del array_links[0]


        bijhouden = 0

        return array_links



    def scrape_data(self):
        euro_rg = re.compile(r'(€+\s*[0-9]+[,-]*)\s*[a-z]*\s*€*([0-9]{0,3}[,-]*[0-9]{0,2})', re.I | re.M)
        oppervlakte_rg = re.compile(r'[0-9]+\s*[m]+\s*[2²]+')
        array_links = self.scrapy()
        for links in array_links:
            bsObj = self.connectieopen('https://gapph.nl/'+links)
            pintro_text = bsObj.find('p',attrs={'class':'intro'}).getText()
            title_text = bsObj.find('div',attrs={'class':'title'}).getText()
            container = bsObj.find('article',attrs={'id':'divContent'})

            ullist = container.find('ul')
            lilist = ullist.findAll('li')

            tocompare = container.getText()
            prijs = re.findall(euro_rg, tocompare)

            oppervlakte = re.findall(oppervlakte_rg, tocompare)
            if prijs:
             print(prijs)
            if oppervlakte:
             print(oppervlakte)

            for list in lilist:
                tocompare = list.getText()
                prijs  = re.findall(euro_rg,tocompare)


                oppervlakte = re.findall(oppervlakte_rg,tocompare)
                # if prijs:
                #     print(prijs)
                # if oppervlakte:
                #     print(oppervlakte)








            print("https://www.gapph.nl/"+links)


        return








    def connectieopen(self,link):
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
            bsObj = BeautifulSoup(content.decode('utf-8','ignore'), "html.parser")
        except HTTPError as fout:
            print(fout + link)
        except URLError as fout:
            print("cant find url")
        except ConnectionError as e:
            print(e)
            print(link)
        else:

            return bsObj







scraper = vpsscraper()

scraper.scrape_data()
