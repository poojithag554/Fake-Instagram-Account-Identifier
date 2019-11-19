# -*- coding: utf-8 -*-
"""app.py
Flask webapp
"""

from flask import Flask, request, render_template
from model import FakeAccClassifier
import numpy as np
from selenium import webdriver

app = Flask(__name__)

classifier = FakeAccClassifier()

# What happens when the form is submitted
@app.route('/', methods=['POST'])
def make_prediction():
    username = request.form['username']

    # Extract data using Selenium web scraping
    data = get_data(username)

    # Handling invalid usernames
    if data is None:
        return render_template('page.html', generated_text='Invalid username: @' + username)

    # Get prediction from classifier
    prediction = classifier.predict(data)

    # Update front-end with result
    return render_template('page.html', generated_text='@' + username + ': ' + prediction)


# Data extraction from web scraping
def get_data(un):
    # Initialize Chrome and open the user account webpage
    driver = webdriver.Chrome('./chromedriver.exe')
    URL = 'http://instagram.com/' + un
    driver.get(URL)

    try:
        # Invalid username handling
        valid = driver.find_elements_by_xpath('/html/body/div/div[1]/div/div/h2')[0].text
        if valid == "Sorry, this page isn't available.":
            driver.close()
            print("Invalid username")
            return None
    except:
        # Data extraction
        data = np.zeros(11)

        # 0. profile picture
        data[0] = 1
        try:
            pic = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/div/div/div/button/img')
        except:
            data[0] = 0

        # 1. nums/length username
        un_nums = 0
        for c in un:
            if c.isdigit():
                un_nums += 1
        data[1] = un_nums / len(un)

        # 2. full name words
        try:
            name = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/h1')[0].text
            words = name.split(' ')
            data[2] = len(words)
        except:
            data[2] = 0

        # 3. nums/length name
        if data[2] == 0:
            data[3] == 1 # vacuous truth type of thing?
        else:
            name_nums = 0
            for c in name:
                if c.isdigit():
                    name_nums += 1
            data[3] = name_nums / len(name)

        # 4. name == username
        if name == un:
            data[4] == 1
        else:
            data[4] == 0

        # 5. desc length
        try:
            desc = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/span')[0].text
            data[5] = len(desc)
        except:
            data[5] = 0

        # 6. external url
        url = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/a')
        if len(url) == 0:
            data[6] = 0
        else:
            data[6] = 1

        # 7. private?
        private = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/article[2]/div/div/h2')
        if len(private) == 0:
            data[7] = 0  # is not private
        else:
            data[7] = 1

        # 8. posts
        posts = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/a/span')[
            0].text
        posts = posts.replace(',', '')
        data[8] = int(posts)

        # 9. followers
        follows = \
        driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')[
            0].text
        follows = follows.replace(',', '')
        data[9] = int(follows)

        # 10. following
        following = \
        driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span')[
            0].text
        following = following.replace(',', '')
        data[10] = int(following)

        # Close Chrome
        driver.close()
        return data


# Initialize web page
@app.route('/', methods=['GET'])
def load():
    return render_template('page.html', generated_text="")

if __name__ == '__main__':
    app.run(debug=True)
