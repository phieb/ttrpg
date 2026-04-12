#!/usr/bin/env python3
"""
TTRPG Charakterblatt Generator
Erstellt atmosphärische PDFs für jeden Spieler nach Session 0.
Aufruf: python3 character_sheet.py [abenteuer_pfad]
"""

import sys
import os
import glob
import yaml
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Farben — dunkel und atmosphärisch
COL_BG = colors.HexColor('#1a1410')          # Tief-Braun/Schwarz
COL_PARCHMENT = colors.HexColor('#c8a96e')   # Pergament-Gold
COL_PARCHMENT_LIGHT = colors.HexColor('#e8d5a3')  # Helles Pergament
COL_ACCENT = colors.HexColor('#8b2020')      # Dunkel-Rot
COL_ACCENT2 = colors.HexColor('#4a6741')     # Dunkel-Grün
COL_DARK_TEXT = colors.HexColor('#2a1f0a')   # Dunkelbraun für Text
COL_GOLD_LINE = colors.HexColor('#a07840')   # Gold für Linien
COL_FADE = colors.HexColor('#3d2e1a')        # Für Hintergrund-Elemente


def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def draw_background(c, width, height):
    """Zeichnet den atmosphärischen Hintergrund"""
    # Haupthintergrund
    c.setFillColor(COL_BG)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Pergament-Textur Overlay (mehrere halbtransparente Rechtecke)
    c.setFillColor(colors.HexColor('#2d1f0a'))
    c.rect(0.5*cm, 0.5*cm, width - 1*cm, height - 1*cm, fill=1, stroke=0)

    # Rand-Verzierung
    c.setStrokeColor(COL_GOLD_LINE)
    c.setLineWidth(2)
    c.rect(0.8*cm, 0.8*cm, width - 1.6*cm, height - 1.6*cm, fill=0, stroke=1)
    c.setLineWidth(0.5)
    c.rect(1.0*cm, 1.0*cm, width - 2.0*cm, height - 2.0*cm, fill=0, stroke=1)


def draw_ornament(c, x, y, size=20):
    """Zeichnet ein einfaches ornamentales Element"""
    c.setStrokeColor(COL_GOLD_LINE)
    c.setLineWidth(1)
    # Kleines Kreuz-Ornament
    c.line(x - size, y, x + size, y)
    c.line(x, y - size*0.4, x, y + size*0.4)
    c.circle(x, y, 3, fill=0, stroke=1)


def draw_divider(c, x, y, width):
    """Zeichnet eine dekorative Trennlinie"""
    c.setStrokeColor(COL_GOLD_LINE)
    c.setLineWidth(0.8)
    c.line(x, y, x + width, y)
    c.setLineWidth(0.3)
    c.line(x, y - 2, x + width, y - 2)


def draw_section_header(c, x, y, text, width, fontsize=11):
    """Zeichnet einen Abschnitt-Header mit Hintergrund"""
    c.setFillColor(COL_ACCENT)
    c.rect(x, y - 3, width, fontsize + 6, fill=1, stroke=0)

    c.setFillColor(COL_PARCHMENT_LIGHT)
    c.setFont("Helvetica-Bold", fontsize)
    c.drawString(x + 5, y + 1, text.upper())


def draw_skill_box(c, x, y, skill_name, skill_desc, box_width):
    """Zeichnet eine Skill-Box"""
    box_height = 2.2*cm
    padding = 0.3*cm

    # Box Hintergrund
    c.setFillColor(colors.HexColor('#1e1508'))
    c.setStrokeColor(COL_GOLD_LINE)
    c.setLineWidth(0.5)
    c.roundRect(x, y, box_width, box_height, 4, fill=1, stroke=1)

    # Skill Name
    c.setFillColor(COL_PARCHMENT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + padding, y + box_height - padding - 10, skill_name)

    # Skill Beschreibung — Textwrapping
    c.setFillColor(COL_PARCHMENT_LIGHT)
    c.setFont("Helvetica", 8)
    max_chars = int(box_width / 4.5)
    desc = skill_desc or ""
    lines = []
    words = desc.split()
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars:
            current_line += (" " if current_line else "") + word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for i, line in enumerate(lines[:3]):
        c.drawString(x + padding, y + box_height - padding - 24 - i*11, line)


