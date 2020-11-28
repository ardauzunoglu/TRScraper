import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

kitap = input("İncelemelerin Çekileceği Kitap Adı: ")
dosya_adi = input("Oluşturulacak Excel dosyasının adı: ")
dosya_adi = dosya_adi + ".xlsx"
review_texts = []
review_useful = []
review_not_useful = []
author_texts = []
date_texts = []
scrape_useful = True
scrape_author = True
scrape_date = True
path = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(path)

time.sleep(1)

driver.get("https://www.kitapyurdu.com")
driver.maximize_window()

time.sleep(1)

search = driver.find_element_by_id("search-input")
search.send_keys(kitap)
search.send_keys(Keys.ENTER)

time.sleep(1)

try:
    close_notification = driver.find_element_by_class_name("opt-in-disallow-button")
    close_notification.click()
except:
    pass

time.sleep(1)

product = driver.find_element_by_link_text(kitap)
product.click()

time.sleep(1)
reviewsTab = driver.find_element_by_class_name("pr__htabs-review-text")
reviewsTab.click()

l = 1
review_length = reviewsTab.text.replace("Yorumlar","")
review_length = int(review_length)

if review_length % 5 == 0:
    review_length = review_length // 5
else:
    review_length = (review_length // 5) + 1

while l < review_length:
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    match = False

    while match == False:
        lastCount = lenOfPage
        time.sleep(1)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

    reviews = driver.find_elements_by_class_name("review-text")
    for review in reviews:
        review = review.text
        review_texts.append(review)
    
    authors = driver.find_elements_by_xpath("//a[@class ='alt']//span[@itemprop='name']")
    for author in authors:
        author = author.text 
        author_texts.append(author)
    
    dates = driver.find_elements_by_class_name("review-date")
    for date in dates:
        date = date.text
        date_texts.append(date)

    usefuls = driver.find_elements_by_xpath("//div[@class ='agree']//span[@class='count']")
    for useful in usefuls:
        useful = useful.text
        review_useful.append(useful)

    not_usefuls = driver.find_elements_by_xpath("//div[@class ='disagree']//span[@class='count']")
    for not_useful in not_usefuls:
        not_useful = not_useful.text
        review_not_useful.append(not_useful)

    l += 1
    next_page = driver.find_element_by_link_text(str(l))
    next_page.click()

df = pd.DataFrame({"Yorumlar": review_texts})

if scrape_author:
    df["Müşteriler"] = author_texts

if scrape_date:
    df["İnceleme Tarihi"] = date_texts

if scrape_useful:
    df["İncelemeyi Yararlı Bulan Kişi Sayısı"] = review_useful
    df["İncelemeyi Yararlı Bulmayan Kişi Sayısı"] = review_not_useful

df.to_excel(dosya_adi, header = True, index = False)

x = "Çektiğiniz veriler "+ dosya_adi + " adlı excel dosyasına kaydedildi."
print(x)
