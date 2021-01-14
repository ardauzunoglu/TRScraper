import requests
import pandas as pd
from bs4 import BeautifulSoup

review_list = []

def get_soup(url):
    r = requests.get(url, params={"wait":"2"})
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def get_reviews(soup):
    reviews = soup.find_all("div", {"data-hook":"review"})
    try:
        for review in reviews:
            review = {
                "Yorum":review.find("span", {"data-hook":"review-body"}).text.replace("\n", ""),
                "Yorumun Beğeni Sayısı":review.find("span", {"data-hook":"helpful-vote-statement"}).text.split()[0].replace("Bir", "1"),
                "Yorumun Başlığı":review.find("a", {"data-hook":"review-title"}).text.replace("\n", ""),
                "Yorum Yazan Müşteri":review.find("span", {"class":"a-profile-name"}).text.replace("\n", ""),
                "Yorumun Yazıldığı Tarih":" ".join(review.find("span", {"data-hook":"review-date"}).text.split()[1:4]),
            }
            review_list.append(review)
    except:
        pass

def list_to_excel(list):
    df = pd.DataFrame(list)
    df.to_excel("amazon_bs4.xlsx", header = True, index = False)
    print("Excele kaydedildi.")