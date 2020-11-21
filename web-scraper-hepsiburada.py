import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

urun_adi = input("Değerlendirmeleri çekeceğiniz ürün adı: ")
dosya_adi = input("Oluşturulacak Excel dosyasının adı: ")
dosya_adi = dosya_adi + ".xlsx"
review_texts = []
review_useful = []
review_not_useful = []
customer_name_texts = []
customer_province_texts = []
customer_age_texts = []
date_texts = []
scrape_useful = True
scrape_customer_name = True
scrape_customer_province = True
scrape_customer_age = True
scrape_date = True

path = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(path)

time.sleep(1)

driver.get("https://www.hepsiburada.com")

time.sleep(1)

driver.maximize_window()

time.sleep(1)

arama_bari = driver.find_element_by_class_name("desktopOldAutosuggestTheme-input")
arama_bari.send_keys(urun_adi)
arama_bari.send_keys(Keys.ENTER)

time.sleep(1)

urun = driver.find_element_by_class_name("search-item")
urun.click()

time.sleep(1)

review_count = driver.find_element_by_id("productReviewsTab").text
review_count = review_count.replace("Değerlendirmeler ", "")
review_count = review_count.replace("(","")
review_count = review_count.replace(")","")
review_count = int(review_count)
review_page_count = (review_count // 10) + 1

constant_url = driver.current_url
try:
    index_of_question_mark = constant_url.index("?")
    constant_url = constant_url[:index_of_question_mark]
except:
    pass

i = 1
while i <= review_page_count:
    url = constant_url + "-yorumlari?sayfa=" + str(i)
    driver.get(url)

    review_cards = driver.find_elements_by_xpath("//*[@id='hermes-voltran-comments']//div[@itemprop='review']")

    reviews = driver.find_elements_by_xpath("//*[@id='hermes-voltran-comments']//span[@itemprop='description']")
    for review in reviews:
        review = review.text
        review_texts.append(review)

    customer_names = driver.find_elements_by_xpath("//*[@id='hermes-voltran-comments']//span[@itemprop='author']")
    for customer_name in customer_names:
        customer_name = customer_name.text
        customer_name_texts.append(customer_name)

    customer_ages = driver.find_elements_by_xpath("//*[@class='hermes-ReviewCard-module-1-Wp3']//span[2]")
    for customer_age in customer_ages:
        customer_age = customer_age.text
        customer_age = customer_age.replace("(", "")
        customer_age = customer_age.replace(")", "")
        if customer_age == "":
            customer_age = "Boş"
        customer_age_texts.append(customer_age)

    customer_provinces = driver.find_elements_by_xpath("//*[@class='hermes-ReviewCard-module-1-Wp3']//span[3]")
    for customer_province in customer_provinces:
        customer_province = customer_province.text
        customer_province = customer_province.replace("-", "")
        customer_province = customer_province.replace(" ", "")
        customer_province_texts.append(customer_province)

    dates = driver.find_elements_by_xpath("//*[@id='hermes-voltran-comments']//span[@itemprop='datePublished']")
    for date in dates:
        date = date.text
        date = date.replace(",", "")
        date = date.split()
        day_abbr = ["Pts", "Sal", "Çar", "Per", "Cum", "Cts", "Paz"]
        day_conv = {
            "Pts":"Pazartesi",
            "Sal":"Salı",
            "Çar":"Çarşamba",
            "Per":"Perşembe",
            "Cum":"Cuma",
            "Cts":"Cumartesi",
            "Paz":"Pazar",
            "Pazartesi":"Pazartesi",
            "Salı":"Salı",
            "Çarşamba":"Çarşamba",
            "Perşembe":"Perşembe",
            "Cuma":"Cuma",
            "Cumartesi":"Cumartesi",
            "Pazar":"Pazar"
        }
        years = ["2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000"]
        if date[2] not in years:
            date.insert(2, "2020")
        date[-1] = day_conv[date[-1]]
        date = " ".join(date)
        date_texts.append(date)

    usefuls = driver.find_elements_by_xpath("//*[@id='hermes-voltran-comments']//button[@class='hermes-ReviewCard-module-1MoiF']")
    not_usefuls = driver.find_elements_by_xpath("//*[@id='hermes-voltran-comments']//button[@class='hermes-ReviewCard-module-39K0Y']")

    for useful in usefuls:
        useful = useful.text
        useful = useful.replace("Evet", "")
        useful = useful.replace("(", "")
        useful = useful.replace(")", "")
        review_useful.append(useful)
    
    for not_useful in not_usefuls:
        not_useful = not_useful.text
        not_useful = not_useful.replace("Hayır", "")
        not_useful = not_useful.replace("(", "")
        not_useful = not_useful.replace(")", "")
        review_not_useful.append(not_useful)

    while len(review_useful) < len(date_texts):
        review_useful.append("0")
        review_not_useful.append("0")

    while len(review_texts) < len(date_texts):
        review_texts.append("Boş")

    i += 1

driver.close()
print(len(review_texts))
print(len(review_useful))
print(len(review_not_useful))
print(len(date_texts))
print(len(customer_name_texts))
print(len(customer_age_texts))
print(len(customer_province_texts))
df = pd.DataFrame({"Değerlendirme: ":review_texts})

if scrape_useful:
    df["Değerlendirmeyi Yararlı Bulanlar"] = review_useful
    df["Değerlendirmeyi Yararlı Bulmayanlar"] = review_not_useful

if scrape_date:
    df["Değerlendirme Tarihi:"] = date_texts

if scrape_customer_name:
    df["Müşterinin Adı Soyadı"] = customer_name_texts

if scrape_customer_age:
    df["Müşterinin Yaşı"] = customer_age_texts

if scrape_customer_province:
    df["Müşterinin Konumu"] = customer_province_texts

df.to_excel(dosya_adi, header = True, index = False)

x = "Çektiğiniz veriler "+ dosya_adi + " adlı excel dosyasına kaydedildi."
print(x)