import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def initialize():

    print("""
        ---------------------------------------------------------
        -         Trendyol Scraper'a hoş geldiniz!              -
        -         Geliştirici: Arda Uzunoğlu                    -
        ---------------------------------------------------------
    """)


    global urun_adi, dosya_adi, delay, review_texts, review_useful, customer_name_texts, date_texts, scrape_useful, scrape_customer_name, scrape_date, path

    urun_adi = input("Yorumların çekileceği ürün adı: ")
    dosya_adi = input("Oluşturulacak Excel dosyasının adı: ")
    dosya_adi = dosya_adi + ".xlsx"
    delay = int(input("Bekleme süresi: "))

    review_texts = []
    review_useful = []
    customer_name_texts = []
    date_texts = []

    scrape_useful_input = input("İncelemenin aldığı beğeni sayısı çekilsin mi(y/n): ")
    while (scrape_useful_input.lower() != "y") or (scrape_useful_input.lower() != "n"):
        if scrape_useful_input.lower() == "y":
            scrape_useful = True
            break

        elif scrape_useful_input.lower() == "n":
            scrape_useful = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_useful_input = input("İncelemenin aldığı beğeni sayısı çekilsin mi(y/n): ") 
            print("\n")

    scrape_customer_name_input = input("Müşteri isimleri çekilsin mi(y/n): ")
    while (scrape_customer_name_input.lower() != "y") or (scrape_customer_name_input.lower() != "n"):
        if scrape_customer_name_input.lower() == "y":
            scrape_customer_name = True
            break

        elif scrape_customer_name_input.lower() == "n":
            scrape_customer_name = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_customer_name_input = input("Müşteri isimleri çekilsin mi(y/n): ")
            print("\n")

    scrape_date_input = input("İnceleme tarihleri çekilsin mi(y/n): ")
    while (scrape_date_input.lower() != "y") or (scrape_date_input.lower() != "n"):
        if scrape_date_input.lower() == "y":
            scrape_date = True
            break

        elif scrape_date_input.lower() == "n":
            scrape_date = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_date_input = input("İnceleme tarihleri çekilsin mi(y/n): ")
            print("\n")

    scrape_useful = True
    scrape_customer_name = True
    scrape_date = True

    path = "C:\Program Files (x86)\chromedriver.exe"

def scrape():
    try:
        driver = webdriver.Chrome(path)
        time.sleep(1)

    except:
        print("Chromedriver kullanılamıyor.")
        sys.exit()

    try:
        driver.get("https://www.trendyol.com")
        time.sleep(1)
        driver.maximize_window()
        time.sleep(1)

    except:
        print("Trendyola'a erişilemiyor.")
        sys.exit()

    try:
        arama_bari = driver.find_element_by_class_name("search-box")
        arama_bari.send_keys(urun_adi)
        arama_bari.send_keys(Keys.ENTER)
        time.sleep(1)

        urun = driver.find_element_by_class_name("prdct-desc-cntnr")
        urun.click()
        time.sleep(1)

    except:
        print("Ürün bulunamadı.")
        sys.exit()

    url = driver.current_url
    index_of_question_mark = url.index("?")
    url = url[:index_of_question_mark]
    url = url + "/yorumlar"
    driver.get(url)

    yorum_sayisi = driver.find_element_by_class_name("pr-rnr-sm-p-s")
    yorum_sayisi = yorum_sayisi.text
    yorum_sayisi = yorum_sayisi.replace("Değerlendirme", "")
    yorum_sayisi = yorum_sayisi.replace("Yorum", "")
    yorum_sayisi = yorum_sayisi.split()
    yorum_sayisi = int(yorum_sayisi[1])

    while len(review_texts) < yorum_sayisi:

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

            print("Veriler çekiliyor...")
            print("İnceleme: " + str(len(review_texts)))

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

    print("""
        --------------------------------------------------------------------------
        -  Projeden memnun kaldıysanız Github üzerinden yıldızlamayı unutmayın.  -
        -  Github Hesabım: ardauzunoglu                                          -
        --------------------------------------------------------------------------
    """)

    time.sleep(3)

if __name__ == "__main__":
    initialize()
    scrape()