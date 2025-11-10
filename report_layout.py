from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Création du document
doc = SimpleDocTemplate("Rapport_EEE.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = []

# Titre principal
story.append(Paragraph("Espèces exotiques envahissantes <br/> Première visite de site", styles["Title"]))
story.append(Spacer(1, 20))

# Cinq sections
sections = [
    "Informations générale",
    "Localisation",
    "Observations",
    "Traitement",
    "Commentaires et photos"
]

for s in sections:
    story.append(Paragraph(s, styles["Heading2"]))
    story.append(Paragraph("Contenu de la section " + s, styles["BodyText"]))
    story.append(Spacer(1, 15))

doc.build(story)