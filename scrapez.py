#!/bin/python
# coding=utf-8

from bs4 import BeautifulSoup
from urllib2 import urlopen
from time import sleep
import json

BASE_URL = 'http://www.althingi.is'

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def get_profile_links(section_url):
    soup = make_soup(section_url)
    profile_links = []
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
      profile_links.append(BASE_URL + row.findAll('a')[0]['href'])
    return profile_links

def get_profile(profile_url):
    soup = make_soup(profile_url)
    # The name is always in the h1 tag
    name = soup.find("h1").string
    # Get the person div to narrow down the scraping area
    person = soup.find("div", {'class': 'person'})

    # The following items are all in try/catches, as not all peeps have them
    try:
      # Image url
      image_url = BASE_URL + person.find("img")["src"]
    except:
      image_url = None
    
    # More narrowing down the scraping area
    office_ul = person.find('ul', {'class': 'office'})

    try:
      office = office_ul.find('strong', text=u'Embætti:').parent.get_text().split(': ')[1]
    except:
      office = ""
    try:
      district = office_ul.find('strong', text=u'Kjördæmi:').parent.get_text().split(': ')[1]
    except:
      district = ""
    try:
      party = office_ul.find('strong', text=u'Þingflokkur:').parent.get_text().split(': ')[1]
    except:
      party = ""
    try:
      # Some trickery required to assemble email address
      p = person.find('ul', {'class': 'first'}).get_text()
      email = p.split('\'')[1] + '@' + p.split('\'')[3]
    except:
      email = ""
    try:
      phone = person.find('a', {'class': 'tel'}).get_text()
    except:
      phone = ""
    try:
      # Some have more than one website
      all_a = person.find('ul', {'class': 'second'}).find_all('a')
      sites = []
      for a in all_a:
        sites.append(a['href'])
    except:
      sites = []
    try:
      twitter = person.find('a', {'class': 'twitter'})['href']
    except:
      twitter = ""
    try:
      facebook = person.find('a', {'class': 'facebook'})['href']
    except:
      facebook = ""
    return {"name": name,
            "image_url": image_url,
            "althing_url": profile_url,
            "office": office,
            "district": district,
            "party": party,
            "email": email,
            "phone": phone,
            "sites": sites,
            "twitter": twitter,
            "facebook": facebook
            }

if __name__ == '__main__':
    scrape_url = 'http://www.althingi.is/thingmenn/thingmenn/sitjandi-adal--og-varathingmenn'
    thingmenn_links = get_profile_links(scrape_url)
    data = [] # a list to store our dictionaries
    for thingmadur in thingmenn_links:
        person = get_profile(thingmadur)
        data.append(person)
    
    f = open('thingmenn.json', 'w')
    # Let's make this json pretty
    f.write(json.dumps(data, sort_keys=True, indent=4))
    f.close

    print "All dumped and ready"