import requests
import json
import requests
from rich import print
from bs4 import BeautifulSoup

print("Veille Cyber Securite : \n")

try:
    ### partie Scrap it-connect ###
    url = "https://www.it-connect.fr/actualites/actu-securite/"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    article_titles = soup.find_all("h2")

    #Check si requete precedente = requete
    with open("C:\API\cache.txt", "r") as file:
        old_articles = file.read()

    #Check for nouveau article
    if old_articles == str(article_titles):
        print ("[green]Pas de nouvel article.\n")
    else:
       #Prend uniquement le dernier article
       title = article_titles[0]
       #Vire les espaces vides
       titre = title.text[6:]

       print("[red]Nouvel article :\n")
       print(titre)

    #Save articles
    with open("C:\API\cache.txt", "w") as file:
        file.write(str(article_titles))
except:
    print("[red]Error scrap it-connect.\n")

### partie Scrap ANSII  ###
url = "https://www.cert.ssi.gouv.fr/alerte/"
response = requests.get(url)

soup2 = BeautifulSoup(response.content, "html.parser")

count_alert = 0
items_status = soup2.find_all(class_="item-status")
items_title = soup2.find_all(class_="item-title")
list_articles = []

#Recup les titres d'articles en fonction de en cours ou non
for status in items_status:
    if status.text == "Alerte en cours":
        #Osef des articles de mise a jour
        if "MàJ" not in items_title[count_alert].text:
            list_articles.append(((items_title[count_alert]).text)[:-1])
    count_alert = count_alert + 1

#Affiches les articles
if list_articles != []:
    print("[red]Alerte ANSII en cours :")
    for i in list_articles:
        print (i)
else:
    print ("[green]Aucune alerte ANSII en cours.")

#Partie CVE
url = "https://vuldb.com/?api"
payload = {"apikey": "f87caa578056f12a0b2491ab1f505258", "recent": "50"}

response = requests.post(url, data=payload)
data = response.json()
count = 0

#Get l'API et check si y'a des vulns en high
try:
    for vuln in data["result"]:
       if (vuln["vulnerability"]["risk"]["name"] == "high"):
           print("[red]CVE Critique : " + vuln["source"]["cve"]["id"] + " | " + vuln["entry"]["title"])
           count = count + 1

    if count == 0:
       print ("\n[green]Pas de nouvel CVE critique.")
except:
    print("[red]Plus de credit d'API.")
