from selenium import webdriver
from bs4 import BeautifulSoup
import requests, shutil


def download(fileName, url):
    response = requests.get(url, stream=True)
    with open("insta\\"+fileName, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

def goToImage(link,d,domain):
    d.get(domain+link)
    html=d.page_source
    soup = BeautifulSoup(html,"lxml")
    imgs=soup.find('span').find_all(class_="KL4Bh")
    pLinks=[]
    for i in imgs:
        pLinks.append(i.find('img')['src'])
    return pLinks

def goToVideo(link,d,domain):
    d.get(domain+link)
    html=d.page_source
    soup = BeautifulSoup(html,"lxml")
    vLink=soup.find(class_="tWeCl")['src']
    return vLink

def getImages(d,domain):
    html=d.page_source
    soup = BeautifulSoup(html,"lxml")   
    rows=soup.find('span').find_all(class_="Nnq7C weEfm")
    count=1
    vCount=1
    # print("downloading "+str(pics)+" pictures...")
    for row in rows:
        elems=row.find_all(class_="v1Nh3 kIKUG _bz0w")
        for e in elems:
            a=e.find('a')
            link=a['href']
            divs=a.contents
            if len(divs) > 1:
                label=divs[1].find("span")['aria-label']
            if len(divs) == 1 or label == 'Carousel':
                print("downloading art"+str(count)+"...",end=" ")
                imgLinks=goToImage(link,d,domain)
                for l in imgLinks:
                    download("art"+str(count)+".png",l)
                    print("done")
                    count+=1
            else:
                print("downloading video"+str(vCount)+"...",end=" ")
                download("video"+str(vCount)+".mp4",goToVideo(link,d,domain))
                print("done")
                vCount+=1
    print('All downloaded')

# driver=webdriver.Chrome()
# domain = "https://www.instagram.com"
# user ='/'+"narendramodi"

# driver.get(domain+user)
# getImages(driver,domain)

