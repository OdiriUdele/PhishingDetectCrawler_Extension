from datetime import datetime
from urllib.parse import urlencode, urlparse, urlunparse
from googleapiclient.discovery import build

import whois
from bs4 import BeautifulSoup
import requests
import time
import dns.resolver
import regex as re
import urllib


#################################################################################################################################
#               Domain registration age 
#################################################################################################################################

def domain_registration_length(domain):
    try:
        res = whois.query(domain)
        expiration_date = res.expiration_date
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        # Some domains do not have expiration dates. The application should not raise an error if this is the case.
        if expiration_date:
            if type(expiration_date) == list:
                expiration_date = min(expiration_date)
            return abs((expiration_date - today).days)
        else:
            return 0
    except Exception as e:
        print("domain_registration_length err")
        print(e)
        return -1


#################################################################################################################################
#               Domain recognized by WHOIS
#################################################################################################################################


def whois_registered_domain(domain):
    try:
        hostname = whois.query(domain).name

        if type(hostname) == list:
            for host in hostname:
                if re.search(host.lower(), domain):
                    return 0
            return 1
        else:
            # print(re.search(hostname.lower(), domain))
            if re.search(hostname.lower(), domain):
                return 0
            else:
                return 1
    except Exception as e:
        print("whois_registered_domain err")
        print(e)
        return 1


#################################################################################################################################
#               Unable to get web traffic (Page Rank)
#################################################################################################################################

def web_traffic(short_url):
    try:
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + short_url).read(),
                             "xml").find("REACH")['RANK']
    except Exception as e:
        print("web_traffic error")
        print(e)
        return 0
    return int(rank)


#################################################################################################################################
#               Domain age of a url
#################################################################################################################################

def domain_age(domain):
    try:
        res = whois.query(domain)
        creation_date = res.creation_date
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        # Some domains do not have expiration dates. The application should not raise an error if this is the case.
        if creation_date:
            if type(creation_date) == list:
                creation_date = min(creation_date)
            return abs((creation_date - today).days)
        else:
            return 0
    except Exception as e:
        print("domain_age err")
        print(e)
        return -1


#################################################################################################################################
#               Google index
#################################################################################################################################

def google_index(api_key, cx, url):
    api_key = "AIzaSyA_nfbhPR_lQalRSetg4zZPt4ge8RU6GaI"
    cx = "332899deff05744fb"
    parsed = urlparse(url)
    url2 = url

    if (parsed.scheme == 'http'):
        parsed_url = parsed._replace(scheme='https')
        url2 = urlunparse(parsed_url)

    query = f"site:{url}"
    service = build("customsearch", "v1", developerKey=api_key)
    try:
        result = service.cse().list(q=query, cx=cx).execute()

        # Check if the target URL is present in the search results
        for item in result.get("items", []):
            if url in item.get("link", "") or url2 in item.get("link", ""):
                print("indexed")
                return 0

        return 1
    except AttributeError as e:
        print("google_index error")
        print(e)
        return 1


#################################################################################################################################
#               DNSRecord  expiration length
#################################################################################################################################

def dns_record(domain):
    try:
        nameservers = dns.resolver.resolve(domain, 'NS')

        if len(nameservers) > 0:
            return 0
        else:
            return 1
    except:
        return 1


#################################################################################################################################
#               Page Rank from OPR
#################################################################################################################################


def page_rank(key, domain):
    url = 'https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D=' + domain
    try:
        request = requests.get(url, headers={'API-OPR': key})
        result = request.json()
        result = result['response'][0]['page_rank_integer']
        if result:
            return result
        else:
            return 0
    except:
        return -1
