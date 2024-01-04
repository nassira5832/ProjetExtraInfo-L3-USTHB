import requests
from bs4 import BeautifulSoup
import codecs

ListUrl = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def AvoirLesNoms(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    names = [li.text.strip() for li in soup.find_all('li', class_='even')]
    return names


def LesNoms(interval, port):
     tousLesNoms = []
     debut, fin = interval.split('-')
     A=ListUrl [ListUrl.index(debut):ListUrl.index(fin)+1]
     for i in A:
         url = f"{port}://www.vidal.fr/medicaments/gammes/liste-{i}.html"
         names = AvoirLesNoms(url)
         tousLesNoms.extend(names)
     return tousLesNoms
    

#-----------------------------------------------------------------------------------------#
# Écriture du dictionnaire dans le fichier .dic avec encodage UTF-16 LE BOM
def CreeDic (interval, port):

      tousLesNoms= LesNoms(interval,port)
      NomFichier = "subst.dic"
      with codecs.open(NomFichier, "w", encoding="utf-16le") as file:
           file.write('\ufeff')
           for name in tousLesNoms:
                 file.write(f"{name},.N+subst\n")
#----------------------------------------------------------------------------------------#
# donner la possibilité a l'utilisateur de donner l'interval des pages a traiter : 

arg1=input("veuillez donner l'interval de page a traiter sous form <premiere page>-<derniere page>  ")
while '-' not in arg1 :
     print ("erreur veuillez entrer l'interval correctement ")
     arg1=input("veuillez donner l'interval de page a traiter sous form <premiere page>-<derniere page>  ")
     
debut, fin = arg1.split('-')
while (debut not in ListUrl or fin not in ListUrl or ListUrl.index(debut) >= ListUrl.index(fin)):
          print ("erreur veuillez entrer l'interval correctement ")
          arg1=input("veuillez donner l'interval de page a traiter sous form <premiere page>-<derniere page>  ")
          while '-' not in arg1 :
             print ("erreur veuillez entrer l'interval correctement ")
             arg1=input("veuillez donner l'interval de page a traiter sous form <premiere page>-<derniere page>  ")
          debut, fin = arg1.split('-')
#------------------------------------------------------------------------------------------#
# donner la possibilité a l'utilisateur de donner le point  : 
arg2=input("donner le port d'accès (mettez 80 pour http ou 443 pour https)")
while arg2 not in ['80', '443'] : 
     print ("erreur veuillez mettre 80 pour http ou bien 443 pour https ")
if arg2=='80' : 
     arg2="http"
else:
     if arg2=='443':
          arg2="https"

#------------------
VoirLesNoms=LesNoms(arg1,arg2)
print(VoirLesNoms)
# creation du dictionnaire 
CreeDic(arg1,arg2)
#----------------------------------------------------------------------------------------# 
entites_par_lettre = {}
nombre_total_entites = 0

with codecs.open('subst.dic', 'r', encoding='utf-16le') as file:
     for x in file:
          ligne_striped = x.strip()
          entite = ligne_striped.split(',')[0]
          premiere_lettre = entite[0].upper()
          entites_par_lettre[premiere_lettre] = entites_par_lettre.get(premiere_lettre, 0) + 1
          nombre_total_entites += 1

with codecs.open('infos1.txt', 'w', encoding='UTF-8') as output_file:
    for lettre, nombre_entites in sorted(entites_par_lettre.items()):
        output_file.write(f"{lettre}: {nombre_entites} entités\n")

    output_file.write(f"Nombre total d'entités: {nombre_total_entites}")


