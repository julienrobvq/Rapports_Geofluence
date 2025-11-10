# -*- coding: utf-8 -*-

from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QComboBox, QCheckBox, QLabel, QPushButton, QScrollArea, QWidget, QGridLayout, QMessageBox, QHBoxLayout
from qgis.core import QgsProject
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

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

        btn_layout = QHBoxLayout()
        self.btn_select_all = QPushButton("Tout sélectionner")
        self.btn_unselect_all = QPushButton("Tout désélectionner")
        btn_layout.addWidget(self.btn_select_all)
        btn_layout.addWidget(self.btn_unselect_all)
        layout.addLayout(btn_layout)

        self.btn_select_all.clicked.connect(self.select_all)
        self.btn_unselect_all.clicked.connect(self.unselect_all)

        self.btn_ok = QPushButton("Générer le rapport")
        layout.addWidget(self.btn_ok)
        self.btn_ok.clicked.connect(self.accept)

        # --- Charger la couche ---
        layers = QgsProject.instance().mapLayersByName("Form_EEE")
        if not layers:
            QMessageBox.critical(self, "Erreur", "Couche 'Form_EEE' introuvable.")
            self.reject(); return
        self.layer = layers[0]

        self.site_field = "site"

        # --- Champs affichés manuellement ---
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
    
    def select_all(self):
        for cb in self.checkboxes:
            cb.setChecked(True)

    def unselect_all(self):
        for cb in self.checkboxes:
            cb.setChecked(False)


    def get_selection(self):
        site = self.site_combo.currentText()
        champs = [cb.toolTip() for cb in self.checkboxes if cb.isChecked()]
        return site, champs

def get_display_value(layer, feature, field_name):
    """Retourne la valeur affichée dans QGIS pour un champ donné."""
    field = layer.fields().field(field_name)
    cfg = field.editorWidgetSetup()
    value = feature.attribute(field_name)

    if value in (None, ""):
        return ""

    # --- ValueMap ---
    if cfg.type() == "ValueMap":
        mapping = cfg.config().get("map", {})
        for k, v in mapping.items():
            if str(k) == str(value):
                return v
        return str(value)

    # --- ValueRelation ---
    if cfg.type() == "ValueRelation":
        rel_layer_id = cfg.config().get("Layer")
        key_field = cfg.config().get("Key")
        value_field = cfg.config().get("Value")
        rel_layer = QgsProject.instance().mapLayer(rel_layer_id)
        if rel_layer:
            for f in rel_layer.getFeatures():
                if str(f[key_field]) == str(value):
                    return str(f[value_field])
        return str(value)

    # --- Valeur par défaut ---
    return str(value)


# --- Exécution ---
dlg = RapportEEE()
if dlg.exec_():
    site, champs = dlg.get_selection()

    # Récupération des données dans QGIS
    layer = QgsProject.instance().mapLayersByName("Form_EEE")[0]
    expr = f'"site" = \'{site}\''
    layer.selectByExpression(expr)
    feats = layer.selectedFeatures()
    if not feats:
        QMessageBox.warning(None, "Avertissement", "Aucun enregistrement trouvé pour ce site.")
    else:
        feat = feats[0]  # premier enregistrement

        # --- Définir les sections et champs associés ---
        sections = {
            "Identification": ["site"],
            "Localisation": [
                            "site",
                            "zgie",
                            "region",
                            "Munic",
                            "mrc",
                            "Respo",
                            "Milieu",
                            "Repere",
                            "Contrainte"],
            "Observations": [
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
                            "hote"],
            "Traitement": [            
                            "Trt_av",
                            "Trt_avQui",
                            "Trt_avType",
                            "TraitRecom"],
            "Commentaires et photos": [
                            "EEE_Comment",
                            "photo1"]
        }

        # --- Création du PDF ---
        doc = SimpleDocTemplate("Rapport_EEE.pdf", pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Espèces exotiques envahissantes <br/> Première visite de site", styles["Title"]))
        story.append(Spacer(1, 20))

        # Parcourir les sections et injecter les champs sélectionnés
        for titre, liste_champs in sections.items():
            story.append(Paragraph(titre, styles["Heading2"]))
            contenu = []
            for champ in liste_champs:
                if champ in champs:  # seulement ceux cochés
                    alias = layer.fields().field(champ).alias() or champ
                    valeur = get_display_value(layer, feat, champ)
                    #Ignorer les valeurs nulles
                    if valeur not in ("", "NULL", "Null"):
                        contenu.append(f"<b>{alias}</b> : {valeur}")
            if contenu:
                story.append(Paragraph("<br/>".join(contenu), styles["BodyText"]))
            else:
                story.append(Paragraph("(Aucun champ sélectionné pour cette section)", styles["Italic"]))
            story.append(Spacer(1, 15))

        doc.build(story)
        print("Rapport généré avec succès.")
