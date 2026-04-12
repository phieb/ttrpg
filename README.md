# TTRPG — Dungeon Master System

Narratives Rollenspiel mit Claude als Dungeon Master.
Ein D20 für alles, keine Würfelmechanik-Bürokratie, dafür gute Geschichten.

> **Signal-Bot:** Dieses Repo enthält die Spielwelt-Daten (Engine, Templates, Abenteuer).
> Der dazugehörige Signal-Bot (Routing, Claude API, Avatar-Generierung) liegt in
> [phieb/ttrpg-signal](https://github.com/phieb/ttrpg-signal).

## Struktur

```
ttrpg/
├── _engine/                          ← nie anfassen, immer gleich
│   ├── DUNGEON_MASTER.md             ← die DM-Logik (Kern des Systems)
│   ├── templates/                    ← Vorlagen für neue Abenteuer
│   │   ├── character.yaml
│   │   ├── setting.yaml
│   │   ├── npcs.yaml
│   │   └── session.yaml
│   └── tools/
│       └── generate_character_pdf.py ← Charakterblatt PDFs + Gemini Prompts
└── adventures/
    ├── _template/                    ← Vorlage für neues Abenteuer (kopieren!)
    │   └── CLAUDE.md
    └── [abenteuer-name]/             ← ein Ordner pro Abenteuer
        ├── CLAUDE.md
        ├── setting.yaml
        ├── npcs.yaml
        ├── session.yaml
        └── characters/
            ├── [name].yaml
            ├── [name]_charakterblatt.pdf
            └── [name]_portrait_prompt.txt
```

## Neues Abenteuer starten

```bash
cp -r adventures/_template adventures/mein_abenteuer
cd adventures/mein_abenteuer
# Claude Code öffnen und sagen: "Starte Session 0"
```

## Spielen

Claude Code im Abenteuer-Ordner öffnen und sagen:
- `Starte Session 0` — Weltenbau und Charaktererstellung
- `Weiterspielen` — Abenteuer fortsetzen

## Während dem Spiel

| Kommando | Was passiert |
|----------|-------------|
| `pause` | Spielstand speichern |
| `session 0 abschließen` | Weltenbau beenden, PDFs generieren |
| D20 würfeln und Zahl eintippen | Würfelergebnis |

## PDFs neu generieren

```bash
cd adventures/[abenteuer-name]
pip install reportlab pyyaml
python3 ../../_engine/tools/generate_character_pdf.py
```

## Würfelsystem

Ein D20 für alles. Physisch würfeln, Ergebnis eintippen.

| Ergebnis | Bedeutung |
|----------|-----------|
| 1 | Kritisches Versagen |
| 2-5 | Versagen |
| 6-10 | Teilerfolg mit Haken |
| 11-15 | Erfolg |
| 16-19 | Voller Erfolg |
| 20 | Kritischer Erfolg |

Relevanter Skill = eine Stufe besser. Schwäche trifft zu = eine Stufe schlechter.
