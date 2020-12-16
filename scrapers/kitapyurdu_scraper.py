import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def initialize():

    print("""
        ---------------------------------------------------------
        -         Kitapyurdu Scraper'a hoş geldiniz!            -
        -         Geliştirici: Arda Uzunoğlu                    -
        ---------------------------------------------------------
    """)

    global kitap, dosya_adi, delay, review_texts, review_useful, review_not_useful, author_texts, date_texts, scrape_useful, scrape_author, scrape_date, path

    kitap = input("İncelemelerin Çekileceği Kitap Adı: ")
    dosya_adi = input("Oluşturulacak Excel dosyasının adı: ")
    dosya_adi = dosya_adi + ".xlsx"
    delay = int(input("Bekleme süresi: "))

    review_texts = []
    review_useful = []
    review_not_useful = []
    author_texts = []
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

    scrape_author_input = input("Kullanıcı isimleri çekilsin mi(y/n): ")
    while (scrape_author_input.lower() != "y") or (scrape_author_input.lower() != "n"):
        if scrape_author_input.lower() == "y":
            scrape_author = True
            break

        elif scrape_author_input.lower() == "n":
            scrape_author = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_author_input = input("Kullanıcı isimleri çekilsin mi(y/n): ")
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

    path = "C:\Program Files (x86)\chromedriver.exe"

def scrape():
    try:
        driver = webdriver.Chrome(path)
        time.sleep(delay)

    except:
        print("Chromedriver kullanılamıyor.")
        sys.exit()

    try:
        driver.get("https://www.kitapyurdu.com")
        driver.maximize_window()
        time.sleep(delay)

    except:
        print("Kitapyurdu'na erişilemiyor.")
        sys.exit()

    try:
        search = driver.find_element_by_id("search-input")
        search.send_keys(kitap)
        search.send_keys(Keys.ENTER)

        time.sleep(delay)

        try:
            close_notification = driver.find_element_by_class_name("opt-in-disallow-button")
            close_notification.click()

        except:
            pass

        time.sleep(delay)

        product = driver.find_element_by_class_name("name.ellipsis")
        product.click()
        time.sleep(delay)

    except:
        print("Kitap bulunamadı.")
        sys.exit()

    try:
        reviewsTab = driver.find_element_by_class_name("pr__htabs-review-text")
        reviewsTab.click()
        time.sleep(delay)

    except:
        print("Kitap incelemeleri bulunamadı.")
        sys.exit()

    l = 1
    review_length = reviewsTab.text.replace("Yorumlar","")
    
    try:
        review_length = review_length.replace(".","")
        review_length = int(review_length)

    except:
        review_length = int(review_length)

    if review_length % 5 == 0:
        review_length = review_length // 5
    else:
        review_length = (review_length // 5) + 1

    while l <= review_length:

        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        match = False

        while match == False:
            lastCount = lenOfPage
            time.sleep(delay)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            if lastCount == lenOfPage:
                match = True

        print("Veriler çekiliyor...")
        print("Sayfa: " + str(l))

        try:
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

        except:
            time.sleep(delay)

        l += 1

        try: 
            next_page = driver.find_element_by_link_text(str(l))
            next_page.click()

        except:
            time.sleep(delay)

    kisa = min(len(author_texts), len(date_texts), len(review_useful), len(review_not_useful))
    kisa -= 1

    columns = [author_texts, date_texts, review_useful, review_not_useful]
    for column in columns:
        column = column[:kisa]

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
