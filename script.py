import mechanicalsoup
from bs4 import BeautifulSoup
import requests
from threading import Timer
from twilio.rest import Client

browser = mechanicalsoup.StatefulBrowser()

response = browser.open("https://www.reg.uci.edu/perl/WebSoc")
form = browser.select_form('form[action="https://www.reg.uci.edu/perl/WebSoc"]')

form["Dept"] = "I&C SCI"
form["CourseNum"] = "53"

response = browser.submit_selected()

soup = browser.get_current_page()
code = soup.find(string="35590").find_parent('td')
# print(code)
td = code.find_next_siblings('td')
counts = td[7:9]

status = str(td[15])[38:42]
maxCounts = int(str(counts[0])[52:55])
enrolledCounts = int(str(counts[1])[34:37])

client = Client("AC7c09234936d0a3e628ff95cb236f094e", "e95941bafd158537584bf2bdd4027578")
message = "WEBREG: ICS 53 Spots Open!\n" + "Current status: " + str(enrolledCounts) + "/" + str(maxCounts) + "\nClass Code: 35590, 35591\nCheck for discussion sections" + "\nhttps://www.reg.uci.edu/registrar/soc/webreg.html"

if (status == "OPEN"):
  client.messages.create(to="+14159968939", 
                        from_="+13475072147", 
                        body=message)