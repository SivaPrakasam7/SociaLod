#!/bin/python3
# from flask import Flask,render_template,redirect,session
from selenium import webdriver
from bs4 import BeautifulSoup
from collections import defaultdict
from time import sleep

import chromedriver_autoinstaller
import re
import requests
import pprint
import json
import argparse


class BROWSER: # selenium browser initilization
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chromedriver_autoinstaller.install(),chrome_options=chrome_options)


class COMMON: # Common function for all classes
    def __init__(self):pass

    def error(self, code):# Error handler
        try:return eval(code)
        except:pass

    def handle(self,var,val):
        try:return eval(val)
        except Exception as e:
            print(e,val)
            return None


class FACEBOOK: # Login required
    def __init__(self,url,luser,lpasswd):
        self.url=f'https://www.facebook.com/{url}'
        self.rslt=defaultdict(dict)
        self.detail=[['Overview','Work_and_education','Places','Contact_and_basic_info','Family_and_relationships','Details','Life_events'],['Photos','Videos','Friends']]
        self.browser=BROWSER().browser
        self.cm=COMMON()
        self.login(luser,lpasswd)
        self.mine()

    def login(self,luser,lpasswd):
        self.browser.get('https://www.facebook.com/login')
        user=self.browser.find_element_by_id('email')
        passwd=self.browser.find_element_by_id('pass')
        login=self.browser.find_element_by_name('login')
        user.send_keys(luser)
        passwd.send_keys(lpasswd)
        login.click()
        sleep(0.5)
        
    def mine(self):
        for about in self.detail[0]:
            self.browser.get(f'{self.url}/about_{about.lower()}')
            sleep(3)
            self.soup=BeautifulSoup(self.browser.page_source,'html5lib')
            self.rslt[about]=self.soup.find('div',{'class':'dati1w0a tu1s4ah4 f7vcsfb0 discj3wi'}).get_text('\n').split('\n')
        self.rslt['Profile']=self.soup.find('div',{'class':'b3onmgus e5nlhep0 ph5uu5jm ecm0bbzt spb7xbtv bkmhp75w emlxlaya s45kfl79 cwj9ozl2'}).find('image').get('xlink:href')
        self.rslt['Social']=list(set([n.get('href').replace('mailto:','') for n in self.soup.find_all('a',href=re.compile(r'(https://twitter.com/.*|https://www.linkedin.com/in/.*|mailto:.*|https://t.me/.*|https://www.instagram.com/.*|https://github.com/.*|https://www.pinterest.com/.*|https://www.reddit.com/user/.*)'))]))
        self.browser.get(f'{self.url}/friends')
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep(1)
        self.soup=BeautifulSoup(self.browser.page_source,'html5lib')
        self.rslt['Media']=[{n.find('img').get('src'):[n.find('img').get('alt').strip(),[m.strip() for m in n.get_text('\n').split('\n') if m.strip()]]} for n in self.soup.find_all('div',{'class':re.compile(r'(rq0escxv rj1gh0hx buofh1pr ni8dbmo4 stjgntxs l9j0dhe7|bp9cbjyn ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi n1f8r23x rq0escxv j83agx80 bi6gxh9e discj3wi hv4rvrfc ihqw7lf3 dati1w0a gfomwglr)')}) if n.find('img')]


