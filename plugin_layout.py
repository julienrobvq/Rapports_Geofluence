from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox, QCheckBox, QLabel, QPushButton,
    QScrollArea, QWidget, QGridLayout, QMessageBox
)
from qgis.core import QgsProject

class RapportEEE(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sélection du site et des champs")
        self.resize(380, 420)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Sélectionnez un site :"))
        self.site_combo = QComboBox()
        layout.addWidget(self.site_combo)

        layout.addWidget(QLabel("Champs à inclure :"))
        scroll = QScrollArea()
        container = QWidget()
        self.champ_layout = QGridLayout(container)
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        self.btn_ok = QPushButton("Valider")
        layout.addWidget(self.btn_ok)
        self.btn_ok.clicked.connect(self.accept)

        # --- Charger la couche ---
        layers = QgsProject.instance().mapLayersByName("Form_EEE")
        if not layers:
            QMessageBox.critical(self, "Erreur", "Couche 'Form_EEE' introuvable.")
            self.reject(); return
        self.layer = layers[0]

        self.site_field = "site"  # champ exact dans ta couche

        # --- Définir manuellement les champs affichés ---
        self.champs_affiches = [
            "site",
            "zgie",
            "region",
            "Munic",
            "mrc",
            "Respo",
            "Milieu",
            "Repere",
            "Contrainte",
            "categorie",
            "EEE_Type",
            "lat_flore",
            "autre_sp",
            "autre_nom_latin",
            "Superf_m2",
            "StadeDev",
            "site_autre_stade",
            "site_stade_1",
            "site_stade_2",
            "site_stade_3",
            "site_stade_4",
            "site_stade_5",
            "cause_probag",
            "hote",
            "Trt_av",
            "Trt_avQui",
            "Trt_avType",
            "TraitRecom",
            "EEE_Comment",
            "photo1"
        ]

        # --- Remplir les listes ---
        self.remplir_sites()
        self.remplir_champs()

    def remplir_sites(self):
        valeurs = sorted({f[self.site_field] for f in self.layer.getFeatures()
                          if f[self.site_field] not in (None, "", " ")})
        self.site_combo.addItems([str(v) for v in valeurs])

    def remplir_champs(self):
        self.checkboxes = []
        for i, champ in enumerate(self.champs_affiches):
            alias = self.layer.fields().field(champ).alias() or champ
            cb = QCheckBox(alias)
            cb.setToolTip(champ)
            self.champ_layout.addWidget(cb, i, 0)
            self.checkboxes.append(cb)

    def get_selection(self):
        site = self.site_combo.currentText()
        champs = [cb.toolTip() for cb in self.checkboxes if cb.isChecked()]
        return site, champs


# --- Exécution ---
dlg = RapportEEE()
if dlg.exec_():
    site, champs = dlg.get_selection_