def generate_character_pdf(char_data, setting_data, output_path):
    """Generiert ein atmosphärisches Charakterblatt als PDF"""
    char = char_data.get('charakter', {})
    ident = char_data.get('identitaet', {})
    skills = char_data.get('skills', [])
    motivation = char_data.get('motivation', {})
    beziehungen = char_data.get('beziehungen', {})
    imagen_prompt = char_data.get('imagen_prompt', '')
    welt = setting_data.get('welt', {}) if setting_data else {}

    width, height = A4
    c = canvas.Canvas(output_path, pagesize=A4)

    # Hintergrund
    draw_background(c, width, height)

    # Welt-Name oben klein
    welt_name = welt.get('name', 'Unbekannte Welt')
    c.setFillColor(COL_PARCHMENT)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, height - 1.5*cm, welt_name.upper())

    # Ornamente oben
    draw_ornament(c, width/2 - 4*cm, height - 1.5*cm, 15)
    draw_ornament(c, width/2 + 4*cm, height - 1.5*cm, 15)

    # CHARAKTERBLATT Titel
    c.setFillColor(COL_PARCHMENT_LIGHT)
    c.setFont("Helvetica", 9)
    c.drawCentredString(width/2, height - 2.2*cm, "— CHARAKTERBLATT —")

    # Charakter Name — groß
    char_name = char.get('name', 'Unbekannt')
    c.setFillColor(COL_PARCHMENT)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, height - 3.8*cm, char_name)

    # Gespielt von
    gespielt_von = char.get('gespielt_von', '')
    if gespielt_von:
        c.setFillColor(COL_GOLD_LINE)
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(width/2, height - 4.5*cm, f"gespielt von {gespielt_von}")

    draw_divider(c, 1.5*cm, height - 5.0*cm, width - 3*cm)

    # IDENTITÄT Bereich
    y_pos = height - 5.8*cm
    left_col = 1.5*cm
    right_col = width/2 + 0.3*cm
    col_width = width/2 - 1.8*cm

    draw_section_header(c, left_col, y_pos, "Identität", col_width * 2 + 0.3*cm)
    y_pos -= 0.7*cm

    # Wer bist du
    wer = ident.get('wer_bist_du', '')
    if wer:
        c.setFillColor(COL_PARCHMENT_LIGHT)
        c.setFont("Helvetica-Oblique", 9)
        # Textwrapping
        max_chars = 80
        words = wer.split()
        lines = []
        current = ""
        for word in words:
            if len(current) + len(word) + 1 <= max_chars:
                current += (" " if current else "") + word
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        for i, line in enumerate(lines[:3]):
            c.drawString(left_col + 0.3*cm, y_pos - i*12, line)
        y_pos -= (len(lines[:3]) * 12 + 8)

    # Aussehen, Alter, Herkunft
    details = [
        ("Aussehen", ident.get('aussehen', '')),
        ("Alter", ident.get('alter', '')),
        ("Herkunft", ident.get('herkunft', '')),
    ]
    for label, value in details:
        if value:
            c.setFillColor(COL_GOLD_LINE)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(left_col + 0.3*cm, y_pos, f"{label}:")
            c.setFillColor(COL_PARCHMENT_LIGHT)
            c.setFont("Helvetica", 8)
            c.drawString(left_col + 2.5*cm, y_pos, str(value)[:60])
            y_pos -= 14

    draw_divider(c, 1.5*cm, y_pos - 3, width - 3*cm)
    y_pos -= 0.7*cm

    # SKILLS Bereich
    draw_section_header(c, left_col, y_pos, "Fähigkeiten & Skills", col_width * 2 + 0.3*cm)
    y_pos -= 0.5*cm

    # Skills in 2 Spalten
    skill_width = col_width - 0.2*cm
    for i, skill in enumerate(skills[:6]):
        col_x = left_col if i % 2 == 0 else right_col
        if i % 2 == 0 and i > 0:
            y_pos -= 2.4*cm
        c.setFillColor(COL_PARCHMENT)
        c.setFont("Helvetica-Bold", 9)
        skill_name = skill.get('name', '') if isinstance(skill, dict) else str(skill)
        skill_desc = skill.get('beschreibung', '') if isinstance(skill, dict) else ''
        draw_skill_box(c, col_x, y_pos - 2.2*cm, skill_name, skill_desc, skill_width)

    if skills:
        rows = (len(skills[:6]) + 1) // 2
        y_pos -= (rows * 2.4*cm + 0.3*cm)
    else:
        y_pos -= 0.5*cm

    draw_divider(c, 1.5*cm, y_pos - 3, width - 3*cm)
    y_pos -= 0.7*cm

    # MOTIVATION Bereich
    draw_section_header(c, left_col, y_pos, "Motivation & Seele", col_width * 2 + 0.3*cm)
    y_pos -= 0.5*cm

    mot_items = [
        ("Will", motivation.get('will', '')),
        ("Fürchtet", motivation.get('fuerchtet', '')),
        ("Geheimnis", motivation.get('geheimnis', '')),
        ("Begleiter", beziehungen.get('begleiter', '')),
    ]
    for label, value in mot_items:
        if value:
            c.setFillColor(COL_GOLD_LINE)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(left_col + 0.3*cm, y_pos, f"{label}:")
            c.setFillColor(COL_PARCHMENT_LIGHT)
            c.setFont("Helvetica", 8)
            # Textwrapping für längere Texte
            max_chars = 70
            words = value.split()
            lines = []
            current = ""
            for word in words:
                if len(current) + len(word) + 1 <= max_chars:
                    current += (" " if current else "") + word
                else:
                    if current:
                        lines.append(current)
                    current = word
            if current:
                lines.append(current)
            for i, line in enumerate(lines[:2]):
                c.drawString(left_col + 3.0*cm, y_pos - i*11, line)
            y_pos -= (max(len(lines[:2]), 1) * 11 + 5)

    # NOTIZEN Bereich — am Ende
    draw_divider(c, 1.5*cm, y_pos - 5, width - 3*cm)
    y_pos -= 0.7*cm

    draw_section_header(c, left_col, y_pos, "Notizen & Zustand", col_width * 2 + 0.3*cm)
    y_pos -= 0.4*cm

    # Leere Linien für Notizen
    for i in range(4):
        c.setStrokeColor(COL_FADE)
        c.setLineWidth(0.5)
        c.line(left_col + 0.3*cm, y_pos - i*0.6*cm, width - 1.8*cm, y_pos - i*0.6*cm)

    # IMAGEN PROMPT Bereich — ganz unten
    if imagen_prompt:
        y_prompt = 2.5*cm
        draw_divider(c, 1.5*cm, y_prompt + 0.8*cm, width - 3*cm)
        c.setFillColor(COL_PARCHMENT)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(left_col, y_prompt + 0.2*cm, "IMAGEN 3 PROMPT:")
        c.setFillColor(COL_FADE)
        c.setFont("Helvetica", 6.5)
        # Wrap prompt
        words = imagen_prompt.split()
        lines = []
        current = ""
        for word in words:
            if len(current) + len(word) + 1 <= 100:
                current += (" " if current else "") + word
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        for i, line in enumerate(lines[:3]):
            c.setFillColor(COL_PARCHMENT_LIGHT)
            c.drawString(left_col, y_prompt - i*9, line)

    # Seitenzahl / Footer
    c.setFillColor(COL_GOLD_LINE)
    c.setFont("Helvetica", 7)
    c.drawCentredString(width/2, 1.2*cm, f"~ {char_name} ~ {welt_name} ~")

    c.save()
    print(f"PDF erstellt: {output_path}")


