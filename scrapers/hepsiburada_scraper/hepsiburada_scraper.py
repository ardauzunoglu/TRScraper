import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys

def hepsiburada_scrape():
    def initialize():
        def preference(scrape_input):
                while (scrape_input.lower() != "y") or (scrape_input.lower() != "n"):
                    if scrape_input.lower() == "y":
                        output = True
                        break

                    elif scrape_input.lower() == "n":
                        output = False
                        break

                    else:
                        print("Geçersiz yanıt.")
                        scrape_input = input("İncelemenin aldığı beğeni sayısı çekilsin mi(y/n): ") 

                return output

        print("""
            ---------------------------------------------------------
            -         Hepsiburada Scraper'a hoş geldiniz!           -
            -         Geliştirici: Arda Uzunoğlu                    -
            ---------------------------------------------------------
        """)

        global product_name, file, delay, review_texts, review_useful, review_not_useful, customer_name_texts, customer_province_texts, customer_age_texts, date_texts, scrape_useful, scrape_customer_name, scrape_customer_province, scrape_customer_age, scrape_date, path

        product_name = input("Değerlendirmelerin çekileceği ürün adı: ")
        file = input("Oluşturulacak Excel dosyasının adı: ")
        file = file + ".xlsx"
        delay = int(input("Bekleme süresi: "))

        review_texts = []
        review_useful = []
        review_not_useful = []
        customer_name_texts = []
        customer_province_texts = []
        customer_age_texts = []
        date_texts = []

        scrape_useful_input = input("İncelemenin aldığı beğeni sayısı çekilsin mi(y/n): ")
        scrape_useful = preference(scrape_useful_input)

        scrape_customer_name_input = input("Müşteri isimleri çekilsin mi(y/n): ")
        scrape_customer_name = preference(scrape_customer_name_input)

        scrape_customer_province_input = input("Müşteri konumları çekilsin mi(y/n): ")
        scrape_customer_province = preference(scrape_customer_province_input)

        scrape_customer_age_input = input("Müşteri yaşları çekilsin mi(y/n): ")
        scrape_customer_age = preference(scrape_customer_age_input)

        scrape_date_input = input("İnceleme tarihleri çekilsin mi(y/n): ")
        scrape_date = preference(scrape_date_input)
        
        path = "BURAYA CHROMEDRIVER KONUMUNU GİRİNİZ"

    def scrape():
        try:
            print("Chromedriver'a erişiliyor...")
            driver = webdriver.Chrome(path)
            time.sleep(delay)
            print("Chromedriver'a erişildi.")

        except WebDriverException:
            print("Chromedriver kullanılamıyor.")
            sys.exit()

        try: 
            print("Hepsiburada adresine gidiliyor...")
            driver.get("https://www.hepsiburada.com")
            time.sleep(delay)
            driver.maximize_window()
            time.sleep(delay)
            print("Hepsiburada adresine gidildi.")

        except:
            print("Hepsiburada'ya erişilemiyor.")
            sys.exit()

        try:
            print("Ürün aranıyor...")
            arama_bari = driver.find_element_by_class_name("desktopOldAutosuggestTheme-input")
            arama_bari.send_keys(product_name)
            arama_bari.send_keys(Keys.ENTER)
            time.sleep(delay)

            urun = driver.find_element_by_class_name("search-item")
            urun.click()
            time.sleep(delay)
            print("Ürün bulundu.")
            
        except NoSuchElementException:
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

        except NoSuchElementException:
            print("İnceleme bulunamadı.")
            sys.exit()

        try:
            index_of_question_mark = constant_url.index("?")
            constant_url = constant_url[:index_of_question_mark]

        except NoSuchElementException:
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

        length_list = [review_texts, review_useful, review_not_useful, date_texts, customer_name_texts, customer_age_texts, customer_province_texts]
        limit = map(len, length_list)
        limit = min(list(limit))
        limit -= 1
        
        review_texts_fin = review_texts[:limit]
        df = pd.DataFrame({"Değerlendirme: ":review_texts_fin})

        if scrape_useful:
            review_useful_fin = review_useful[:limit]
            review_not_useful_fin = review_not_useful[:limit]
            df["Değerlendirmeyi Yararlı Bulanlar"] = review_useful_fin
            df["Değerlendirmeyi Yararlı Bulmayanlar"] = review_not_useful_fin

        if scrape_date:
            date_texts_fin = date_texts[:limit]
            df["Değerlendirme Tarihi:"] = date_texts_fin

        if scrape_customer_name:
            customer_name_texts_fin = customer_name_texts[:limit]
            df["Müşterinin Adı Soyadı"] = customer_name_texts_fin

        if scrape_customer_age:
            customer_age_texts_fin = customer_age_texts[:limit]
            df["Müşterinin Yaşı"] = customer_age_texts_fin

        if scrape_customer_province:
            customer_province_texts_fin = customer_province_texts[:limit]
            df["Müşterinin Konumu"] = customer_province_texts_fin

        df.to_excel(file, header = True, index = False)

        x = "Çektiğiniz veriler "+ file + " adlı excel dosyasına kaydedildi."
        print(x)

        print("""
            --------------------------------------------------------------------------
            -  Projeden memnun kaldıysanız Github üzerinden yıldızlamayı unutmayın.  -
            -  Github Hesabım: ardauzunoglu                                          -
            --------------------------------------------------------------------------
        """)

        time.sleep(3)

    initialize()
    scrape()

if __name__ == "__main__":
    hepsiburada_scrape()