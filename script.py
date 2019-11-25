import config
import mechanicalsoup
from bs4 import BeautifulSoup
from threading import Timer
from twilio.rest import Client

browser = mechanicalsoup.StatefulBrowser()
client = Client(config._accountSID, config._authToken)

def searchClass(dept, courseNum, courseId):
  response = browser.open("https://www.reg.uci.edu/perl/WebSoc")
  form = browser.select_form('form[action="https://www.reg.uci.edu/perl/WebSoc"]')

  form["Dept"] = dept
  form["CourseNum"] = courseNum

  response = browser.submit_selected()

  soup = browser.get_current_page()
  code = soup.find(string=courseId).find_parent('td')
  # print(code)
  td = code.find_next_siblings('td')
  counts = td[7:9]

  status = str(td[15])[38:42]
  maxCounts = int(str(counts[0])[52:55])
  enrolledCounts = int(str(counts[1])[34:37])

  message = "WEBREG: " + dept + " " + courseNum + " Spots Open!\n" + "Current status: " + str(enrolledCounts) + "/" + str(maxCounts) + "\nClass Code: " + courseId + "\nCheck for discussion sections" + "\nhttps://www.reg.uci.edu/registrar/soc/webreg.html"

  if (status == "OPEN"):
    for num in config._to:
      client.messages.create(to=num, 
                            from_=config._from, 
                            body=message)


searchClass("I&C SCI", "53", "35590")
searchClass("COMPSCI", "171", "34340")