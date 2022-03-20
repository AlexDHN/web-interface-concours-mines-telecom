import sqlite3 as sql
import os
import pandas as pd

##Création des différents listes de données à partir des excels##

candidats_codes = [] #liste des candidats
direction = './../../data'
candidats_codes_SCEI = [] #liste des candidats dans les excels XXX_SCEI
admis = []
admissibles = []
refuses = []


for excel in  os.listdir(direction):
    #on parcourt tous les excels à la recherche de ceux qui contiennent des codes de candidats
    if excel.endswith(".xlsx") and excel.startswith("ADMIS"):
        #Dans les excels Admis_XXX et Admissibles_XXX, le code est de la forme "Can _cod" 
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        for i in range(len(a) - 1):
            code_etudiant = a.loc[i, 'Can _cod']
            if code_etudiant not in candidats_codes:
                candidats_codes.append(code_etudiant)
            if excel.startswith("ADMIS_") and not excel.endswith("ATS.xlsx"): ##A CORRIGER : la table Admis_ATS fait des bêtises
                if code_etudiant not in admis:
                    admis.append(code_etudiant)
            elif excel.startswith("ADMISSIBLE_") and not excel.endswith("ATS.xlsx"):
                if (code_etudiant not in admissibles) and (code_etudiant != 116150):
                    admissibles.append(code_etudiant)
    #les candidats qui ne sont que dans les tables résultats n'ont que des résultats : on a décidé de pas en tenir compte (juste pour les stats)
    elif excel.endswith(".xlsx") and excel.startswith("Inscript"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        for i in range(1, len(a) - 2):
            if a.loc[i, " "] not in candidats_codes:
                candidats_codes.append(a.loc[i, " "])
    #les candidats qui sont dans les tables XXX_SCEI se retrouvent tous dans les autres excels déjà parcourus
    #On les stocke dans une liste différente pour pouvoir prouver ce postulat ensuite            
    elif excel.endswith("SCEI.xlsx"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        for i in range(1, len(a) - 1):
            if a.loc[i, "scei"] not in candidats_codes_SCEI:
                candidats_codes_SCEI.append(a.loc[i, "scei"])


for code in admis:
    if code in admissibles:
        # admissibles = list(filter(lambda a:a != code, admissibles))
        admissibles.remove(code)
for code in candidats_codes:
    #création de la liste des refuses
    if (code not in admis) and (code not in admissibles):
        refuses.append(code)

# print("voici tous les candidats", candidats_codes,"\n")
# print("voici admis", admis, "\n")
# print("voici admissible", admissibles, "\n")
# print("voici refusés", refuses, "\n")


##Tests dans MinesDB##

DATABASE = './MinesDB copy.db'

con = sql.connect(DATABASE)
cur = con.cursor()


###Codes des candidats

#Vérification que les candidats de SCEI sont bien dans les autres excels utilisés :
def test_candidats_SCEI_dans_autres_excels():
    for code in candidats_codes_SCEI:
        assert(code in candidats_codes)

#Vérification de si les candidats des SPE sont dans les non SPE ou vice-versa



##Vérification que tous les candidats des excels sont dans la BDD :
def test_grosse_boucle_de_lenfer():
    for code in candidats_codes:
        a = cur.execute('SELECT can_cod FROM ELEVE WHERE can_cod = (?)', (float(code),)).fetchone()
        if a is None:
            a = cur.execute('SELECT can_cod FROM ATS WHERE can_cod = (?)', (float(code),)).fetchone()
        if a is None:
            a = cur.execute('SELECT can_cod FROM RESULTAT WHERE can_cod = (?)', (float(code),)).fetchone()
        assert a == (float(code),)

#Vérification des admissibles / admis / refuses
def test_admis_admissibles():
    for code in admis:
        a = cur.execute('SELECT can_cod FROM Admission WHERE can_cod = (?) AND id_type_admission = 0', (float(code),)).fetchone()
        assert a == (float(code),)
    for code in admissibles:
        a = cur.execute('SELECT can_cod FROM Admission WHERE can_cod = (?) AND id_type_admission = 1', (float(code),)).fetchone()
        assert a == (float(code),)
    for code in refuses:
        a = cur.execute('SELECT can_cod FROM Admission WHERE can_cod = (?) AND id_type_admission = 2', (float(code),)).fetchone()
        assert a == (float(code),)