class LINKEDIN: # Login required Certificate error BeautifulSoup used
    def __init__(self,url,luser,lpasswd):
        self.url=f'https://www.linkedin.com/in/{url}'
        self.rslt=defaultdict(dict)
        self.browser=BROWSER().browser
        self.cm=COMMON()
        self.login(luser,lpasswd)
        self.mine()

    def login(self,luser,lpasswd):
        self.browser.get('https://www.linkedin.com/login')
        user=self.browser.find_element_by_id('username')
        passwd=self.browser.find_element_by_id('password')
        login=self.browser.find_element_by_class_name('btn__primary--large')
        user.send_keys(luser)
        passwd.send_keys(lpasswd)
        login.click()
        sleep(0.5)
        
    def mine(self):
        self.browser.get(self.url)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep(2)
        self.soup=BeautifulSoup(self.browser.page_source,'html5lib')
        self.rslt['Profile']=self.soup.find('img',{'class':'pv-top-card__photo'}).get('src')
        self.rslt['Name']=self.soup.find('img',{'class':'pv-top-card__photo'}).get('alt')
        self.rslt['Intro']=[n.strip() for n in self.soup.find('div',{'class':'display-flex justify-space-between pt2'}).get_text('\n').split('\n') if n.strip()]
        try:self.rslt['Activity']=[[m.strip() for m in n.get_text('\n').split('\\n') if m.strip()] for n in self.soup.find('ul',{'class':'pv-recent-activity-section-v2__column-activity list-style-none'}).find_all('li')]
        except:self.rslt['Activity']=self.cm.handle(self.soup,"var.find('div',{'class':'pv-recent-activity-section-v2__columns'}).find('p').get_text('\\n').strip()")
        self.rslt['About']=self.cm.handle(self.soup,"[n.strip() for n in var.find('section',{'class':'pv-about-section'}).find('div').get_text('\\n').split('\\n') if n.strip()]")
        self.rslt['Experience']=self.cm.handle(self.soup,"[[m.strip() for m in n.get_text('\\n').split('\\n') if m.strip()] for n in var.find('section',{'class':'experience-section'}).find('ul').find_all('li')]")
        self.rslt['Education']=self.cm.handle(self.soup,"[[m.strip() for m in n.get_text('\\n').split('\\n') if m.strip()] for n in var.find('section',{'class':'education-section'}).find('ul').find_all('li')]")
        self.rslt['Certification']=self.cm.handle(self.soup,"[[m.strip() for m in n.get_text('\\n').split('\\n') if m.strip()] for n in var.find('section',{'id':'certifications-section'}).find('ul').find_all('li')]")
        self.rslt['Volunteer']=self.cm.handle(self.soup,"[[m.strip() for m in n.get_text('\\n').split('\\n') if m.strip()] for n in var.find('section',{'class':'pv-profile-section volunteering-section ember-view'}).find('ul').find_all('li')]")
        self.rslt['Skills']=self.cm.handle(self.soup,"[[m.strip() for m in n.get_text('\\n').split('\\n') if m.strip()] for n in var.find('ol',{'class':'pv-skill-categories-section__top-skills pv-profile-section__section-info section-info pb1'}).find_all('li')]")
        self.rslt['Interests']=self.cm.handle(self.soup,"[[m.strip() for m in n.get_text('\\n').split('\\n') if m.strip()] for n in var.find('section',{'class':'pv-profile-section pv-interests-section artdeco-card mt4 p5 ember-view'}).find('ul').find_all('li')]")
        self.browser.get(f'{self.url}/detail/contact-info/')
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        self.soup=BeautifulSoup(self.browser.page_source,'html5lib')
        self.rslt['Contact info']=[n.strip() for n in self.soup.find('div',{'class':'pv-profile-section__section-info section-info'}).get_text('\n').split('\n') if n.strip()]
        self.rslt['Social']=list(set([n.get('href').replace('mailto:','') for n in self.soup.find_all('a',href=re.compile(r'((https://|)twitter.com/.*|(https://|)www.facebook.com/.*|mailto:.*|https://t.me/.*|(https://|)www.instagram.com/.*|(https://|)github.com/.*|(https://|)www.pinterest.com/.*|(https://|)www.reddit.com/user/.*)'))]))


