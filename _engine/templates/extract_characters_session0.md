Analysiere dieses Session-0-Gespräch und extrahiere die Charakterdaten für die Spieler: $players_str

Gespräch:
$conversation

Gib die extrahierten Daten als JSON zurück — nur Felder die tatsächlich im Gespräch vorkommen, keine Erfindungen:
{"charaktere": {"SpielerName": {"name": "Charaktername", "wer_bist_du": "Kurze Charakterbeschreibung", "aussehen": "Aussehen", "alter": "Alter", "herkunft": "Herkunft", "skills": [{"name": "Skillname", "beschreibung": "Kurze Beschreibung"}], "will": "Ziel/Wunsch des Charakters (Liste wenn mehrere)", "fuerchtet": "Angst/Schwäche", "geheimnis": "Geheimnis (falls erwähnt)", "begleiter": "Wichtige Beziehung (falls erwähnt)", "imagen_prompt": "Detailed English portrait prompt: appearance, clothing, style, background, lighting, mood"}}}$flavour_additions

Nur JSON zurückgeben. Felder weglassen wenn keine Info vorhanden.
