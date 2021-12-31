#  Asim Arain
#  Wanna Talk to the Internet? Stage 5

links = []

import requests
import string
from bs4 import BeautifulSoup
import os

page_number = int(input())
desired_article = input()

def nature_web_srcaper(url_article_page, desired_article, path_name):
    if not os.path.exists(path_name):
        os.mkdir(path_name)
    url_article_page_soup = BeautifulSoup(requests.get(url_article_page).content, 'html.parser')
    
    #  find the articles
    url_page_articles = url_article_page_soup.find_all('article')
    for article in url_page_articles:
        article_type = article.find('span', "c-meta__type").text
        if article_type == desired_article:
            links.append(article.find('a').get('href'))
    
    #  Now the links array has the links of the desired artciles
    for anchor in links:
        desired_anchor_url = ("https://www.nature.com" + anchor)
        desired_content = BeautifulSoup(requests.get(desired_anchor_url).content, 'html.parser')
        desired_title = desired_content.find('title').text.strip()
    
        #  Clean up the title in the desired format
        for char in desired_title:
            if char in string.punctuation:
                desired_title = desired_title.replace(char, "")
            elif char == " ":
                desired_title = desired_title.replace(" ", "_")
    
        #  Obtain the article
        desired_article_body = desired_content.find('div', {'class': 'c-article-body u-clearfix'})
        desired_file = open(os.path.join(path_name, desired_title +".txt"), 'wb')
        desired_file.write(bytes(desired_article_body.text, 'utf-8'))
        desired_file.close()


for page in range(page_number):
    # Course required that the path name be capital "P" in Page, but doesn't matter in URL
    path_name = f"Page_{page + 1}"
    url_article_page = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={page + 1}"
    nature_web_srcaper(url_article_page, desired_article, path_name)
    
#  In the future, it is best to create a check for all the paths existing before giving the "thumbs-up"
print("Saved all articles.")
    