def main():
    # Pfad zum Abenteuer-Ordner (default: aktuelles Verzeichnis)
    if len(sys.argv) > 1:
        adventure_path = Path(sys.argv[1])
    else:
        adventure_path = Path.cwd()

    # Engine-Pfad (relativ zu diesem Script)
    engine_path = Path(__file__).parent.parent

    # Setting laden
    setting_path = adventure_path / 'setting.yaml'
    setting_data = {}
    if setting_path.exists():
        setting_data = load_yaml(setting_path)

    # Alle Charakter-YAMLs finden
    char_dir = adventure_path / 'characters'
    if not char_dir.exists():
        print(f"Kein 'characters/' Ordner in {adventure_path}")
        sys.exit(1)

    char_files = list(char_dir.glob('*.yaml'))
    if not char_files:
        print("Keine Charakter-YAMLs gefunden.")
        sys.exit(1)

    # PDFs generieren
    for char_file in char_files:
        if char_file.name.startswith('_'):
            continue
        char_data = load_yaml(char_file)
        char_name = char_data.get('charakter', {}).get('name', char_file.stem)
        output_pdf = char_dir / f"{char_file.stem}_charakterblatt.pdf"
        print(f"Generiere Charakterblatt für {char_name}...")
        generate_character_pdf(char_data, setting_data, str(output_pdf))

    print("\nAlle Charakterblätter erstellt!")
    print(f"Gespeichert in: {char_dir}")


if __name__ == '__main__':
    main()
