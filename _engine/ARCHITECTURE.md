# TTRPG Engine Architecture

## The Beginning
TTRPG BOT — AKTUELLER STAND
ENGINE (Haupt-DM-Prompt)
DUNGEON_MASTER.md          ← reguläres Spiel + Session 0
CHARACTER_SETUP.md         ← privater 1:1 Charakter-Setup Kanal
  └── Flag-System          ← lädt Module pro Phase wenn aktiv
FLAGS / MODULE
flags/
  ├── mature_content/
  │   ├── DUNGEON_MASTER.md      ← sensuell, literarisch, in-scene bleiben
  │   └── CHARACTER_SETUP.md    ← mature-content spezifische Setup-Fragen
  └── booktok/
      ├── DUNGEON_MASTER.md     ← romance arc, spannungsbogen, orchestrierung
      ├── SESSION_ZERO.md       ← booktok Session 0 Anpassungen
      ├── CHARACTER_SETUP.md    ← dark romance Charakterfindung
      └── CONTENT_PREFERENCES.md ← vollständiges Präferenzen-Menü
SESSION ZERO
session_zero/
  ├── spieler_vorbereitung.md     ← Einladungsdokument für Spieler
  ├── beispielcharaktere.md       ← Inspiration Spieler + DM-Hebel
  └── content_preferences.md     ← Wishes / No-Gos Menü
LAUFENDE SESSION
session_zero/
  ├── charakter_discovery.md     ← 4 Enthüllungsszenen System
  └── [noch offen: Spieler→DM Befehl während Spiel]
DATEN PRO ABENTEUER
abenteuer/
  ├── setting.yaml
  ├── session.yaml          ← inkl. romance_arc tracking
  ├── content_matrix.yaml   ← wishes/no-gos aller Spieler
  ├── npcs.yaml
  └── characters/
        └── [name].yaml
FLOW
Einladung DM → Spieler (privat)
  → Consent
  → Spielervorbereitung + Beispielcharaktere
  → Content Preferences
  → Charakter Name + Erscheinung
  → [alle bereit] → Gruppenkanal
  → Erste Szene + Bild
  → Spiel läuft
        ├── Gruppenkanal: nur Story
        └── Privatkanal: [Befehl noch offen]

Was noch fehlt / offen:
* Anpassung aller Prompts an neues System. 
□ Privat-Befehl Spieler→DM während Spiel
□ Onboarding-Prompt (DM schreibt Spieler an)
□ Trigger Warnings als konfigurierbares Template - differenzierung default und flag Trigger
□ Epilog / Abenteuer-Abschluss
□ Wie Spieler 2 in laufende Szene einsteigt


## Overview
This document describes the complete architecture of the TTRPG Dungeon Master system, including the three DM phases, flag system, character creation flow, and content preference management.
---
## 1. The Three DM Phases
The DM operates in three distinct phases, each with different responsibilities and file templates:
| Phase | Channel | Description |
|-------|---------|-------------|
| **Character Setup** | Private DM → Player | Individual character creation, content preferences |
| **Session 0** | Group channel | Character introductions, first scene, world building |
| **Regular Play** | Group channel | Main gameplay, quest progression |
### Phase 1: Character Setup (Private)
**When:** After player is invited, before Session 0
**Flow:**
1. DM sends invitation + adventure description + trigger warnings
2. Player gives consent
3. DM sends character creation questionnaire
4. Player provides: name, appearance, background, skills, weaknesses, goals
5. DM collects content preferences (wishes, no-gos)
6. Repeat for each player
**Output:** `characters/[player_name].yaml` with full character data
### Phase 2: Session 0 (Group)
**When:** All players have completed character setup
**Flow:**
1. DM creates first scene with all characters together
2. DM generates scene image with all character avatars
3. Introduces the world, current situation, main quest hook
4. Players interact, establish relationships
5. Session 0 ends when setup complete
**Output:** `session.yaml` with status: 1, initial scene set
### Phase 3: Regular Play (Group)
**When:** Session 0 complete, ongoing gameplay
**Flow:**
1. DM describes scene
2. NSCs act
3. DM asks group: "Was macht ihr?"
4. Players decide
5. DM resolves actions
6. Repeat
**Output:** `session.yaml` updated after each session
---
## 2. File Structure
```
ttrpg/
├── _engine/
│   ├── ARCHITECTURE.md              # This file
│   ├── TOP_DM_REGELN.md          # Core rules (always loaded)
│   ├── DUNGEON_MASTER.md         # Regular play DM rules
│   ├── SESSION_ZERO.md           # Session 0 DM rules
│   ├── templates/
│   │   ├── character.yaml     # Character template
│   │   └── adventure.yaml    # Adventure setup template
│   ├── flags/
│   │   ├── mature_content/
│   │   │   ├── DUNGEON_MASTER.md
│   │   │   └── CHARACTER_SETUP.md
│   │   └── booktok/
│   │       ├── DUNGEON_MASTER.md
│   │       ├── SESSION_ZERO.md
│   │       ├── CHARACTER_SETUP.md
│   │       └── CONTENT_PREFERENCES.md
│   └── tools/
│       └── generate_character_pdf.py
├── adventures/
│   └── [adventure_name]/
│       ├── setting.yaml        # World, atmosphere, flags
│       ├── session.yaml       # Current state, quest backlog
│       ├── npcs.yaml          # Known NPCs
│       ├── characters/
│       │   ├── [player1].yaml
│       │   └── [player2].yaml
│       └── spielprotokoll.jsonl # Full log
└── status.yaml                 # Global adventure status
```
---
## 3. Character Data Model
Stored in: `adventures/[name]/characters/[player].yaml`
```yaml
charakter:
  name: "Character Name"
  gespielt_von: "PlayerName"
identitaet:
  wer_bist_du: "Who is this character"
  aussehen: "Physical description"
  alter: ""
  herkunft: "Background"
skills:
  - name: "Skill Name"
    beschreibung: "What it does"
motivation:
  will: "Personal goal"
  fuerchtet: "Fear"
  geheimnis: "Secret"
beziehungen:
  begleiter: "Other party members"
  nscs: []
zustand:
  verletzt: false
  erschoepft: false
  notizen: ""
# CONTENT PREFERENCES (Booktok flag)
praefereenzen:
  wishes:
    - slow_burn
    - dark_protector
  no_gos:
    - cheating
  custom_wishes: ""
  custom_no_gos: ""
imagen_prompt: "Portrait prompt for Imagen"
```
---
## 4. Quest Backlog System
**Problem:** DM forgets main plot/quest during long sessions
**Solution:** Internal quest tracking in `session.yaml`
### Data Structure
```yaml
session: 1
status: pausiert
quest_backlog:
  hauptquest:
    name: "Name of main quest"
    beschreibung: "What is the quest"
    status: aktiv  # aktiv / geloest / fehlgeschlagen
    detail: "Current specifics"
  nebenquests:
    - name: "Side quest 1"
      beschreibung: ""
      status: aktiv
    - name: "Side quest 2"
      beschreibung: ""
      status: aktiv
```
### Quest Lifecycle
1. **Quest entsteht** → Immediately save to quest_backlog
   - Name + description
   - Status: aktiv
