from bs4 import BeautifulSoup
import requests

domain = "https://www.instagram.com/"
user = "swg_ghosh"

res = requests.get(
    domain+user, headers={"User-Agent": "Default"})
res.encoding = "utf-8"
data = res.text
soup = BeautifulSoup(data, features='html.parser')
details=soup.find('meta', attrs={'property': 'og:description'})['content'].split()
image=soup.find('meta', attrs={'property': 'og:image'})['content']
followers=details[0]
following=details[2]
posts=details[4]
username=details[len(details)-1]
print(username[1:-1])
print("Followers: "+str(followers))
print("Following: "+str(following))
print("Posts: "+str(posts))
print("Image: "+image)
