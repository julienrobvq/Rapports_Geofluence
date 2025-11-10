import re

# chemin du fichier à analyser
chemin_fichier = "eee.xml"   # adapte le nom selon ton fichier

# lire le contenu du fichier
with open(chemin_fichier, "r", encoding="utf-8") as f:
    texte = f.read()

# expression régulière
pattern = r'name="([^"]*)"'

# trouver toutes les correspondances
resultats = re.findall(pattern, texte)

# afficher les résultats
for r in resultats:
    print(r)
