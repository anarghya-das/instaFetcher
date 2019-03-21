# Insta Fetcher 

A modern bot which can download any/all public instagram posts. If you want to download all your posts to have a backup,
or just download posts from a particular year, this is the tool you need to use. It can even download individual posts as well. 
Curious about how you would try it out? Read the steps below.

## Instructions to run Insta Fectcher 

1. Fire up your Terminal

2. CLone this repository

```
git clone https://github.com/anarghya-das/instaFetcher.git
```

3. After cloning, change your working directory to this repository 

```
cd instaFetcher
```

4. Install all the packages in the requirements.txt (Make sure you have python and pip installed and set in your **PATH**)

```python
pip install -r requirements.txt or pip3 install -r requirements.txt
```

5. Download the [chrome driver](http://chromedriver.chromium.org/downloads) and add it to your **PATH**

6. Make sure you have google chrome or any other chromium based browser installed as well.

7. Now you can either run the python file directly by giving the proper inputs (shown below)

```python
python3 private.py or python private.py
```

8. Or you could run the flask server and access the website on your **localhost**


```python
python3 main.py or python main.py
```

## Examples of Usage

Open the **private.py** file. Scroll towards the end where you'll find the following section:

```python
# * Example Usage

# name="USERNAME of the account to scrape posts" 
# year="YEAR TO USE AS A FILTER"
# linkToPost="https://www.instagram.com/p/BvPUab_gBwf/" 
# ! If target account is private, enter the details of the account which is following it.
# AUTH_EMAIL="USERNAME OR EMAIL"
# AUTH_PASS="PASSWORD"

# downloadWithLink(linkToPost) # * Downloads the post in the specified link of the post
# downloadAll(name,AUTH_EMAIL,AUTH_PASS) # * Downloads all the posts uploaded by the given user (name)
# donwloadWithFilter(name,year,AUTH_EMAIL,AUTH_PASS) # * Downloads all the posts with the given year
```

For the first usage example, uncomment the linkToPost variable (line 238) and downloadWithLink() function (line 243).
Run the file by following the step no. 7 as mentioned above.

Here's an example showing the steps:

![demo](https://github.com/anarghya-das/instaFetcher/blob/master/examples/downloadWithLink.gif)