class GITHUB: # Nologin BeautifulSoup used
    def __init__(self,url):
        self.url=f'https://github.com/{url}'
        self.rslt=defaultdict(dict)
        self.soup=BeautifulSoup(requests.get(url).content,'html5lib')
        self.cm=COMMON()
        self.mine()
    
    def mine(self):
        self.rslt['Profile']=self.soup.find('img',src=re.compile(r'https://avatars.githubusercontent.com/u/.*')).get('src').replace('s=64','s=100')
        self.rslt['Name']=[n.strip() for n in self.soup.find('h1',{'class':'vcard-names'}).text.split('\n') if n.strip()]
        self.rslt['Social']=list(set([n.get('href').replace('mailto:','') for n in self.soup.find_all('a',href=re.compile(r'(https://twitter.com/.*|https://www.linkedin.com/in/.*|mailto:.*|https://t.me/.*|https://www.instagram.com/.*|https://www.facebook.com/.*|https://www.pinterest.com/.*|https://www.reddit.com/user/.*)'))]))
        self.rslt['About']=[n.strip() for n in self.soup.find('div',{'class':'js-profile-editable-area d-flex flex-column d-md-block'}).get_text('\n').split('\n') if n.strip()]
        self.rslt['Achivements']=self.cm.handle(self.soup,"[{n.get('alt'):n.get('src')} for n in var.find('div',{'class':'border-top color-border-secondary pt-3 mt-3 d-none d-md-block'}).find_all('img',src=re.compile(r'^https://github.githubassets.com/.*'))]")
        self.rslt['Organizations']=self.cm.handle(self.soup,"[{'https://github.com'+n.get('href'):json.loads(n.get('data-hydro-click')).pop('payload')} for n in var.find('div',{'class':'border-top color-border-secondary pt-3 mt-3 clearfix hide-sm hide-md'}).find_all('a',{'data-hovercard-type':'organization'})]")
        self.rslt['Projects']=self.cm.handle(self.soup,"[[m.strip() for m in n.text.split(\n) if m.strip()] for n in var.find('ol',{'class':'d-flex flex-wrap list-style-none gutter-condensed mb-4 js-pinned-items-reorder-list'}).find_all('div',{'class','pinned-item-list-item-content'})]")
        try:self.rslt['Activity']['Commits'],self.rslt['Activity']['Created']=[[{re.sub(r"\n.*\n?"," - ",m.text.replace(' ','').strip()):f"https://github.com{m.find('a',href=True).get('href')}"} for m in n.find_all('li') if m.text.replace(' ','').strip()] for n in self.soup.find('div',{'id':'js-contribution-activity'}).find_all('ul',{'class':'list-style-none mt-1'})]
        except:self.rslt['Activity']['Commits'],self.rslt['Activity']['Created']=None,None


class INSTAGRAM: # Nologin https://www.instagram.com/harishwarrior
    def __init__(self,url):
        self.url=f'https://www.instagram.com/{url}'
        self.rslt=defaultdict(dict)
        self.browser=BROWSER().browser
        self.cm=COMMON()
        self.mine()
        
    def mine(self):
        self.browser.get(self.url)
        self.rslt['Profile']=None


class PINTEREST: # Nologin BeautifulSoup used
    def __init__(self,url):
        self.url=f'https://www.pinterest.com/{url}'
        self.rslt=defaultdict(dict)
        self.browser=BROWSER().browser
        self.cm=COMMON()
        self.mine()
        
    def mine(self):
        self.browser.get(self.url)
        self.soup=BeautifulSoup(self.browser.page_source,'html5lib')
        self.rslt['Profile']=self.soup.find('img').get('src')
        self.rslt['Name']=self.soup.find('img').get('alt')
        self.rslt['Social']=list(set([n.get('href').replace('mailto:','') for n in self.soup.find_all('a',href=re.compile(r'(https://www.linkedin.com/in/.*|https://www.facebook.com/.*|mailto:.*|https://t.me/.*|https://www.instagram.com/.*|https://github.com/.*|https://www.reddit.com/user/.*)'))]))
        for l in [n.get('href').split('/')[2] for n in self.soup.find_all('a',{'class':'boardLinkWrapper'})]:
            self.browser.get(f'{self.url}/{l}')
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            self.soup=BeautifulSoup(self.browser.page_source,'html5lib')
            try:self.rslt[l.replace(self.url,'').replace('/','')]=[{n.get('src'):n.get('alt').strip()} for n in self.soup.find_all('img',{'class':'GrowthUnauthPinImage__Image'})]
            except:pass


class TWITTER: # Nologin BeautifulSoup used
    def __init__(self,url):
        self.url=f'https://twitter.com/{url}'
        self.rslt=defaultdict(dict)
        self.browser=BROWSER().browser
        self.cm=COMMON()
        self.mine()
        
    def mine(self):
        self.browser.get(self.url)
        sleep(3)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        self.soup=BeautifulSoup(self.browser.page_source,'html5lib')
        self.rslt['Profile']=self.cm.handle(self.soup,"var.find('img',src=re.compile(r'^https://pbs.twimg.com/profile_images/.*')).get('src')")
        self.rslt['Name']=self.soup.find('div',{'class':'css-1dbjc4n r-1wbh5a2 r-dnmrzs r-1ny4l3l'}).get_text('\n').strip()
        self.rslt['Intro']=[n.get_text('\n').strip() for n in self.soup.find_all('div',{'class':'css-1dbjc4n r-1adg3ll r-6gpygo'})]
        self.rslt['Tweets']=[self.cm.handle(n,"{var.find('img',{'class':'css-9pa8cd'}).get('src'):[m.strip() for m in var.get_text('\\n').split('\\n') if m.strip()]}") for n in self.soup.find_all('div',{'data-testid':'tweet'})]
        self.rslt['Social']=list(set([n.get('href').replace('mailto:','') for n in self.soup.find_all('a',href=re.compile(r'(https://www.linkedin.com/in/.*|https://www.facebook.com/.*|mailto:.*|https://t.me/.*|https://www.instagram.com/.*|https://github.com/.*|https://www.pinterest.com/.*|https://www.reddit.com/user/.*)'))]))


