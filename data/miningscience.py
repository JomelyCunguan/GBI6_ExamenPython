def download_pubmed (keyword):
    """
    Funcion que pide como entrada una variable tipo string y como salida muestra un DataFrame 
    """
    from Bio import Entrez
    from Bio import SeqIO
    from Bio import GenBank 
    Entrez.email = 'jomely.cunguan@example.com'
    handle = Entrez.esearch(db='pubmed',
                        sort='relevance',
                        retmax='1000',
                        retmode='xml',
                        term=keyword)
    results = Entrez.read(handle)
    id_list = results["IdList"]
    ids = ','.join(id_list)
#id_l.append(ids)
    Entrez.email = 'jomely.cunguan@example.com'
    handle = Entrez.efetch(db='pubmed',
                       retmode='xml',
                       id=ids)
    id_l = ids.split(",")
    return (id_l) 


##mining_pubs 
import csv 
import re
import pandas as pd 
from collections import Counter

def mining_pubs(tipo):
    """
    función que pide como entrada una variable tipo string que puede ser "DP", "AU y "AD" y en output muestra un DataFrame 
    de PMID y año de publicación; PMID y pais y numero de autores respectivamente
    """
    with open("pubmed-EcuadorGen-set.txt", errors="ignore") as f: 
        texto = f.read() 
    if tipo == "DP":
        ## Data frame con el PMID y año de publicación
        PMID = re.findall("PMID- (\d*)", texto) 
        year = re.findall("DP\s{2}-\s(\d{4})", texto) ##extrae el año de publicación de los articulos 
        pmid_year = pd.DataFrame()
        pmid_year["PMID"] = PMID
        pmid_year["Año de publicación"] = year
        return (pmid_year)
    ## Data frame con el PMID y año de publicación 
    elif tipo == "AU": 
        PMID = re.findall("PMID- (\d*)", texto) 
        autores = texto.split("PMID- ")
        autores.pop(0)
        num_autores = []
        for i in range(len(autores)):
            numero = re.findall("AU -", autores[i])
            n = (len(numero))
            num_autores.append(n)
        pmid_autor = pd.DataFrame()
        pmid_autor["PMID"] = PMID 
        pmid_autor["Numero de autores"] = num_autores
        return (pmid_autor)
    elif tipo == "AD": 
        texto = re.sub(r" [A-Z]{1}\.","", texto)
        texto = re.sub(r"St\.","", texto)
        texto = re.sub(r"Av\.","", texto)
        texto = re.sub(r"Vic\.","", texto)
        texto = re.sub(r"Tas\.","", texto)
        texto = re.sub(r"Md\.","", texto)
        AD = texto.split("AD  - ")
        n_paises = []
        for i in range(len(AD)): 
            pais = re.findall("\S, ([A-Za-z]*)\.", AD[i])
            if not pais == []: ## se elimina las listas vacias que no contienen información de los paises 
                if not len(pais) >= 2:  ## se eliminae en caso de que la lista tenga mas de un elemento  
                    if re.findall("^[A-Z]", pais[0]): ## se elimina aquellas selecciones que no empiezan con mayusculas
                        n_paises.append(pais[0])
        conteo=Counter(n_paises)
        resultado = {}
        for clave in conteo:
            valor = conteo[clave]
            if valor != 1: 
                resultado[clave] = valor 
        numero_pais = pd.DataFrame()
        numero_pais["pais"] = resultado.keys()
        numero_pais["numero de autores"] = resultado.values()
        return (numero_pais)
