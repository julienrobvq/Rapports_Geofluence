# rapports/mhh.py

import os
from .base import BaseRapport
from docxtpl import DocxTemplate
from qgis.core import QgsProject
from qgis.PyQt.QtWidgets import QMessageBox


class RapportMHH(BaseRapport):

    def __init__(self, parent=None):

        super().__init__(
            layer_form_name="Form_MHH",
            champs_affiches=[],
            parent=parent,
        )

        # Si couche absente on annule
        if not hasattr(self, "layer_form"):
            self._init_ok = False
            return

        self._init_ok = True

        self.layer_mhh = self.layer_form

        self.layer_even = QgsProject.instance().mapLayersByName("Evenement")[0]
        self.layer_sol = QgsProject.instance().mapLayersByName("FormSect_Sol")[0]
        self.layer_pert = QgsProject.instance().mapLayersByName("FormSect_TypePert")[0]
        self.layer_veget = QgsProject.instance().mapLayersByName("FormSect_SP_Veget")[0]

        self.champs_affiches = [
            "Nom_Station",
            "num_echant",
            "Contexte",
            "Situat",
            "FormTerr",
            "Depress",
            "Depres_pct",
            "Montic_pct",
            "Date"
        ]

    def exec_(self):
        if not getattr(self, "_init_ok", True):
            return 0
        return super().exec_()

    def export_word(self, file_path):

        template_path = os.path.join(
            os.path.dirname(__file__),
            "templates",
            "template_mhh.docx"
        )
        doc = DocxTemplate(template_path)

        feat_mhh = self.current_feats_form[0]
        id_ref = feat_mhh["ID_MHH"]

        feat_even = next(
            (f for f in self.layer_even.getFeatures() if f["ID_EVEN"] == feat_mhh["ID_EVEN"]),
            None
        )
        feat_sol = next(
            (f for f in self.layer_sol.getFeatures() if f["ID_MHH"] == id_ref),
            None
        )
        feat_pert = next(
            (f for f in self.layer_pert.getFeatures() if f["ID_MH"] == id_ref),
            None
        )
        feat_veget = next(
            (f for f in self.layer_veget.getFeatures() if f["ID_MHH"] == id_ref),
            None
        )

        context = {
            "mhh": {},
            "even": {},
            "sol": {},
            "pert": {},
            "veget": {},
        }

        for champ in self.champs_affiches:
            if champ in self.layer_form.fields().names():
                context["mhh"][champ] = self.get_display_value(
                    self.layer_form, feat_mhh, champ
                    )

        if feat_even:
            for champ in self.champs_affiches:
                if champ in self.layer_even.fields().names():
                    context["even"][champ] = self.get_display_value(
                        self.layer_even, feat_even, champ
                        )
        
        if feat_sol:
            for champ in self.champs_affiches:
                if champ in self.layer_sol.fields().names():
                    context["sol"][champ] = self.get_display_value(
                        self.layer_sol, feat_sol, champ
                        )

        if feat_pert:
            for champ in self.champs_affiches:
                if champ in self.layer_pert.fields().names():
                    context["pert"][champ] = self.get_display_value(
                        self.layer_pert, feat_pert, champ
                        )

        if feat_veget:
            for champ in self.champs_affiches:
                if champ in self.layer_veget.fields().names():
                    context["veget"][champ] = self.get_display_value(
                        self.layer_veget, feat_veget, champ
                        )

        doc.render(context)
        doc.save(file_path)
        QMessageBox.information(self, "Bravo", "Rapport Milieu humide généré")