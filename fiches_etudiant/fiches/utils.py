from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io

def generate_pdf(fiche):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1,  
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        spaceBefore=12,
    )
    
    normal_style = styles['Normal']
    
    content = []
    
    title = Paragraph(f"Fiche des etudiants de l'ASJA ", title_style)
    content.append(title)
    content.append(Spacer(1, 20))
    if fiche.photo :
        img = Image(fiche.photo,width=100, height=100)
        img.hAlign='RIGHT'
        content.append(img)
    
    content.append(Paragraph("Informations Personnelles", heading_style))
    content.append(Paragraph(f"<b>Nom :</b> {fiche.nom}", normal_style))
    content.append(Paragraph(f"<b>Prénom :</b> {fiche.prenom}", normal_style))
    content.append(Paragraph(f"<b>Filière :</b> {fiche.filiere}", normal_style))
    content.append(Paragraph(f"<b>Niveau :</b> {fiche.niveau}", normal_style))
    content.append(Spacer(1, 12))

    if fiche.interets:
        content.append(Paragraph("Centres d'Intérêt", heading_style))
        content.append(Paragraph(fiche.interets, normal_style))
        content.append(Spacer(1, 12))
    
    if fiche.description:
        content.append(Paragraph("Description", heading_style))
        content.append(Paragraph(fiche.description, normal_style))
        content.append(Spacer(1, 12))

        
        
    if fiche.avis_responsable:
        content.append(Paragraph("Avis du Responsable", heading_style))
        content.append(Paragraph(fiche.avis_responsable, normal_style))
    
    doc.build(content)
    buffer.seek(0)
    return buffer