2. **Quest geloest** → Update status to "geloest"
   - Keep in backlog for reference
   - Add completion note
3. **Quest fehlgeschlagen** → Update status to "fehlgeschlagen"
4. **DM nudge** → When players drift, reference quest_backlog:
   - "Eure Aufgabe ist..."
   - "Ihr habt versprochen..."
   - "Die Zeit laeuft ab..."
---
## 5. Content Preferences System
**Flag:** booktok (and similar flags)
### Collection Flow (Private Channel)
1. DM sends CONTENT_PREFERENCES.md to player
2. Player goes through category list: Wish / Neutral / No-Go
3. Player provides custom wishes/no-gos
4. DM stores in `characters/[player].yaml`
### Calculation (DM process)
After ALL players submitted preferences, DM calculates:
```yaml
# Stored in adventure yaml after calculation:
player_preferences:
  berechnet:
    erlaubt:
      # Everything EXCEPT items marked as no-go by ANY player
      - [list of allowed themes]
    aktiv_foerdern:
      # Only themes that:
      # - appear in at least one player's wishes
      # - AND are not in ANY player's no-gos
      - [list of themes to actively include]
```
### Calculation Logic
```
For each theme in global_theme_list:
  IF theme is in ANY player's no_gos:
    NOT erlaubt
  ELSE IF theme is in ANY player's wishes:
    erlaubt AND aktiv_foerdern
  ELSE:
    erlaubt (but not actively promoted)
```
---
## 6. Flag System
### What are Flags?
Flags modify the DM rules based on adventure type. When a flag is set in `setting.yaml`, the corresponding add-on rules apply.
### Flag Naming Convention
- lowercase
- underscore for spaces: `mature_content`, `booktok`
### How Flags Work
1. Set in `setting.yaml`:
   ```yaml
   flags:
     - mature_content: true
     - booktok: true
   ```
2. DM loads flag add-ons from `_engine/flags/[flag_name]/`
3. Flag-specific DM rules OVERRIDE default rules for that adventure
### Flag Files
Each flag can have:
- `[flag_name]/DUNGEON_MASTER.md` - Play rules
- `[flag_name]/SESSION_ZERO.md` - Session 0 rules
- `[flag_name]/CHARACTER_SETUP.md` - Character creation / setup questions
- `[flag_name]/CONTENT_PREFERENCES.md` - Preference categories
### Default Fallback
If no flag-specific file exists, use default from `_engine/`
---
## 7. Session Flow Summary
```
[Player joins]
      ↓
DM → Private: Einladung + Beschreibung + Trigger Warnings
      ↓
[Player Consent]
      ↓
DM → Private: Charakter-Erstellung
      ↓
[All players ready]
      ↓
DM → Group: Session 0 Szene (First Scene + Image)
      ↓
[Session 0 complete]
      ↓
DM → Group: Regular Play
      ↓
[Each session: DM updates session.yaml with quest_backlog]
      ↓
[Session end: DM updates status.yaml]
```
---
## 8. DM Loading Order
When starting a session, DM loads files in this order:
1. **Always:** `TOP_DM_REGELN.md` - Core rules
2. **Phase-specific:**
   - Character Setup: template + flag add-on if exists
   - Session 0: `SESSION_ZERO.md` + flag add-on if exists
   - Regular Play: `DUNGEON_MASTER.md` + flag add-on if exists
3. **Adventure-specific:**
   - `setting.yaml` - World and flags
   - `characters/*.yaml` - All player characters
   - `npcs.yaml` - Known NPCs
   - `session.yaml` - Current state + quest_backlog
---
## 9. Templates
### Character Template
See: `ttrpg/__engine/templates/character.yaml`
### Adventure Setup Template
See: `ttrpg/_engine/templates/adventure.yaml`
---
## 10. Future Considerations
- Player private channel for help during play
- Meta vs story separation in group channel
- Session pause/resume flow
- Multiple adventures parallel support