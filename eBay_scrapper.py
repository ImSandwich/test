import urllib.request
from bs4 import BeautifulSoup
import pickle

uClient = urllib.request.urlopen("https://www.ebay.com/v/allcategories")
content = uClient.read()
uClient.close()
count = 0
categories = {}
soup = BeautifulSoup(content, "html.parser")
sub_categories = soup.findAll("li",{"class":"sub-category"})
for i in sub_categories:
    count += 1
    sub_category = (i.text.split("-")[0]).strip()
    main_category = (i.text.split("-")[1]).strip()
    if (main_category not in categories.keys()):
        categories[main_category] = []
    categories[main_category].append(sub_category)

print(count)
