import amazon_scraper as as 
from amazon_scraper import amazon_scraper
import beyazperde_scraper as bp
from beyazperde_scraper import beyazperde_scrape
import ciceksepeti_scraper as cs 
from ciceksepeti_scraper import ciceksepeti_scraper
import eksi_scraper as es
from eksi_scraper import eksisozluk_scrape
import gittigidiyor_scraper as gs 
from gittigidiyor_scraper import gittigidiyor_scrape
import hepsiburada_scraper as hb 
from hepsiburada_scraper import hepsiburada_scrape
import incehesap_scraper as is 
from incehesap_scraper import incehesap_scraper
import kitapyurdu_scraper as ky 
from kitapyurdu_scraper import kitapyurdu_scrape
import mediamarkt_scraper as ms 
from mediamarkt_scraper import mediamarkt_scraper
import n11_scraper as ns 
from n11_scraper import n11_scraper
import trendyol_scraper as ty 
from trendyol_scraper import trendyol_scrape
import yemeksepeti_scraper as ys 
from yemeksepeti_scraper import yemeksepeti_scrape
import youtube_scraper as yt
from youtube_scraper import youtube_scrape

choices = ["amazon", "beyazperde", "çiçeksepeti", "ekşi sözlük", "gittigidiyor", "hepsiburada", "incehesap", "kitapyurdu", "mediamarkt", "n11", "trendyol", "yemeksepeti", "youtube"]
libs = {"amazon":amazon_scraper, "beyazperde":beyazperde_scrape, "çiçeksepeti":ciceksepeti_scraper, "ekşi sözlük":eksisozluk_scrape, "hepsiburada":hepsiburada_scrape, "incehesap":incehesap_scraper, 
        "kitapyurdu":kitapyurdu_scrape, "mediamarkt":mediamarkt_scraper, "n11":n11_scraper, "trendyol":trendyol_scrape, "yemeksepeti":yemeksepeti_scrape, "youtube":youtube_scrape}

choice = input("Kullanacağınız scraper: ")
choice = choice.lower()

if choice in choices:
    scraper = libs[choice]
    scraper()
else:
    print("Geçersiz yanıt.")
    secenek = input("Kullanacağınız scraper: ")