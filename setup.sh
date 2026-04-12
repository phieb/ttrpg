#!/bin/bash
# TTRPG Datei-Organizer
# Aufruf: bash setup.sh
# Aus dem ttrpg/ Ordner aufrufen

set -e

TTRPG_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Organisiere Dateien in: $TTRPG_DIR"

# Zone.Identifier Müll löschen
find "$TTRPG_DIR" -maxdepth 1 -name "*.Identifier" -delete
echo "  Zone.Identifier Dateien gelöscht"

# Ordnerstruktur anlegen
mkdir -p "$TTRPG_DIR/_engine/tools"
mkdir -p "$TTRPG_DIR/_engine/templates"
mkdir -p "$TTRPG_DIR/adventures/_template/characters"
mkdir -p "$TTRPG_DIR/adventures/test_abenteuer/characters"

# Engine-Dateien
[ -f "$TTRPG_DIR/DUNGEON_MASTER.md" ]   && mv "$TTRPG_DIR/DUNGEON_MASTER.md"   "$TTRPG_DIR/_engine/DUNGEON_MASTER.md"   && echo "  _engine/DUNGEON_MASTER.md"
[ -f "$TTRPG_DIR/character_sheet.py" ]  && mv "$TTRPG_DIR/character_sheet.py"  "$TTRPG_DIR/_engine/tools/generate_character_pdf.py" && echo "  _engine/tools/generate_character_pdf.py"

# Templates
[ -f "$TTRPG_DIR/character.yaml" ]      && mv "$TTRPG_DIR/character.yaml"      "$TTRPG_DIR/_engine/templates/character.yaml" && echo "  _engine/templates/character.yaml"

# Abenteuer-Template
[ -f "$TTRPG_DIR/ABENTEUER_CLAUDE.md" ] && mv "$TTRPG_DIR/ABENTEUER_CLAUDE.md" "$TTRPG_DIR/adventures/_template/CLAUDE.md"  && echo "  adventures/_template/CLAUDE.md"

# Test-Abenteuer
[ -f "$TTRPG_DIR/session.yaml" ]        && mv "$TTRPG_DIR/session.yaml"        "$TTRPG_DIR/adventures/test_abenteuer/session.yaml" && echo "  adventures/test_abenteuer/session.yaml"
[ -f "$TTRPG_DIR/setting.yaml" ]        && mv "$TTRPG_DIR/setting.yaml"        "$TTRPG_DIR/adventures/test_abenteuer/setting.yaml" && echo "  adventures/test_abenteuer/setting.yaml"

# Charaktere ins test_abenteuer
for f in phieb.yaml markus.yaml lyra.yaml; do
  [ -f "$TTRPG_DIR/$f" ] && mv "$TTRPG_DIR/$f" "$TTRPG_DIR/adventures/test_abenteuer/characters/$f" && echo "  adventures/test_abenteuer/characters/$f"
done

# PDFs ins test_abenteuer
for f in phieb_charakterblatt.pdf markus_charakterblatt.pdf lyra_charakterblatt.pdf; do
  [ -f "$TTRPG_DIR/$f" ] && mv "$TTRPG_DIR/$f" "$TTRPG_DIR/adventures/test_abenteuer/characters/$f" && echo "  adventures/test_abenteuer/characters/$f"
done

echo ""
echo "Fertig! Struktur:"
find "$TTRPG_DIR" -not -path "*/\.*" | sort | sed 's|[^/]*/|  |g'
