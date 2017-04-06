from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

def scrape(word):
    full_list = []
    ap = 'http://hosted.ap.org/dynamic/external/search.hosted.ap.org/wireCoreTool/Search?SITE=AP&SECTION=HOME&TEMPLATE=DEFAULT&query='

    page = urlopen(ap+word)

    soup = BeautifulSoup(page, 'lxml')

    all_heads = soup.find_all('span',{'class':'latestnews'})
    for heads in all_heads:
        full_list.append(heads.get_text())
    print(full_list[:])
    # for line in full_list[39:63]:
    #     return line

scrape('st+louis')
