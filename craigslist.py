from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime
import csv
import sys
import os
import smtplib
import config
import time

#HOUR_GAP = 36


# Craigslist search URL
BASE_URL = ('http://sfbay.craigslist.org/search/sfc/fuo?sort=rel&maxAsk=250&query={0}') 
# max price at 250
#&areaID=11&subAreaID=&catAbb=sss

def parse_results(search_term):
    results = []
    search_term = search_term.strip().replace(' ', '+')
    search_url = BASE_URL.format(search_term)
    soup = BeautifulSoup(urlopen(search_url).read())
    rows = soup.find('div', 'content').find_all('p', 'row')
    for row in rows:
        url = 'http://sfbay.craigslist.org' + row.a['href']
        #price = row.find('span', class_='price').get_text()
        create_date = row.find('time').get('datetime')
        title = row.find_all('a')[1].get_text()
        results.append({'url': url, 'create_date': create_date, 'title': title})
    return results

def write_results(results):
    """Writes list of dictionaries to file."""
    fields = results[0].keys()
    with open('results.csv', 'w') as f:
        dw = csv.DictWriter(f, fieldnames=fields, delimiter='|')
        dw.writer.writerow(dw.fieldnames)
        dw.writerows(results)

def has_new_records(results):
    current_posts = [x['url'] for x in results]
    fields = results[0].keys()
    if not os.path.exists('results.csv'):
        return True

    with open('results.csv', 'r') as f:
        reader = csv.DictReader(f, fieldnames=fields, delimiter='|')
        seen_posts = [row['url'] for row in reader]

    is_new = False
    for post in current_posts:
        if post in seen_posts:
            pass
        else:
            is_new = True
    return is_new

# change this to send email instead of text
def send_email(email_addr, msg):
    fromaddr = "Craigslist Checker"
    msg = ("From: {0}\r\nTo: {1}\r\n\r\n{2}").format(fromaddr, email_addr, msg)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(config.email['username'], config.email['password'])
    server.sendmail(fromaddr, email_addr, msg)
    server.quit()

def get_current_time():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    try:
        TERM = sys.argv[1]
        #!nchange#
        email_addr= sys.argv[2]
    except:
        print "You need to include a search term and an email address!\n"
        sys.exit(1)

    #if len(PHONE_NUMBER) != 10:
        #print "Phone numbers must be 10 digits!\n"
        #sys.exit(1)

    results = parse_results(TERM)
    
    # Send the SMS message if there are new results
    if has_new_records(results):
        message = "Hey - there are new Craigslist posts for: {0}".format(TERM.strip())
        print "[{0}] There are new results - sending email message to {0}".format(get_current_time(), email_addr)
        send_email(email_addr, message)
        write_results(results)
    else:
        print "[{0}] No new results - will try again later".format(get_current_time())

