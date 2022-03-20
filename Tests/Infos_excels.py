import os
import pandas as pd
import glob as g


direction = './data'

Admis = {}
Admissibles = {}
Classes = {}
CMT_Oraux = {}
Ecrits = {}
Inscription = {}
Ecoles = {}
Etablissements = {}
EtatsReponses = {}
Voeux = {}
Oraux = {}
Resultats_ecrits = {}
Resultats_oraux = {}



Infos = {"admis" : Admis, "admissible" : Admissibles,
         "classes" : Classes, "CMT_oraux" : CMT_Oraux,
         "ecrit" : Ecrits, "inscription" : Inscription,
         "ecoles" : Ecoles, "etablissements" : Etablissements,
         "etats_reponses" : EtatsReponses, "voeux" : Voeux,
         "oraux" : Oraux, "resultats_ecrits" : Resultats_ecrits,
         "resultats_oraux" : Resultats_oraux}

Admis["nombre d'admis"] = 0
Admissibles["nombre d'admissibles"] = 0


#ajout des nombres de lignes des excels
for excel in os.listdir(direction):
    #Admis
    if excel.startswith("ADMIS_") and excel.endswith("SPE.xlsx"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        Admis["nombre d'admis"] += len(a)
    #Admissibles
    elif excel.startswith("ADMISSIBLE_") and excel.endswith("SPE.xlsx"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        Admissibles["nombre d'admissibles"] += len(a)
    #Classes
    elif excel.startswith("Classes_MP") and not excel.endswith("SCEI.csv"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        Classes["nombre d'eleves en MP"] = len(a)
    elif excel.startswith("Classes_PC") and not excel.endswith("SCEI.csv"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        Classes["nombre d'eleves en PC"] = len(a)
    elif excel.startswith("Classes_PSI") and not excel.endswith("SCEI.csv"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        Classes["nombre d'eleves en PSI"] = len(a)
    elif excel.startswith("Classes_PT") and not excel.endswith("SCEI.csv"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        Classes["nombre d'eleves en PT"] = len(a)
    elif excel.startswith("Classes_TSI") and not excel.endswith("SCEI.csv"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        Classes["nombre d'eleves en TSI"] = len(a)
    #CMT (concours mines télécom) notes
    elif excel.startswith("CMT_") and excel.endswith("MP.xlsx"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        Classes["nombre d'eleves en MP bis"] = len(a)


print(Admis["nombre d'admis"])
print(Admissibles["nombre d'admissibles"])
print(Classes["nombre d'eleves en MP"])
print(Classes["nombre d'eleves en MP bis"])


###Infos du fichiers Inscription

files = os.listdir(direction)

print(files[0])

path = os.path.join(direction, "Inscription.xlsx")
inscription = pd.read_excel(path, engine='openpyxl')

Inscription["nombre de lignes"] = len(inscription) - 1
#for i in range(len(inscription) - 1):
    #Infos["Inscription"]["nombre de sansINE"] = 1

print(Infos["inscription"]['nombre de lignes'])
