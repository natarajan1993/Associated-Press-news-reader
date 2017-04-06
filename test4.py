from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import glob
#

# def scrape(word):
#     full_list = []
#     ap = 'http://hosted.ap.org/dynamic/external/search.hosted.ap.org/wireCoreTool/Search?SITE=AP&SECTION=HOME' \
#          '&TEMPLATE=DEFAULT&query='
#
#     page = urlopen(ap + word)
#
#     soup = BeautifulSoup(page, 'lxml')
#
#     all_heads = soup.find_all('span', {'class': 'latestnews'})
#     for heads in all_heads:
#         full_list.append(heads.get_text())
#     return full_list[:]
#
# lines = []
# with open(r'C:\Users\Natarajan\PycharmProjects\AP_scraper\docs\topics.txt') as file:
#     for line in file:
#         line = line.strip()
#         lines.append(line)
# t1 = [scrape(lines[0])] # A separate list for each of the top 3 headlines from each topic searched
# t2 = [scrape(lines[1])]
# t3 = [scrape(lines[2])]
# t4 = [scrape(lines[3])]
# t5 = [scrape(lines[4])]
# print(t1[0][:5]+t2[0][:5])

# def clear_contents(filename):
#     open(filename, 'w').close()
# #
ap = ['http://hosted.ap.org/dynamic/stories/M/ML_SYRIA_THE_LATEST?SITE=AP&SECTION=HOME&TEMPLATE=DEFAULT',
      'http://hosted.ap.org/dynamic/stories/F/FINANCIAL_MARKETS?SITE=AP&SECTION=HOME&TEMPLATE=DEFAULT',
      'http://hosted.ap.org/dynamic/stories/U/US_SENATE_AIR_FORCE_SECRETARY?SITE=AP&SECTION=HOME&TEMPLATE=DEFAULT']

def return_full_news_string(ap):
    i = 0
    # for i in range(len(ap)):
    full_list = []
    print(ap)
    page = urlopen(ap)

    soup = BeautifulSoup(page, 'lxml')

    all_heads = soup.find_all('p', {'class': 'ap-story-p'})
    for heads in all_heads:
        full_list.append(heads.get_text())
    full_list = full_list[0:len(full_list)-1]
    # a = ' '.join(full_list)

    # file =  open(r'C:\Users\Natarajan\PycharmProjects\AP_scraper\news_temp.txt','w')
    # file.write(a)
    return full_list
everything = []
for i in ap:
    everything.append(return_full_news_string(i))
print(everything)
#
# def update_recommendations(headlines_list):
#     clear_contents(r'C:\Users\Natarajan\PycharmProjects\AP_scraper\docs\test.txt')
#     with open(r'C:\Users\Natarajan\PycharmProjects\AP_scraper\docs\test.txt','w') as file:
#         file.writelines("\n".join(headlines_list))
#
# update_recommendations(['d','e','f'])

# def get_document_filenames(document_path=r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp'):
#     return [os.path.join(document_path, each)
#             for each in os.listdir(document_path)]

# path = r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp'
# filenames = next(os.walk(path))[2]
# print(filenames)
# x = [f for f in os.listdir(r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp')]
# print(x)
# import os
# from fnmatch import fnmatch
#
# root = r'C:\Users\Natarajan\PycharmProjects\AP_scraper\temp'
# pattern = "*.txt"
#
# for path, subdirs, files in os.walk(root):
#     for name in files:
#         if fnmatch(name, pattern):
#             print(os.path.join(path, name))