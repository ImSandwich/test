from gensim.models import Word2Vec
from googlesearch import search
from nltk import word_tokenize
from nltk.corpus import stopwords
import urllib.request
from bs4 import BeautifulSoup
import pickle

categories = pickle.load(open("eBay_categories.pkl","rb"))
model = pickle.load(open("model.pkl", "rb"))
training = pickle.load(open("training.pkl", "rb"))
nn = pickle.load(open("neuralnetwork.pkl","rb"))

sub_categories = {}

s = set(stopwords.words("english"))

keys_array = []
#form the probability chart
for key in training.keys():
    sub_categories[key] = 0
    keys_array.append(key)


u_inp = input()
response = search(u_inp, tld="com", num=3, start=0, stop=1, pause=1)
for result in response:
    try:
        uContent = urllib.request.urlopen(result)
        html = uContent.read()
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.findAll("p")
        for paragraph in paragraphs:
            sentence = word_tokenize(paragraph.text)
            filtered_sentence = [w for w in sentence if w not in s]
            for w in filtered_sentence:
                try:
                        sub_categories[keys_array[nn.predict([model.wv[w]])[0]]]+=1
                except:
                    pass
        uContent.close()
    except:
        pass

ranking = [(k, sub_categories[k]) for k in sub_categories.keys()]
ranking = sorted(ranking, key = lambda x: x[1], reverse=True)
total_score = 0
if (total_score==0):
    print("No match")
else:
    for i in ranking: total_score += i[1]
    ranking = [(x[0], "{:0.2f}".format(x[1]/total_score * 100)+"%") for x in ranking]
    print(ranking)