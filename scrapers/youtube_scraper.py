import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def youtube_scrape():
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
            -         Youtube Scraper'a hoş geldiniz!               -
            -         Geliştirici: Arda Uzunoğlu                    -
            ---------------------------------------------------------
        """)
        
        global url, file, delay, scrape_author, scrape_date, scrape_title, scrape_like, path

        url = input("Yorumların çekileceği Youtube videosunun bağlantısı: ")
        file = input("Oluşturulacak Excel dosyasının adı: ")
        file = file + ".xlsx"
        delay = int(input("Bekleme süresi: "))

        scrape_author_input = input("Kullanıcı isimleri çekilsin mi(y/n): ")
        scrape_author = preference(scrape_author_input)

        scrape_date_input = input("Yorum tarihleri çekilsin mi(y/n): ")
        scrape_date = preference(scrape_date_input)

        scrape_title_input = input("Video başlığı çekilsin mi(y/n): ")
        scrape_title = preference(scrape_title_input)
    
        scrape_like_input = input("Yorumun aldığı beğeni sayısı çekilsin mi(y/n): ")
        scrape_like = preference(scrape_like_input)

        path = "BURAYA CHROMEDRIVER KONUMUNU GİRİNİZ"

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

        driver.close()

        length_list = [comment_texts, author_texts, date_texts, like_texts, title_text]
        limit = map(len, length_list)
        limit = min(list(limit))
        limit -= 1

        comment_texts_fin = comment_texts[:limit]
        df = pd.DataFrame({"Yorumlar":comment_texts_fin})
        if scrape_author:
            author_texts_fin = author_texts[:limit]
            df["Kullanıcı"] = author_texts_fin

        if scrape_date:
            date_texts_fin = date_texts[:limit]
            df["Yorum Tarihi"] =  date_texts_fin
        
        if scrape_like:
            like_texts_fin = like_texts[:limit]
            df["Yorumun Aldığı Beğeni Sayısı"] =  like_texts_fin
        
        if scrape_title:
            title_text_fin = title_text[:limit]
            df["Video Başlığı"] = title_text_fin

        df.to_excel(file, header = True, index = False)
        x = "Çektiğiniz veriler " + file + " adlı excel dosyasına kaydedildi."
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
    youtube_scrape()