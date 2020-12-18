import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def initialize():

    print("""
        ---------------------------------------------------------
        -         Hepsiburada Scraper'a hoş geldiniz!           -
        -         Geliştirici: Arda Uzunoğlu                    -
        ---------------------------------------------------------
    """)

    global urun_adi, dosya_adi, delay, review_texts, review_useful, review_not_useful, customer_name_texts, customer_province_texts, customer_age_texts, date_texts, scrape_useful, scrape_customer_name, scrape_customer_province, scrape_customer_age, scrape_date, path

    urun_adi = input("Değerlendirmelerin çekileceği ürün adı: ")
    dosya_adi = input("Oluşturulacak Excel dosyasının adı: ")
    dosya_adi = dosya_adi + ".xlsx"
    delay = int(input("Bekleme süresi: "))

    review_texts = []
    review_useful = []
    review_not_useful = []
    customer_name_texts = []
    customer_province_texts = []
    customer_age_texts = []
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

    scrape_customer_province_input = input("Müşteri konumları çekilsin mi(y/n): ")
    while (scrape_customer_province_input.lower() != "y") or (scrape_customer_province_input.lower() != "n"):
        if scrape_customer_province_input.lower() == "y":
            scrape_customer_province = True
            break

        elif scrape_customer_province_input.lower() == "n":
            scrape_customer_province = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_customer_province_input = input("Müşteri konumları çekilsin mi(y/n): ")
            print("\n")

    scrape_customer_age_input = input("Müşteri yaşları çekilsin mi(y/n): ")
    while (scrape_customer_age_input.lower() != "y") or (scrape_customer_age_input.lower() != "n"):
        if scrape_customer_age_input.lower() == "y":
            scrape_customer_age = True
            break

        elif scrape_customer_age_input.lower() == "n":
            scrape_customer_age = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_customer_age_input = input("Müşteri yaşları çekilsin mi(y/n): ")
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
        driver.get("https://www.hepsiburada.com")
        time.sleep(delay)
        driver.maximize_window()
        time.sleep(delay)

    except:
        print("Hepsiburada'ya erişilemiyor.")
        sys.exit()

    try:
        arama_bari = driver.find_element_by_class_name("desktopOldAutosuggestTheme-input")
        arama_bari.send_keys(urun_adi)
        arama_bari.send_keys(Keys.ENTER)
        time.sleep(delay)
        urun = driver.find_element_by_class_name("search-item")
        urun.click()
        time.sleep(delay)

    except:
        print("Ürün bulunamadı.")
        sys.exit()

    try:
        review_count = driver.find_element_by_id("productReviewsTab").text
        review_count = review_count.replace("Değerlendirmeler ", "")
        review_count = review_count.replace("(","")
        review_count = review_count.replace(")","")
        review_count = int(review_count)
        if review_count % 30 == 0:
            review_page_count = review_count // 10

        else:
            review_page_count = (review_count // 10) + 1

        constant_url = driver.current_url

    except:
        print("İnceleme bulunamadı.")
        sys.exit()

    try:
        index_of_question_mark = constant_url.index("?")
        constant_url = constant_url[:index_of_question_mark]

    except:
        pass

    i = 1
    while i <= review_page_count:

        url = constant_url + "-yorumlari?sayfa=" + str(i)
        driver.get(url)

        print("Veriler çekiliyor...")
        print("Sayfa: " + str(i))

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
    kisa = [len(review_texts), len(review_useful), len(review_not_useful), len(date_texts), len(customer_name_texts), len(customer_age_texts), len(customer_province_texts)]
    kisa = min(kisa)
    kisa -= 1
    
    review_texts_fin = review_texts[:kisa]
    df = pd.DataFrame({"Değerlendirme: ":review_texts_fin})

    if scrape_useful:
        review_useful_fin = review_useful[:kisa]
        review_not_useful_fin = review_not_useful[:kisa]
        df["Değerlendirmeyi Yararlı Bulanlar"] = review_useful_fin
        df["Değerlendirmeyi Yararlı Bulmayanlar"] = review_not_useful_fin

    if scrape_date:
        date_texts_fin = date_texts[:kisa]
        df["Değerlendirme Tarihi:"] = date_texts_fin

    if scrape_customer_name:
        customer_name_texts_fin = customer_name_texts[:kisa]
        df["Müşterinin Adı Soyadı"] = customer_name_texts_fin

    if scrape_customer_age:
        customer_age_texts_fin = customer_age_texts[:kisa]
        df["Müşterinin Yaşı"] = customer_age_texts_fin

    if scrape_customer_province:
        customer_province_texts_fin = customer_province_texts[:kisa]
        df["Müşterinin Konumu"] = customer_province_texts_fin

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