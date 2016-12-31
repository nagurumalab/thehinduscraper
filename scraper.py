from pprint import pprint
import json
import requests
from newspaper import Article
from bs4 import BeautifulSoup
FRONT_PAGE = "http://www.thehindu.com/todays-paper"

def get_all_sections():
    front_page_soup = get_soup(FRONT_PAGE)
    all_a = front_page_soup.select("#subnav-tpbar-latest a")
    sections = [("Front Page", FRONT_PAGE)]
    for a in all_a:
        sections.append((a.text.strip().title(), a['href']))
    return sections

def get_article(link):
    art = Article(link)
    art.download()
    art.parse()
    print "Got article - ", art.title
    article = dict(
        title=art.title,
        text=art.text,
        image=art.top_image,
        authors=art.authors,
        link=art.url
    )
    return article

def get_articles(page_soup):
    articles = []
    for section in page_soup.select(".tpaper-container section"):
        section_articles = []
        sec_heading = section.select("h2")
        section_title = ''
        if sec_heading:
            section_title = sec_heading[0].text.strip().title()
        for article in section.select(".section-container li a"):
            art_title = article.text.strip()
            art_link = article['href']
            art = get_article(art_link)
            section_articles.append(art)
        articles.append((section_title, section_articles))
    return articles

def get_soup(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content)
    return soup

def main():
    sections = get_all_sections()
    all_articles = []
    for sec, sec_link in sections:
        print "Getting Section - %s (%s)" % (sec, sec_link)
        sec_soup = get_soup(sec_link)
        sec_articles = get_articles(sec_soup)
        all_articles.append((sec, sec_articles))
    json.dump(all_articles, open("today.json", "w"))

if __name__ == "__main__":
    main()
