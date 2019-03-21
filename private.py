from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from zipfile import ZipFile 
from datetime import datetime
import os, time, shutil, requests, json

SCROLL_PAUSE_TIME = 2

def filterYear(year,jstr):
    jsobObject=json.loads(jstr)
    dString=jsobObject['uploadDate']
    uploadTime=datetime.strptime(dString,'%Y-%m-%dT%H:%M:%S')
    y=datetime.strptime(year,'%Y')
    return uploadTime.year==y.year


def downloadHelper(fileName, url):
    folder="all/"
    if not os.path.isdir(folder):
        os.mkdir(folder)
    response = requests.get(url, stream=True)
    with open(folder+fileName, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


def zip(files):
    with ZipFile('all/Pics.zip','w') as zip:
        for f in files:
            zip.write(f)
            os.remove(f)        


def downloadVideo(driver):
    downloadedVids=[]
    fname=""
    videoSource=driver.find_elements_by_xpath("//video[@class='tWeCl']")
    if not videoSource:
        return False
    vs=videoSource[0].get_attribute('src')
    fname=vs[vs.rfind('/')+1:vs.find('?')]
    if videoSource not in downloadedVids:
        downloadHelper(fname,vs)
        downloadedVids.append(videoSource)
    return fname


def downloadPicture(driver): 
    downloadedPics=[]
    fNames=[]
    fname=""
    images=driver.find_elements_by_xpath("//div[@class='KL4Bh']")
    if not images:
        return False
    multi=driver.find_elements_by_xpath("//button[@class='  _6CZji']")
    if multi:
        while multi:
            for img in images:
                if img not in downloadedPics:
                    src=img.find_element_by_tag_name('img').get_attribute('src')
                    fname=src[src.rfind('/')+1:src.find('?')]
                    downloadHelper(fname,src)
                    fNames.append(fname)
                    downloadedPics.append(img)
            multi[0].click()
            multi=driver.find_elements_by_xpath("//button[@class='  _6CZji']")
            images=driver.find_elements_by_xpath("//div[@class='KL4Bh']")
        # zip(fNames)
    else:
        src=images[0].find_element_by_tag_name('img').get_attribute('src')
        fname=src[src.rfind('/')+1:src.find('?')]
        downloadHelper(fname,src)
    return fname


def openlink(driver,link):
    script='window.open("'+link+'");'
    driver.execute_script(script)
    driver.switch_to.window(driver.window_handles[1])
    Text=driver.find_elements_by_xpath("//script[@type='application/ld+json']")[0].get_attribute('text')
    return Text


def addDiv(driver,divs,doneDivs,fyear=""):
    for div in divs:
        if div not in doneDivs:
            posts=div.find_elements_by_xpath("div[@class='v1Nh3 kIKUG  _bz0w']")
            for post in posts:
                a=post.find_element_by_tag_name('a')
                multiple=a.find_elements_by_xpath("div[@class='u7YqG']")
                if not multiple or multiple and multiple[0].find_element_by_css_selector('span').get_attribute("aria-label") =='Carousel':
                    link=a.get_attribute("href")
                    jText=openlink(driver,link)
                    if fyear != "" and not filterYear(fyear,jText):
                        return False
                    # download photos
                    downloadPicture(driver)
                else:
                    link=a.get_attribute("href")
                    jText=openlink(driver,link)
                    if fyear != "" and not filterYear(fyear,jText):
                        driver.close()
                        return False
                    # download videos
                    downloadVideo(driver)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            doneDivs.append(div)
    return True


def scroll(driver,doneDivs,extract=False,fyear=""):
        # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    if extract:
        divs=driver.find_elements_by_xpath("//div[@class='Nnq7C weEfm']")
        res=addDiv(driver,divs,doneDivs,fyear)
    while True and res:
    # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if extract:
            divs=driver.find_elements_by_xpath("//div[@class='Nnq7C weEfm']")
            res=addDiv(driver,divs,doneDivs,fyear)
        # Wait to load page
        # time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    driver.close()
    

def login(driver,em="",pas=""):
    link=driver.find_elements_by_xpath("//a[@class='hUQXy']")[0].get_attribute('href')
    driver.get(link)
    if em == "" or pas == "":
        driver.close()
        raise Exception("User is private, please provide login details!")
        
    print("Logging into the account..")

    email=driver.find_elements_by_xpath("//input[@class='_2hvTZ pexuQ zyHYP']")[0]
    password=driver.find_elements_by_xpath("//input[@class='_2hvTZ pexuQ zyHYP']")[1]    
    email.send_keys(em)
    password.send_keys(pas)
    driver.execute_script('document.getElementsByClassName("_0mzm- sqdOP  L3NKy       ")[0].click()')
    # TODO: Check if login is successful 
    print("Login Successful!")
    time.sleep(2)
    print("Redirecting to target user...",end=" ")


def setup(username):
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    driver=webdriver.Chrome(options=options)
    domain = "https://www.instagram.com"
    user ='/'+username
    driver.get(domain+user)
    res=driver.find_elements_by_xpath("//div[@class='Nd_Rl _2z6nI']")
    return (driver,res,domain,user)


def downloadAll(username,email="",password=""):
    start=time.time()
    doneDivs=[]
    driver,res,domain, user=setup(username)

    if res:
        login(driver,email,password)
        driver.get(domain+user)
        print("Done!")

    print("Collecting Post Links and Downloading...",end=" ")
    scroll(driver,doneDivs,True)
    print("Done! ",end=" ")
    end=time.time()
    print(str(len(doneDivs)*3)+" Posts Scrapped.")
    print("All Done!")
    seconds = end-start
    minutes = seconds / 60
    seconds = seconds % 60
    t="{:0>2} minutes:{:05.2f} seconds".format(int(minutes),seconds)
    print("Time Taken: "+t)


def donwloadWithFilter(name,year,email="",password=""):
    start=time.time()
    doneDivs=[]
    driver,res,domain,user=setup(name)    

    if res:
        login(driver,email,password)
        driver.get(domain+user)
        print("Done!")

    scroll(driver,doneDivs,True,year)
    end=time.time()
    seconds = end-start
    minutes = seconds / 60
    seconds = seconds % 60
    t="{:0>2} minutes:{:05.2f} seconds".format(int(minutes),seconds)
    print("Time Taken: "+t)


def downloadWithLink(link):
    print("started")
    start=time.time()  
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    driver=webdriver.Chrome(options=options)
    driver.get(link)
    f2=downloadPicture(driver)
    f=""
    if  f2 == "": 
        f=downloadVideo(driver)
    driver.close()
    end=time.time()
    seconds = end-start
    minutes = seconds // 60
    seconds = seconds % 60
    t="{:0>2} minutes:{:05.2f} seconds".format(int(minutes),seconds)
    print("Time Taken: "+t)
    if f != "":
        return "/download/"+f
    else:
        return "/download/"+f2


# * Example Usage

# name="USERNAME of the account to scrape posts" 
# year="YEAR TO USE AS A FILTER"
# ! If target account is private, enter the details of the account which is following it.
# AUTH_EMAIL="USERNAME OR EMAIL"
# AUTH_PASS="PASSWORD"

# downloadWithLink("https://www.instagram.com/p/BvOOD9yl4mM/") # * Downloads the post in the specified link of the post
# downloadAll(name,AUTH_EMAIL,AUTH_PASS) # * Downloads all the posts uploaded by the given user (name)
# donwloadWithFilter(name,year,AUTH_EMAIL,AUTH_PASS) # * Downloads all the posts with the given year

# TODO: MAKE IT ASYNC TO IMPROVE COMPLETE PROFILE DOWNLOAD TIME