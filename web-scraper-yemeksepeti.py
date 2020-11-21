import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

dosya_adi = input("Oluşturulacak Excel dosyasının adı: ")
dosya_adi = dosya_adi + ".xlsx"
restoran_info = "İçel Mersin Tantuni"
username_info = "ardauzunogluarda@gmail.com"
password_info = "ardaardaarda1"
sehir = "eskisehir"
yorum_texts = []
author_texts = []
date_texts = []
speed_ratings = []
service_ratings = []
flavour_ratings = []
scrape_author = True
scrape_date = True
scrape_speed = True
scrape_service = True
scrape_flavour = True
path = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(path)

time.sleep(1)

url = "https://www.yemeksepeti.com/" + sehir
driver.get(url)
driver.maximize_window()

time.sleep(1)

username = driver.find_element_by_id("UserName")
username.send_keys(username_info)

password = driver.find_element_by_id("password")
password.send_keys(password_info)
password.send_keys(Keys.ENTER)

time.sleep(1)

address_area = driver.find_element_by_class_name("address-area")
address_area.click()

time.sleep(1)

search_box = driver.find_element_by_class_name("search-box")
search_box.send_keys(restoran_info)
search_box.send_keys(Keys.ENTER)

time.sleep(3)

restoran = driver.find_element_by_class_name("restaurantName")
restoran.click()

time.sleep(1)

yorumlar_section = driver.find_element_by_xpath("//*[@id='restaurantDetail']/div[2]/div[1]/ul/li[4]/a")
yorumlar_section.click()

time.sleep(1)

l = 1
yorum_uzunlugu = yorumlar_section.text
yorum_uzunlugu = yorum_uzunlugu.replace("Yorumlar", "")
yorum_uzunlugu = yorum_uzunlugu.replace("(","")
yorum_uzunlugu = yorum_uzunlugu.replace(")","")
yorum_uzunlugu = (int(yorum_uzunlugu) // 30) + 1

while l < yorum_uzunlugu:

    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    match = False

    while match == False:
        lastCount = lenOfPage
        time.sleep(1)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

    yorumlar = driver.find_elements_by_class_name("comment.row")
    for yorum in yorumlar:
        yorum = yorum.text  
        yorum = yorum.replace("\n", " ")
        yorum = yorum.split()

        if "." in yorum[0]:
            yorum = yorum[1:]
        else:
            pass
            
        yorum = " ".join(yorum)
        yorum_texts.append(yorum)

    authors = driver.find_elements_by_class_name("userName")
    for author in authors:
        author = author.text
        author_texts.append(author)

    dates = driver.find_elements_by_class_name("commentDate")
    for date in dates:
        date = date.text
        date_texts.append(date)

    speeds = driver.find_elements_by_class_name("speed")
    for speed in speeds:
        speed = speed.text
        speed = speed.replace("Hız: ", "")
        speed_ratings.append(speed)

    services = driver.find_elements_by_class_name("serving")
    for service in services:
        service = service.text
        service = service.replace("Servis: ", "")
        service_ratings.append(service)

    flavours = driver.find_elements_by_class_name("flavour")
    for flavour in flavours:
        flavour = flavour.text
        flavour = flavour.replace("Lezzet: ", "")
        flavour_ratings.append(flavour)

    l += 1
    next_page = driver.find_element_by_link_text(str(l))
    next_page.click()

driver.close()

if "Restoran Cevabı" in author_texts:
        degistirilecek_rating_indexleri = author_texts.index("Restoran Cevabı")
        speed_ratings.insert(degistirilecek_rating_indexleri, "Restoran Cevabı")
        service_ratings.insert(degistirilecek_rating_indexleri, "Restoran Cevabı")
        flavour_ratings.insert(degistirilecek_rating_indexleri, "Restoran Cevabı")
    
elif "Yemeksepeti" in author_texts:
    degistirilecek_rating_indexleri = author_texts.index("Yemeksepeti")
    speed_ratings.insert(degistirilecek_rating_indexleri, "Yemeksepeti")
    service_ratings.insert(degistirilecek_rating_indexleri, "Yemeksepeti")
    flavour_ratings.insert(degistirilecek_rating_indexleri, "Yemeksepeti")
    
else:
    pass

df = pd.DataFrame({"Yorumlar": yorum_texts})

if scrape_author:
    df["Müşteriler"] = author_texts

if scrape_date:
    df["Yorum Tarihi"] = date_texts

if scrape_speed:
    df["Hız Değerlendirmesi"] = speed_ratings

if scrape_service:
    df["Servis Değerlendirmesi"] = service_ratings

if scrape_flavour:
    df["Lezzet Değerlendirmesi"] = flavour_ratings

df.to_excel(dosya_adi, header = True, index = False)

x = "Çektiğiniz veriler "+ dosya_adi + " adlı excel dosyasına kaydedildi."
print(x)