import requests
import pandas as pd
import json
import tqdm

url_api = "https://geo.api.gouv.fr/communes"

r = requests.get(url_api)
content = r.json()

nom =[]
code=[]

for item in content:
    nom.append(item['nom'])
    code.append(item['code'])

data_df = pd.DataFrame({
    'Nom Commune': nom,
    'Code Commune': code
    })

print(data_df.shape)
# data_df.info()

# URL API
url_api_com = "https://geo.api.gouv.fr/communes?code=CODE&fields=code,centre,surface,contour,mairie,bbox,population,codeDepartement,departement,codeRegion,region,zone&format=geojson&geometry=contour"

# initialisation des listes
code_commune=[]
nom_commune=[]
nom_departement=[]
code_departement=[]
nom_region=[]
code_region=[]
zone=[]
population=[]
surface=[]
coordinate=[]
# récupération de la réponse, analyse et ajout des données dans les listes
for code_com in tqdm.tqdm(data_df['Code Commune'], desc="Traitement en cours", bar_format="{l_bar}{bar:20}{r_bar}"):
    c=requests.get(url_api_com.replace('CODE', str(code_com)))
    content_communes = c.json()
    features = content_communes['features'][0]
   
    try:
        code_commune.append(features['properties']['code'])
    except:
        code_commune.append("")
    try:
        nom_commune.append(features['properties']['nom'])
    except:
        nom_commune.append("")
    try:
        nom_departement.append(features['properties']['departement']['nom'])
    except:
        nom_departement.append("")
    try:
        code_departement.append(features['properties']['departement']['code'])
    except:
        code_departement.append("")
    try:
        nom_region.append(features['properties']['region']['nom'])
    except:
        nom_region.append("")
    try:
        code_region.append(features['properties']['region']['code'])
    except:
        code_region.append("")
    try:
        zone.append(features['properties']['zone'])
    except:
        zone.append("")
    try:
        population.append(features['properties']['population'])
    except:
        population.append(0)
    try:
        surface.append(features['properties']['surface'])
    except:
        surface.append(0)
    try:
        coordinate.append(features['geometry'])
    except:
        coordinate.append("")

# Création du Dataframe
df_communes=pd.DataFrame({
    'code_commune': code_commune,
    'nom_commune' : nom_commune,
    'code_departement' : code_departement,
    'nom_departement' : nom_departement,
    'code_region' : code_region,
    'nom_region' : nom_region,
    'zone' : zone,
    'population': population,
    'surface': surface,
    'geometry': coordinate
    })
# Enregistrement des données dans le fichier CSV
df_communes.to_csv('data_communes.csv',encoding='utf-8', index=False, index_label=False, mode='w' )