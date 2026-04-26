Analysiere dieses Charaktererstellungs-Gespräch für Spieler '$player_name' und extrahiere die Charakterdaten.

Gespräch:
$conversation

Gib die extrahierten Daten als JSON zurück — nur Felder die tatsächlich im Gespräch vorkommen, keine Erfindungen:
{"name": "Charaktername", "wer_bist_du": "Kurze Charakterbeschreibung", "aussehen": "Aussehen", "alter": "Alter", "herkunft": "Herkunft", "skills": [{"name": "Skillname", "beschreibung": "Kurze Beschreibung"}], "will": "Ziel/Wunsch des Charakters (Liste wenn mehrere)", "fuerchtet": "Angst/Schwäche", "geheimnis": "Geheimnis (falls erwähnt)", "praeferenzen": {"no_gos": [], "wishes": []}, "imagen_prompt": "Detailed English portrait prompt: appearance, clothing, style, background, lighting, mood"}$flavour_additions

Nur JSON zurückgeben. Felder weglassen wenn keine Info vorhanden.
