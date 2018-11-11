import urllib.request
from bs4 import BeautifulSoup
import pickle

uClient = urllib.request.urlopen("https://www.ebay.com/v/allcategories")
content = uClient.read()
uClient.close()

categories = {}
soup = BeautifulSoup(content, "html.parser")
sub_categories = soup.findAll("li",{"class":"sub-category"})
limit = 30
for i in sub_categories:
    limit-=1
    if (limit==0):
        break
    sub_category = (i.text.split("-")[0]).strip()
    main_category = (i.text.split("-")[1]).strip()
    if (main_category not in categories.keys()):
        categories[main_category] = []
    categories[main_category].append(sub_category)

print(categories)
pickle.dump(categories, open("eBay_categories.pkl","wb"))