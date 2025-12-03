# Rapports Géofluence

Cette extension QGIS permet de générer des rapports aux formats word et pdf depuis les formulaires de Géofluence.

Les données incluses dans les rapports peuvent être sélectionnées en fonction des projets (Événement).

La mise en page des rapports est normalisée, permettant une génération rapide et efficace et rapports simples. Il est possible de personnaliser la mise en page de certains rapport au besoin.

## Note pour les rapports Word

La génération des rapports Word s'effectue au moyen du package python-docx. Pour pouvoir l'utiliser, il faut télécharger le dossier 'python_docx-1.2.0.tar.gz' sur ce site : https://pypi.org/project/python-docx/#files

Une fois dézipé, copier le dossier docx situé à cet endroit : "python_docx-1.2.0\src\docx".

Coller ensuite le dossier dans le répertoire site-packages de QGIS : "C:\Program Files\QGIS 3.40.11\apps\Python312\Lib\site-packages".

Ce répertoire permet l'installation de packages tiers dans QGIS.