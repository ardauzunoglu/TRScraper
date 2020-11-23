import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

film = input("İncelemelerin Çekileceği Film: ")
dosya_adi = input("Oluşturulacak Excel dosyasının adı: ")
dosya_adi = dosya_adi + ".xlsx"
review_texts = []
review_useful = []
review_not_useful = []
review_scores = []
member_name_texts = []
date_texts = []
scrape_useful = True
scrape_scores = True
scrape_member_name = True
scrape_date = True

path = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(path)

time.sleep(1)
driver.get("http://www.beyazperde.com")
time.sleep(1)

driver.maximize_window()

time.sleep(1)

search = driver.find_element_by_class_name("header-search-input")
search.send_keys(film)

time.sleep(1)

auto_complete = driver.find_element_by_class_name("autocomplete-result-title")
auto_complete.click()

time.sleep(1)

member_reviews = driver.find_element_by_link_text("Üye Eleştirileri")
member_reviews.click()

time.sleep(1)

try:
    close_banner = driver.find_element_by_id("creativeClose")
    close_banner.click()

except:
    pass

time.sleep(1)

review_count = driver.find_element_by_class_name("titlebar-title.titlebar-title-md")
review_count = review_count.text
review_count = review_count.replace(" kullanıcı eleştirisi","")
review_count = int(review_count)

if review_count % 20 == 0:
    review_page_count = review_count // 20
else:
    review_page_count = (review_count // 20) + 1

constant_url = driver.current_url
l = 1
while l <= review_page_count:
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    match = False

    while match == False:
        lastCount = lenOfPage
        time.sleep(1)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

    reviews = driver.find_elements_by_class_name("review-card-content")
    for review in reviews:
        review = review.text
        review_texts.append(review)

    usefuls = driver.find_elements_by_class_name("reviews-users-comment-useful")
    for useful_unp in usefuls:
        useful_unp = useful_unp.text
        useful_unp = useful_unp.split()
        useful = useful_unp[0][0]
        not_useful = useful_unp[0][1]
        review_useful.append(useful)
        review_not_useful.append(not_useful)

    scores = driver.find_elements_by_class_name("stareval-note")
    for score in scores:
        score = score.text
        score = score.replace(",0","")
        review_scores.append(score)

    member_names = driver.find_elements_by_class_name("review-card-user-infos.cf")
    for member_name in member_names:
        member_name = member_name.text
        seperation = member_name.index("\n")
        member_name = member_name[:seperation]
        member_name_texts.append(member_name)

    dates = driver.find_elements_by_class_name("review-card-meta-date")
    for date in dates:
        date = date.text
        date = date.split()
        date = date[:3]
        date = " ".join(date)
        date_texts.append(date)

    l += 1
    url = constant_url + "?page=" + str(l)
    driver.get(url)

driver.close()

df = pd.DataFrame({"İncelemeler":review_texts})

if scrape_useful:
    df["İncelemeyi Yararlı Bulanlar"] = review_useful
    df["İncelemeyi Yararlı Bulmayanlar"] = review_not_useful

if scrape_scores:
    review_scores = review_scores[:len(review_texts)]
    df["İnceleme Puanları"] = review_scores

if scrape_member_name:
    df["İncelemeyi Yayınlayan Kişi"] = member_name_texts

if scrape_date:
    df["İncelemenin Yayınlanma Tarihi"] = date_texts

df.to_excel(dosya_adi, header = True, index = False)

x = "Çektiğiniz veriler "+ dosya_adi + " adlı excel dosyasına kaydedildi."
print(x)
    