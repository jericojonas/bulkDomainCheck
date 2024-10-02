Automation for Checking Domains Status
- Bulk checking domains status Blocked or not in Indonesia.
Government site checking tools: https://trustpositif.kominfo.go.id/
- domains data retrieve from google sheet
- after checking, will send the checking result automatically to telegram group


Build using Python3 and Selenium

_______________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________

How to Use
- Make Google Sheet File and list your domains, put the sheet name on "gs.js"
- Get Google API Credentials to access your google sheet file, put on "credentials.js"
- Put your Google Firebase Credentials on "serviceAccountKey.json", and put your collection name on "fire.py"
- Make telegram bot and put the not token on "tele.py"
- Get telegram chat ID and put on "tele.py"
https://api.telegram.org/bot{yourbot}/getUpdates
- Run the app "python trust.py"

Optional
if you want to build the REST API to monitor the details of checking result
- prepare your own domain and hosting
- upload "server.mjs" file
- customize and run "server.mjs" file
- put your domain on tele.py

_______________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________


Requirement
- python3
- pip
- chrome webdriver
- requests
- oauth2client
- gspread
- use IP Indonesia

Install command
- pip install virtualenv
- pip install selenium
- pip install requests
- pip install oauth2client
- pip install gspread
- pip install firebase-admin
- pip install pytz (phillipine time)

Check installation details
- pip show selenium
- pip show oauth2client
- pip show requests
- pip show firebase admin

API Server
- npm init -y
- npm install express firebase-admin
- cd server
- node server.js

Port Always running
- sudo npm install -g pm2
- pm2 start server.mjs --name my-server
- pm2 status
- pm2 start my-server
- pm2 stop my-server


