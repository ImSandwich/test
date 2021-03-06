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
training_set = {}
#Find all relevant paragraphs, tokenize, generate word vec
count = 0
for key in categories.keys():
    for sub_category in categories[key]:
        training_set[sub_category] = []
        count+=1
        if (count % 100 == 0): pickle.dump(document, open("document.pkl", "wb"))
        print("Handling subcategory " + str(count))
        response = search(sub_category, tld="com", num=3, start=0, stop=1, pause=0)
        ind = 3
        try:
            result = next(response)
            uContent = urllib.request.urlopen(result)
            html = uContent.read()
            soup = BeautifulSoup(html, "html.parser")
            paragraphs = soup.findAll("p")
            for paragraph in paragraphs:
                sentence = word_tokenize(paragraph.text)
                filtered_sentence = [w.lower() for w in sentence if w not in s]
                document.append(filtered_sentence)
                training_set[sub_category].append(filtered_sentence)
            uContent.close()
            ind-=1
            if (ind == 0): continue
        except:
            pass


pickle.dump(document, open("document.pkl","wb"))
pickle.dump(training_set, open("training.pkl","wb"))
model = Word2Vec(document, size=150, window=10, min_count=2, workers=10)
pickle.dump(model, open("model.pkl","wb"))
#model.wv.most_similar(positive="Boat Parts")