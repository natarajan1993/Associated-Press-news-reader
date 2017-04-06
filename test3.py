import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

global df

def tester():
    r = requests.get("http://hosted.ap.org/dynamic/external/search.hosted.ap.org/wireCoreTool/Search?SITE=AP&SECTION=HOME"
                     "&TEMPLATE=DEFAULT&query=trump")
    soup = BeautifulSoup(r.content,'lxml')
    all_links = []
    all_heads = []
    ah = []
    al = []
    all_heads_raw = soup.find_all('span', {'class': 'latestnews'})
    for a_tag in soup.find_all('a', href=True):
        if a_tag['href'].startswith('/dynamic/stories/'):
            all_links.append('hosted.ap.org'+a_tag['href'])
    for heads in all_heads_raw:
        all_heads.append(heads.get_text())
    links_heads = zip(all_heads,all_links)
    # df = pd.DataFrame(data=links_heads,columns=['Headlines','Links'],index=range(0,len(links_heads)))
    # iterator = iter(df['Headlines'])

    # for head,link in links_heads:
    #    ah.append(head)
    #    al.append(link)

    return all_heads,all_links

ah,al = tester()
print(ah)
print(al)

# df2 = tester()
# print(df2)

# print(df.head())
