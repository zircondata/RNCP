import requests
import pandas as pd
import tqdm

url_api = "https://api.insee.fr/metadonnees/V1/geo/communes?date=*&com=true"

headers={
        'Accept': 'application/json',
        'Authorization': 'Bearer 6c9d7ee0-b3b1-3ad1-be23-54a4a9f4b564'
        }

r = requests.get(url_api, headers=headers)
content = r.json()

code=[]
dateCreation=[]
dateSuppression=[]
intitule=[]
intituleComplet=[]
intituleSansArticle=[]
type_item=[]

for item in tqdm.tqdm(content, desc="Traitement en cours", bar_format="{l_bar}{bar:20}{r_bar}"):
    
    try:
        code.append(item['code'])
    except:
        code.append("")
    try:
        dateCreation.append(item['dateCreation'])
    except:
        dateCreation.append("")
    try:
        dateSuppression.append(item['dateSuppression'])
    except:
        dateSuppression.append("")
    try:
        intitule.append(item['intitule'])
    except:
        intitule.append("")
    try:
        intituleComplet.append(item['intituleComplet'])
    except:
        intituleComplet.append("")
    try:
        intituleSansArticle.append(item['intituleSansArticle'])
    except:
        intituleSansArticle.append("")
    try:
        type_item.append(item['type'])
    except:
        type_item.append("")
    
df_com_hist = pd.DataFrame({
                'code' : code,
                'dateCreation' : dateCreation,
                'dateSuppression' : dateSuppression,
                'intitule' : intitule,
                'intituleComplet' : intituleComplet,
                'intituleSansArticle' : intituleSansArticle,
                'type_item' : type_item
                })

df_com_hist.to_csv('data_com_hist.csv',encoding='utf-8', index=False, index_label=False, mode='w' )

print(df_com_hist.shape)

url_api_pop = "https://api.insee.fr/donnees-locales/V0.1/donnees/geo-IND_POPLEGALES@POPLEG"+"ANNEE"+"/COM-"+"CODE"+".all"

headers={
        'Accept': 'application/json',
        'Authorization': 'Bearer 7fff07c2-a6dc-3c05-817a-fedf447b9e93'
        }

code_com_pop=[]
nom_com_pop=[]
annee_mill=[]
annee_popleg=[]
popmun=[]
popcap=[]
poptot=[]

year_error=[]
code_com_error=[]
status=[]

years=[2020, 2019, 2018, 2017, 2016]
#years=[2020]
for year in years:
        for code_com in tqdm.tqdm(df_com_hist['code'], desc="Traitement en cours "+ str(year), bar_format="{l_bar}{bar:20}{r_bar}"):
                p=requests.get(url_api_pop.replace("ANNEE", str(year)).replace("CODE", str(code_com)), headers=headers)
                if p.ok:
                        content_population = p.json()
                        try:
                                code_com_pop.append(content_population['Zone']['@codgeo'])
                        except:
                                code_com_pop.append("")
                        try:
                                nom_com_pop.append(content_population['Zone']['Millesime']['Nccenr'])
                        except:
                                nom_com_pop.append("")
                        try:
                                annee_mill.append(content_population['Zone']['Millesime']['@annee'])
                        except:
                                annee_mill.append("")
                        try:
                                annee_popleg.append(content_population['Croisement']['JeuDonnees']['Annee'])
                        except:
                                annee_popleg.append("")
                        try:
                                popmun.append(content_population['Cellule'][0]['Valeur'])
                        except:
                                popmun.append("")
                        try:
                                popcap.append(content_population['Cellule'][1]['Valeur'])
                        except:
                                popcap.append("")
                        try:
                                poptot.append(content_population['Cellule'][2]['Valeur'])
                        except:
                                poptot.append("")
                else:
                        year_error.append(year)
                        code_com_error.append(code_com)
                        status.append(p.status_code)
df_error=pd.DataFrame({
        'year_error': year_error,
        'code_com_error' : code_com_error,
        'status' : p.status_code
})
df_population=pd.DataFrame({
    'code_commune': code_com_pop,
    'nom_commune' : nom_com_pop,
    'annee_millesime' : annee_mill,
    'annee_population_legale' : annee_popleg,
    'pop_mun' : popmun,
    'pop_cap' : popcap,
    'pop_tot' : poptot
    })

df_population.to_csv('data_population.csv',encoding='utf-8', index=False, index_label=False, mode='w' )

print(df_population.shape)
df_population