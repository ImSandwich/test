from gensim.models import Word2Vec
from googlesearch import search
from nltk import word_tokenize
from nltk.corpus import stopwords
import urllib.request
from bs4 import BeautifulSoup
import pickle

categories = pickle.load(open("eBay_categories.pkl","rb"))
s = set(stopwords.words("english"))
document = []
#Find all relevant paragraphs, tokenize, generate word vec
count = 0
for key in categories.keys():
    for sub_category in categories[key]:
        count+=1
        print("Handling subcategory " + str(count))
        response = search(sub_category, tld="com", num=3, start=0, stop=1, pause=1)
        for result in response:
            try:
                uContent = urllib.request.urlopen(result)
                html = uContent.read()
                soup = BeautifulSoup(html, "html.parser")
                paragraphs = soup.findAll("p")
                for paragraph in paragraphs:
                    sentence = word_tokenize(paragraph.text)
                    filtered_sentence = [w for w in sentence if w not in s]
                    if (sub_category not in filtered_sentence):
                        filtered_sentence.append(sub_category)
                    document.append(filtered_sentence)
                uContent.close()
            except:
                pass

model = Word2Vec(document, size=150, window=10, min_count=2, workers=10)
pickle.dump(model, open("model.pkl","wb"))
model.wv.most_similar(positive="Golf")