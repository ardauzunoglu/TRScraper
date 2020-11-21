import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

urun_adi = "AvvaBisiklet Yaka Düz T-Shirt"
dosya_adi = input("Oluşturulacak Excel dosyasının adı: ")
dosya_adi = dosya_adi + ".xlsx"
review_texts = []
review_useful = []
customer_name_texts = []
date_texts = []
scrape_useful = True
scrape_customer_name = True
scrape_date = True

path = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(path)

time.sleep(1)
driver.get("https://www.trendyol.com")
time.sleep(1)

driver.maximize_window()

time.sleep(1)

arama_bari = driver.find_element_by_class_name("search-box")
arama_bari.send_keys(urun_adi)
arama_bari.send_keys(Keys.ENTER)

time.sleep(1)

urun = driver.find_element_by_class_name("prdct-desc-cntnr")
urun.click()

time.sleep(1)

url = driver.current_url
index_of_question_mark = url.index("?")
url = url[:index_of_question_mark]
url = url + "/yorumlar"
driver.get(url)

lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
match = False

while match == False:
    lastCount = lenOfPage
    time.sleep(1)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    if lastCount == lenOfPage:
        match = True

time.sleep(1)

reviews = driver.find_elements_by_class_name("rnr-com-tx")
for review in reviews:
    review = review.text
    review_texts.append(review)

usefuls = driver.find_elements_by_xpath("//*[@class='tooltip-wrp']//span[2]")
for useful in usefuls:
    useful = useful.text
    useful = useful.strip("()")
    review_useful.append(useful)

customers = driver.find_elements_by_xpath("//*[@class='rnr-com-bt']//span[@class = 'rnr-com-usr']")
for customer in customers:
    customer = customer.text
    customer = customer.replace("|","")
    customer = customer.split()

    customer_name = customer[-3:]
    customer_name = " ".join(customer_name)
    customer_name_texts.append(customer_name)

    date = customer[:-3]
    date = " ".join(date)
    date_texts.append(date)

driver.close()

df = pd.DataFrame({"Yorum": review_texts})

if scrape_useful:
    df["Yorum Beğeni Sayısı"] = review_useful

if scrape_customer_name:
    df["Yorum Yazan Müşteri"] = customer_name_texts

if scrape_date:
    df["Yorumun Yazıldığı Tarih"] = date_texts

df.to_excel(dosya_adi, header = True, index = False)

x = "Çektiğiniz veriler "+ dosya_adi + " adlı excel dosyasına kaydedildi."
print(x)