# dialogs/rapport_actdetection_dialog.py

from .base_rapport_dialog import BaseRapportDialog

class RapportActDetectionDialog(BaseRapportDialog):
    def __init__(self):
        champs = [
                    "nom_site",
                    "utilisateur",
                    "courriel",
                    "date",
                    "date_fin",
                    "heure",
                    "precision",
                    "region",
                    "munic",
                    "mrc",
                    "superficie",
                    "perimetre",
                    "activite",
                    "methode",
                    "effort",
                    "eee_detec",
                    "comment",
                    "photo"
                ]

        sections = {
            "Visite": [
                    "nom_site",
                    "utilisateur",
                    "courriel",
                    "date",
                    "date_fin",
                    "heure",
                    "precision"
                ],
            "Information sur le site": [
                    "region",
                    "munic",
                    "mrc",
                    "superficie",
                    "perimetre"
                ],
            "Activité de détection": [
                    "activite",
                    "methode",
                    "effort",
                    "eee_detec",
                    "comment",
                    "photo"
                ]
        }
        super().__init__("Form_ActDetection", champs, sections)
