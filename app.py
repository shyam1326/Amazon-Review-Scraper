from flask import Flask, request, render_template, jsonify
from bs4 import BeautifulSoup
from urllib.request import urlopen



app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        searchstring = request.form['content'].replace(" ", "")
        try:
            amazon_url = "https://www.amazon.in/s?k=" + searchstring
            openurl = urlopen(amazon_url)
            amazonpage = openurl.read()
            openurl.close()
            amazon_html = BeautifulSoup(amazonpage, 'html.parser')
            bigbox = amazon_html.find_all('div', {'class': 'sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28'})
            firstbox = bigbox[0]
            product_link = 'https://www.amazon.in/'+ firstbox.div.a['href']
            product_open = urlopen(product_link)    # product_open = requests.get(product_link)
            product_open = product_open.read()
            product_html = BeautifulSoup(product_open, 'html.parser')
            commment_box = product_html.find_all('div', {'class': 'a-section review aok-relative'})


            reviews = []
            for i in commment_box:
                try:
                    name = i.find_all('span', {'class': 'a-profile-name'})[0].text
                except:
                    name = 'No name'

                try:
                    comment_head = i.find_all('a', {'data-hook' : 'review-title'})[0].find('span').text
                except:
                    comment_head = 'No comment heading'

                try:
                    ratings = i.find_all('a', {'class' : "a-link-normal"})[0].find('span').text[0:3]
                except:
                    ratings = 'No ratings'

                try:
                    comments = i.find_all('div', {'data-hook' : "review-collapsed"})[0].find('span').text
                except:
                    comments = 'No comments'

                dictionary = {"Product": searchstring, "Name": name, "Rating": ratings, "CommentHead": comment_head, "Comment": comments}
                reviews.append(dictionary)
            return render_template('results.html', reviews=reviews)
        except:
            return 'Something went wrong'





if __name__ == '__main__':
    app.run(port=8000, debug=True)
