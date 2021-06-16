# SociaLod
<img src="static/icons8-social-network-100.png">

Description
---

Search by user name with set social media publicly available information. That make a Human information resources with recursive search.

REQUIREMENTS
---

    root# pip3 install requirements.txt

RUN
---
    root# python3 app.py -h
    usage: app.py [-h] [-u USERNAME] [-fbu FBUSER] [-fbp FBPASSWD] [-lnu LNUSER] [-lnp LNPASSWD]

    SociaLod Social media informations scrapper by username matches

    optional arguments:
    -h, --help     show this help message and exit
    -u USERNAME    Social media common username
    -fbu FBUSER    Facebook username for login
    -fbp FBPASSWD  Facebook password for login
    -lnu LNUSER    LinkedIn username for login
    -lnp LNPASSWD  LinkedIn password for login

USE
---
    root# python3 app.py -u usernanme -fbu facebookbusername -fbp facebookpassword -lnu linkedinusername -lnp linkedinpassword