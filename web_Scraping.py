#gerekli kütüphaneleri import ettik
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import openpyxl as xl
# Siteye girerken izin almak için headers  tanımladık
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
# Tarayıcıyı başlat
driver = webdriver.Chrome()  # Tarayıcıya göre değişebilir (örneğin, Firefox veya Edge)


baseurl="https://www.evdeeczane.com"
# Sayfanın URL'sini girdik.
url = "https://www.evdeeczane.com/kategori/gunes-bakim-urunleri"
# Web sayfasını aç
driver.get(url)
content=driver.page_source
soup=BeautifulSoup(content,'html.parser')
time.sleep(1)
#BeautifulSoup kütüphanesi kullarak ürünlerin ismini siteden find_all komutu ile kullandık.
names=soup.find_all("div",attrs={"class":"showcase-title"})
#Verilerin tutulması için hepsi için ayrı ayrı dizi tanımladık.
namelist=[]
pricelist=[]
commentlist=[]
productlinks=[]
brandlist=[]
number_of_comment_list=[]
#Ürün isimlerini çektik
for name in names:
    title=name.find("a").text
    namelist.append(title)
#print(namelist)
#Burada diğer sayfaya geçmek için Selenium kütüphanesini kullandık.
next_page_button=soup.find("div",attrs={"class":"paginate-right paginate-active"})
#Ana url ile diğer sayfanın url'sini birleştirerek sayfaların linklerini çektik.
for a in next_page_button.find_all("a",href=True):
    next_page_link=baseurl+a['href']
    #print(next_page_link)
#Ürünlerin fiyatlarını çektik
prices=soup.find_all("div",attrs={"class":"showcase-price-new"})
for price in prices:
    pricelist.append(price.text)
products = soup.find_all('div',class_="showcase-image")
#Ürünlerin linklerini çektik.
for item in products:
    for link in item.find_all('a',href=True):
        productlinks.append(baseurl+link['href'])
#For döngüsü kullanarak ürünlerin içerisinde dolaşarak yorum ,yorum sayısı ve marka modelleri çektik
for links in productlinks:
        r = requests.get(links, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        comments = soup.find_all("div", class_="product-detail-comments-list")
        brands=soup.find_all("div",class_="showcase-brand")
        number_of_comments=soup.find("div",class_="product-comments-container")
        #marka model
        for brand in brands:
            brandlist.append(brand.text)
            #yorum
        for comment in comments:
            # print(b.text)
            commentlist.append(comment.text)
            #yorum sayısı
        for num in number_of_comments.find_all("a",href=True):
            number_of_comment_list.append(num.text)



#Selenium kütüphanesi kullanarak While döngüsü aracılığıyla sayfalarda dolaşarak ek bilgileri çektik.
"""c=0
while c<5:
    driver.get(next_page_link)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    names = soup.find_all("div", attrs={"class": "showcase-title"})
    products = soup.find_all('div', class_="showcase-image")
    for name in names:
        title = name.find("a").text
        namelist.append(title)
    prices = soup.find_all("div", attrs={"class": "showcase-price-new"})
    for price in prices:
        pricelist.append(price.text)
    for item in products:
        for link in item.find_all('a', href=True):
            productlinks.append(baseurl + link['href'])
    for links in productlinks:
        r = requests.get(links, headers=headers)
        comment_soup = BeautifulSoup(r.content, 'html.parser')
        comments = comment_soup.find_all("div", class_="product-detail-comments-list")
        brands = comment_soup.find_all("div", class_="showcase-brand")
        for brand in brands:
            brandlist.append(brand.text)
        for comment in comments:
                commentlist.append(comment)
    for a in next_page_button.find_all("a", href=True):
        next_page_link = baseurl + a['href']
        print(next_page_link)

    c=c+1
"""
#bilgileri dizi içinde yazdırma
print(len(productlinks))
print(productlinks)
print(namelist)
print(pricelist)
print(commentlist)
print(brandlist)
#workbook oluşturma
workbook = xl.Workbook()

# Sayfa oluştur
sheet = workbook.active

# Başlık satırını ekleyin
sheet.append(["Ürün", "Fiyat","Link","marka","Yorum Sayısı"])

# Verileri Excel dosyasına ekleyin
for name, price,links,brands,nums in zip(namelist, pricelist,productlinks,brandlist,number_of_comment_list):
    sheet.append([name, price,links,brands,nums])

# Excel dosyasını kaydedin
workbook.save("urun_fiyat_listesi.xlsx")



