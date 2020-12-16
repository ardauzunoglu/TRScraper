import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def initialize():

    print("""
        ---------------------------------------------------------
        -         Youtube Scraper'a hoş geldiniz!               -
        -         Geliştirici: Arda Uzunoğlu                    -
        ---------------------------------------------------------
    """)
    
    global url, dosya_adi, delay, scrape_authors, scrape_dates, scrape_title, scrape_likes, path

    url = input("Yorumların çekileceği Youtube videosunun bağlantısı: ")
    dosya_adi = input("Oluşturulacak Excel dosyasının adı: ")
    dosya_adi = dosya_adi + ".xlsx"
    delay = int(input("Bekleme süresi: "))

    scrape_author_input = input("Kullanıcı isimleri çekilsin mi(y/n): ")
    while (scrape_author_input.lower() != "y") or (scrape_author_input.lower() != "n"):
        if scrape_author_input.lower() == "y":
            scrape_authors = True
            break

        elif scrape_author_input.lower() == "n":
            scrape_authors = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_author_input = input("Kullanıcı isimleri çekilsin mi(y/n): ") 
            print("\n")

    scrape_dates_input = input("Yorum tarihleri çekilsin mi(y/n): ")
    while (scrape_dates_input.lower() != "y") or (scrape_dates_input.lower() != "n"):
        if scrape_dates_input.lower() == "y":
            scrape_dates = True
            break

        elif scrape_dates_input.lower() == "n":
            scrape_dates = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_dates_input = input("Yorum tarihleri çekilsin mi(y/n): ")
            print("\n")

    scrape_title_input = input("Video başlığı çekilsin mi(y/n): ")
    while (scrape_title_input.lower() != "y") or (scrape_title_input.lower() != "n"):
        if scrape_title_input.lower() == "y":
            scrape_title = True
            break

        elif scrape_title_input.lower() == "n":
            scrape_title = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_title_input = input("Video başlığı çekilsin mi(y/n): ")
            print("\n")

    scrape_likes_input = input("Yorumun aldığı beğeni sayısı çekilsin mi(y/n): ")
    while (scrape_likes_input.lower() != "y") or (scrape_likes_input.lower() != "n"):
        if scrape_likes_input.lower() == "y":
            scrape_likes = True
            break

        elif scrape_likes_input.lower() == "n":
            scrape_likes = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_likes_input = input("Yorumun aldığı beğeni sayısı çekilsin mi(y/n): ")
            print("\n")

    path = "C:\Program Files (x86)\chromedriver.exe"

def scrape():
    comment_texts = []
    author_texts = []
    date_texts = []
    title_text = []
    like_texts = []

    try:
        driver = webdriver.Chrome(path)
        time.sleep(delay)

    except:
        print("Chromedriver kullanılamıyor.")
        sys.exit()

    try: 
        driver.get(url)
        time.sleep(delay)
        driver.maximize_window()
        time.sleep(delay)

    except:
        print("Youtube'a erişilemiyor.")
        sys.exit()

    time.sleep(delay+2)
    comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    title = driver.find_element_by_class_name("title").text
    time.sleep(delay)

    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    time.sleep(delay+2)

    comment_count = driver.find_element_by_class_name("count-text.ytd-comments-header-renderer").text
    comment_count = comment_count.replace(" Yorum","")
    comment_count = comment_count.replace(".","")
    comment_count = int(comment_count)

    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    l = 1
    while l <= comment_count:
        try:
            comments = driver.find_elements_by_xpath("//*[@id='contents']/ytd-comment-thread-renderer")
            comment = comments[l-1]
            print("Veri çekiliyor...")
            print("Yorum: " + str(l))
            author = comment.find_element_by_id("author-text").text
            date = comment.find_element_by_class_name("published-time-text").text
            comment_text = comment.find_element_by_id("content-text").text
            likes = comment.find_element_by_id("vote-count-middle").text

            author_texts.append(author)
            date_texts.append(date)
            comment_texts.append(comment_text)
            like_texts.append(likes)
            title_text.append(title)

        except:
            break

        l += 1

    df = pd.DataFrame({"Yorumlar":comment_texts})
    if scrape_authors:
        df["Kullanıcı"] = author_texts

    if scrape_dates:
        df["Yorum Tarihi"] =  date_texts
    
    if scrape_likes:
        df["Yorumun Aldığı Beğeni Sayısı"] =  like_texts
       
    if scrape_title:
        df["Video Başlığı"] =  title_text

    df.to_excel(dosya_adi, header = True, index = False)
    x = "Çektiğiniz veriler " + dosya_adi + " adlı excel dosyasına kaydedildi."
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