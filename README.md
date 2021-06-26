# SociaLod
<img src="static/icons8-social-network-100.png">

Description
---

Search by user name with set social media publicly available information. That make a Human information resources with recursive search.

REQUIREMENTS
---
    root# pip3 install -r requirements.txt

CONFIG
---
    create .env file and config belows 
        FB_USER="{Your-facebook -username}"
        FB_PASS="{Your-facebook-password}"
        LN_USER="{Your-linkedin-username}"
        LN_PASS="{Tour-linkedin-password}"

RUN
---
    root# python3 app.py -h
    usage: app.py [-h] [-u USERNAME]

    SociaLod Social media informations scrapper by username matches

    optional arguments:
    -h, --help     show this help message and exit
    -u USERNAME    Social media common username

USE
---
    root# python3 app.py -u usernanme