class TIKTOK: # No login https://www.tiktok.com/@canadianmilitary8?
    def __init__(self,url):
        self.url=f'https://www.tiktok.com/{url}'
        self.rslt=defaultdict(dict)

    def mine(self):pass


class REDDIT: # No login BeautifulSoup used
    def __init__(self,url):
        self.url=f'https://www.reddit.com/user/{url}'
        self.rslt=defaultdict(dict)
        self.browser=BROWSER().browser
        self.cm=COMMON()
        self.mine()

    def mine(self):
        self.browser.get(self.url)
        self.soup=BeautifulSoup(self.browser.page_source,'html5lib')
        try:self.rslt['Profile']=self.soup.find('img',{'class':'_2bLCGrtCCJIMNCZgmAMZFM'}).get('src')
        except:self.rslt['Profile']=self.soup.find('img',{'class':'_2TN8dEgAQbSyKntWpSPYM7 _3Y33QReHCnUZm9ewFAsk8C'}).get('src')
        self.rslt['Name']=self.cm.handle(self.soup,"var.find('h1',{'class':'_3LM4tRaExed4x1wBfK1pmg'}).get_text('\\n')")
        self.rslt['About']=self.cm.handle(self.soup,"var.find('div',{'class':'bVfceI5F_twrnRcVO1328'}).get_text('\\n').split('\\n')")
        self.rslt['Posts']=[n.text.split('\n') for n in self.soup.find_all('div',{'class':'_1qftyZQ2bhqP62lbPjoGAh _3Qkp11fjcAw9I9wtLo8frE _3KGXodqw9Ht3MoBpe8_gzB scrollerItem'})]
        self.rslt['Trophy']=[{n.find('img').get('src'):n.find('h5').get_text('\n').strip()} for n in self.soup.find_all('div',{'class':'_2CUZHyZpRYmdvLE9tOI-2L QY_PhyoOHbRd-_92ivr-m'})]
        self.rslt['Social']=list(set([n.get('href').replace('mailto:','') for n in self.soup.find_all('a',href=re.compile(r'(https://www.linkedin.com/in/.*|https://www.facebook.com/.*|mailto:.*|https://t.me/.*|https://www.instagram.com/.*|https://github.com/.*|https://www.pinterest.com/.*|https://twitter.com/.*)'))]))


class MINE:
    def __init__(self,username):
        self.username=username
        self.rslt=defaultdict(dict)

    def mine(self,fbu,fbp,lnu,lnp):
        self.rslt['facebook']=FACEBOOK(self.username,fbu,fbp).rslt # verified
        self.rslt['linkedin']=LINKEDIN(self.username,lnu,lnp).rslt # verified
        self.rslt['github']=GITHUB(self.username).rslt # verified
        # self.rslt['instagram']=INSTAGRAM(self.username).rslt # Test in windows Not used
        self.rslt['pinterest']=PINTEREST(self.username).rslt # verified
        self.rslt['twitter']=TWITTER(self.username).rslt # verified
        # self.rslt['tiktok']=TIKTOK(self.username).rslt # Not used
        self.rslt['reddit']=REDDIT(self.username).rslt # verified
        pprint.pprint(self.rslt)
        open(f'{self.username}.json','w').write(json.dumps(self.rslt,indent=4))


if __name__=='__main__':
    arg=argparse.ArgumentParser(description='SociaLod Social media informations scrapper by username matches')
    arg.add_argument('-u',dest='username',help='Social media common username')
    arg.add_argument('-fbu',dest='fbuser',help='Facebook username for login')
    arg.add_argument('-fbp',dest='fbpasswd',help='Facebook  password for login')
    arg.add_argument('-lnu',dest='lnuser',help='LinkedIn username for login')
    arg.add_argument('-lnp',dest='lnpasswd',help='LinkedIn password for login')
    opt=arg.parse_args()
    MINE(f'{opt.username}').mine(f'{opt.fbuser}',f'{opt.fbpasswd}',f'{opt.lnuser}',f'{opt.lnpasswd}')