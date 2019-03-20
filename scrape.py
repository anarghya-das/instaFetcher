from bs4 import BeautifulSoup
import requests
import shutil

domain = "http://www.sportslogos.net/"
LaLiga = "teams/list_by_league/130/Spanish_La_Liga/Spanish_La_Liga/logos/"
Bundesliga = "teams/list_by_league/132/German_Bundesliga/German_Liga/logos/"


def func(link):
    url = domain+link
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features='html.parser')
    return soup.find(class_="logoWall").find_all('li')


def download(fileName, url):
    response = requests.get(url, stream=True)
    with open("LaLiga\\"+fileName, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


allPictures = []
con = func(LaLiga)
count = 1
for val in con:
    url2 = val.find('a')['href']
    con2 = func(url2)
    for value in con2:
        url3 = domain+value.find('a')['href']
        r = requests.get(url3)
        data = r.text
        soup = BeautifulSoup(data, features='html.parser')
        final = soup.find(class_="mainLogo").find('img')['src']
        allPictures.append(final)
        print("Scrapped "+str(count)+"....", end=" ")
        count += 1

print()
print("Downloading...")
c = 1
for link in allPictures:
    name = "team"+str(c)+".png"
    download(name, link)
    c += 1

print("Done!")
