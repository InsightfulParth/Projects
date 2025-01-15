import requests
import bs4
r = requests.get("https://www.aidtm.ac.in/-/media/Project/AdaniInstitute/Admission/Admission%20Policy%202025",'utf-8')
f = open('C:\\Users\\admin\\Desktop\\policy.pdf','wb')
f.write(r.content)
f.close()
