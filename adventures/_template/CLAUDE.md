# [ABENTEUER NAME]
*Ein TTRPG Abenteuer für 2 Spieler*

---

## Setup

Beim Start dieses Abenteuers:

1. Lies zuerst `../../_engine/DUNGEON_MASTER.md` — dort liegt die gesamte DM-Logik
2. Dann lies `session.yaml` um den aktuellen Status zu verstehen
3. Wenn `session.yaml` noch nicht existiert oder `status: setup` — starte Session 0
4. Wenn `status: active` oder `status: paused` — starte eine normale Session

---

## Spieler

- **Spieler 1:** [Name] — [Charakter wenn schon bekannt]
- **Spieler 2:** [Name] — [Charakter wenn schon bekannt]

---

## Abenteuer-Notizen für den DM

*(Wird nach Session 0 befüllt — oder du kannst hier schon Ideen hinschreiben)*

### Hauptkonflikt
[Was ist das große Problem oder die große Frage dieses Abenteuers?]

### Mögliche Richtungen
- [Möglicher Plot A]
- [Möglicher Plot B]
- [Wilder Joker den die Spieler vielleicht nie entdecken]

### Atmosphäre
[Stichworte: düster? humorvoll? romantisch? episch?]

---

## Dateien in diesem Ordner

```
[abenteuer_name]/
├── CLAUDE.md              ← du bist hier
├── session.yaml           ← Spielstand (auto-generiert)
├── setting.yaml           ← Welt & Regeln (auto-generiert in Session 0)
└── characters/
    ├── [spieler1].yaml    ← Charakterblatt (auto-generiert)
    ├── [spieler1]_charakterblatt.pdf
    ├── [spieler2].yaml
    └── [spieler2]_charakterblatt.pdf
```

---

## PDF neu generieren

```bash
python3 ../../_engine/tools/character_sheet.py
```
