
import requests
import bs4
a = requests.get("https://en.wikipedia.org/wiki/MS_Dhoni")
s = bs4.BeautifulSoup(a.text,"lxml")
print(s.select('img')[15]['src'])

# add above ink with 'https://'
i=requests.get("https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Mahendra_Singh_Dhoni_batting.JPG/220px-Mahendra_Singh_Dhoni_batting.JPG")
f = open('C:\\Users\\admin\\Desktop\\my_computer_image.jpg','wb')
f.write(i.content)
f.close()
