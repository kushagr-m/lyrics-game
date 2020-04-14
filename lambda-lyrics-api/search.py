import json
import urllib
from urllib.parse import urlparse

import requests
import re # regex
from bs4 import BeautifulSoup

from make_response import make_response

def search(event, context):
    """
    Given an event of the form `{ "query": 'string to search' }` returns a list of dicts of type
        [{
            "path": '/lyrics/_artist_/_title_.html',
            "title": songtitle,
            "artist": songartist
        },...]
    """

    search_url = "https://search.azlyrics.com/search.php?q={}"
    query_encoded = urllib.parse.quote(event.get('query',''), safe='')

    request_url = search_url.format(query_encoded)
    print(request_url)

    r = requests.get(request_url)
    assert(r.status_code == 200)

    soup = BeautifulSoup(r.text, 'html.parser')

    returndata = []
    for tr in soup.find_all('tr'):
        try:
            a = tr.find('a')
            path = urlparse(a.get('href')).path
            d = {
                'path': path,
                'title': a.string,
                'artist': tr.find_all('b')[1].text
            }
            returndata.append(d)
        except:
            continue

    make_response(r.status_code, {
            "data": returndata
        })

if __name__ == "__main__":
    from pprint import pprint
    event = {
        "query": "American idiot"
    }
    pprint(json.loads(search(event, None).get('body')))
