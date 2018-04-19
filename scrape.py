# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import dryscrape
import json
import re
import time
import os
from selenium import webdriver
import argparse
from selenium.webdriver import FirefoxOptions
#f = open('all.csv', 'r+')
# specify the url
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--start', dest='start')
parser.add_argument('--end', dest='end')
args = parser.parse_args()
fileName = 0
pgnName = 0
for x in range(int(args.start), int(args.end)):
    #try:
        size = os.path.getsize('moves'+str(fileName)+'.csv')
        if (size > 9000000):
            fileName += 1
        if (os.path.getsize('pgns'+str(pgnName)+'.csv')>9000000):
            pgnName += 1
        f = open('moves'+str(fileName)+'.csv', 'a')
        pgns = open('pgns'+str(fileName)+'.csv', 'a')
        canOpen = False
            #try:
        quote_page = 'http://lczero.org/match_game/' + str(x)
                #session = dryscrape.Session()
                #session.visit(quote_page)
                #response = session.body()
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=opts)
        driver.set_page_load_timeout(30)
                #driver = webdriver.PhantomJS()
        driver.get(quote_page)
        response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser').find('div', {'id':re.compile('yui-gen*')})
        driver.quit()
        if(soup):
            # query the website and return the html to the variable ‘page’
           # response = urlopen(quote_page)
            
            # parse the html using beautiful soup and store in variable `soup`
            soup = BeautifulSoup(response, 'html.parser').findAll('span', {'id':re.compile('training-m\d')})
            pgn = ''
            count = 0
            for n in soup:
                if(n.find('span',{'class':'ct-board-move-movenum'})):
                    pgn += n.find('span',{'class':'ct-board-move-movenum'}).contents[0] 
                if( n.find('span',{'class':'ct-board-move-movetext'}) != 'None'):
                    pgn += n.find('span',{'class':'ct-board-move-movetext'}).contents[0]
                count += 1
            outcome = ''
            outcomeCode = ''
            if(re.search('1/2-1/2',pgn)):
                outcome = 'draw'
                outcomeCode = '1/2-1/2'
            elif re.search('0-1',pgn):
                outcome = 'black win'
                outcomeCode = '0-1'
            elif re.search('1-0',pgn):
                outcome = 'white win'
                outcomeCode = '1-0'
            else:
                outcome = 'unknown'
            #test = soup[2].text.split(',')[1].replace('\\n','').replace('\\x','').replace('\\','').replace('pgnString','').replace(':','').replace('\'','')
            #print(re.sub('\d+\.', '', test))
            #print(test)
            #print(re.finditer('(!?([0-9]+\.))',test))
            #n = ''
            #for n in re.finditer('(!?([0-9]+\.))',test):
            #    pass
            f.write(str(count)+','+quote_page+'\n')
            pgns.write(str(x)+','+pgn+'\n')
            pgns.close()
            f.close()
            #print(re.sub('[a-zA-Z]+\d','',re.sub('=+[a-zA-Z]', '', re.sub('-','',test))).replace('.',''))
            # Take out the <div> of name and get its value
            #name_box = soup.find('div', attrs={'id': 'training-moves'})
            #for n in name_box.children:
            #    print(n)
            #name = name_box.text.strip() # strip() is used to remove starting and trailing
            #print(name_box)
        #except:
        else:
            errorfile = open('error.txt', 'a')
            errorfile.write(quote_page+'\n')
            errorfile.close()
            f.write('error'+','+quote_page+'\n')
            f.close()
            pgns.close()
    #except:
    #    f.write('error getting ,'+quote_page+'\n')
    #    f.close()
    #    pgns.close()
            #f.close()
            #pgns.close()
