import requests
from bs4 import BeautifulSoup

weapon="M4A4"

url="https://csgostash.com/weapon/"+weapon
r=requests.get(url)

c=r.content
soup=BeautifulSoup(c,"html.parser")

span=soup.find_all("div",{"class":"price"})
x=span[0].text.replace("₹","").replace("\n","").replace("-","").replace(",","")

l=[]
j=-1

names=soup.find_all("h3")

for i in range(len(names)-2):
    d={}
    span=soup.find_all("div",{"class":"price"})
    j=j+1
    normal=str(span[j].text.replace("₹","").replace("\n","").replace("-","").replace(",","").replace("'",""))
    j=j+1
    stattrak=span[j].text.replace("₹","").replace("\n","").replace("-","").replace(",","")
    if (len(stattrak)==1): #in case no stattrak is present
        stattrak="N/A"

    #To convert the string price to integer prices, lowest to highest grade
    norm_price=[int(normal) for normal in str.split(normal) if normal.isdigit()]
    stat_price=[int(stattrak) for stattrak in str.split(stattrak) if stattrak.isdigit()]
    name=names[i].text
    d["Name"]=name
    d["Battle Scarred"]=norm_price[0]
    d["Factory New"]=norm_price[1]
    try:  #in case no stattrak is present
        d["StatTrak Battle Scarred"]=stat_price[0]
    except:
        d["StatTrak Battle Scarred"]="N/A"
    try:
        d["StatTrak Factory New"]=stat_price[1]
    except:
        d["StatTrak Factory New"]="N/A"
    l.append(d)

s=str(span[j].text.replace("₹","").replace("\n","").replace("-","").replace(",","").replace("'",""))
x=[int(s) for s in str.split(s) if s.isdigit()]

import pandas
df=pandas.DataFrame(l)

#Rearranging columns and sorting ascending according to battle scarred price, and setting names as index
df = df[['Name', 'Battle Scarred', 'Factory New', 'StatTrak Battle Scarred','StatTrak Factory New']]
df=df.set_index("Name")
df=df.sort_values(["Battle Scarred"])

df.to_csv("csgo"+weapon+".csv")
