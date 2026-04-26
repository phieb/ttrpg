# TTRPG Engine Architecture

## Overview

Three-phase DM system driven by Claude API. Character creation happens privately before group play begins.

---

## 1. The Three DM Phases

| Phase | Channel | Prompt file |
|-------|---------|-------------|
| **CHARACTER_SETUP** | Private DM ↔ Player (1:1) | `_engine/CHARACTER_SETUP.md` |
| **SESSION_ZERO** | Group channel | `_engine/DUNGEON_MASTER.md` (session_zero section) |
| **DUNGEON_MASTER** | Group channel | `_engine/DUNGEON_MASTER.md` |

### Phase 1: Character Setup (Private)
Each player gets a dedicated 2-member Signal group (bot + player) per adventure.

**Flow:**
1. `!new` creates the play group + one private setup group per player
2. Bot sends opening message via `CHARACTER_SETUP.md`
3. Species question (if species flavour active or `verfuegbare_spezies` set in setting.yaml)
4. Character development questions (one at a time)
5. Content preferences: no-gos always, wishes always, flavour-extended if applicable
6. Player signals ready → bot extracts character data → generates avatar
7. When all players ready → adventure moves to `session_0`

**Output:** `characters/[player_name].yaml` with full character + `praeferenzen` block

### Phase 2: Session 0 (Group)
**When:** All players have completed private character setup (`setup_status: ready`)

**Flow:**
1. DM introduces characters into the world
2. Scene image generated
3. Intro scene, relationship building, quest hook
4. `!session0` triggers this phase explicitly

### Phase 3: Regular Play (Group)
**When:** Session 0 complete, adventure status `aktiv`

Standard DM loop: describe → NPCs act → players decide → resolve → repeat.
`!save` compresses history → updates `session.yaml` → clears `spielprotokoll.jsonl`

---

## 2. File Structure

```
ttrpg/
├── _engine/
│   ├── ARCHITECTURE.md           # This file
│   ├── TOP_DM_REGELN.md          # Core rules (always loaded)
│   ├── DUNGEON_MASTER.md         # Regular play + Session 0 DM rules
│   ├── CHARACTER_SETUP.md        # Private 1:1 character creation
│   ├── templates/
│   │   ├── character.yaml
│   │   ├── setting.yaml
│   │   ├── npcs.yaml
│   │   └── session.yaml
│   └── flavours/                   # built-in only — addons are mounted here via Docker
│       ├── fantasy/
│       │   └── CHARACTER_SETUP.md    # human, elf, dwarf, halfblood, witch/warlock
│       ├── mythical/
│       │   └── CHARACTER_SETUP.md    # human, vampire, werewolf, nymph/fae, shapeshifter
│       └── historical/
│           └── CHARACTER_SETUP.md    # human only; stand/herkunft replaces species
├── players/
│   └── [Name].yaml               # Global player registry
├── status.yaml                   # Adventure overview + Signal group IDs
├── status.example.yaml
└── adventures/
    └── [adventure-name]/
        ├── setting.yaml          # World, atmosphere, flavours, verfuegbare_spezies
        ├── session.yaml          # Current state, quest backlog
        ├── npcs.yaml
        ├── spielprotokoll.jsonl  # Crash-safe log, cleared on !save
        └── characters/
            ├── [player].yaml
            └── [player]_avatar.png
```

---

## 3. Flavour System

Flavours are set in `setting.yaml` at `!new` time via `--flavour`:

```yaml
flavours:
  booktok: true
  fantasy: true   # or: mythical, historical
```

The bot loads `_engine/flavours/[flavour]/[PHASE].md` for each active flavour when building
the system prompt for that phase. If no file exists for a flavour+phase combination, it is
silently skipped.

Each flavour can have an optional `manifest.yaml` declaring dependencies:
```yaml
description: "Human-readable description shown by !flavours"
requires:
  - other-flavour
```

**Addons:** drop any flavour folder into `_engine/flavours/` via a Docker volume mount —
the bot picks it up automatically. No registration or code change needed.

### Addon bauen

Ein Addon ist ein eigenes Git-Repo mit einem `flavours/` Ordner. Jeder Flavour darin
ist ein Unterordner mit optionalen Dateien je nach Phase:

```
mein-addon/
  flavours/
    mein-flavour/
      DUNGEON_MASTER.md       ← in DM-System-Prompt injiziert
      CHARACTER_SETUP.md      ← injiziert während Charaktererstellung
      SESSION_ZERO.md         ← injiziert während Session Zero
      CONTENT_PREFERENCES.md  ← injiziert bei Content-Präferenz-Fragen
      CHARACTER_FIELDS.yaml   ← zusätzliche Charakterblatt-Felder
      manifest.yaml           ← Beschreibung + requires
```

**`manifest.yaml`:**
```yaml
description: "Kurze Beschreibung — erscheint bei !flavours"
requires:
  - anderer-flavour   # wird automatisch aktiviert wenn dieser Flavour aktiv ist
```

**`CHARACTER_FIELDS.yaml`:**
```yaml
fields:
  - key: zustand.mein_feld
    required: false     # true = Pflichtfeld für vollständiges Charakterblatt
    detail: full        # full = Wert wird exakt übernommen, nicht zusammengefasst
```

**Docker einbinden** (in `docker-compose.yml` von ttrpg-signal):
```yaml
volumes:
  - /pfad/zu/mein-addon/flavours/mein-flavour:/mnt/ttrpg/_engine/flavours/mein-flavour
```

Referenzimplementierung: [ttrpg-flavour-horror](https://github.com/phieb/ttrpg-flavour-horror)

### Species flavours

| Flavour | Available species |
|---------|------------------|
| `fantasy` | human, elf, dwarf, halfblood, witch/warlock |
| `mythical` | human, vampire, werewolf, nymph/fae, shapeshifter |
| `historical` | human only (species replaced by stand/herkunft) |
| *(none)* | human only |

`verfuegbare_spezies` in `setting.yaml` overrides all of the above with a custom list.

`booktok` stays human-only unless a species flavour is also active.

---

## 4. Character Data Model

`adventures/[name]/characters/[player].yaml`

```yaml
charakter:
  name: ""
  gespielt_von: ""
identitaet:
  wer_bist_du: ""
  aussehen: ""
  alter: ""
  herkunft: ""
skills:
  - name: ""
    beschreibung: ""
motivation:
  will: ""
  fuerchtet: ""
  geheimnis: ""
beziehungen:
  begleiter: ""
  nscs: []
zustand:
  verletzt: false
  erschoepft: false
  notizen: ""
praeferenzen:
  no_gos: []
  wishes: []
  # [addon-specific fields appear here when an addon flavour is active]
imagen_prompt: ""
```

---

## 5. Quest Backlog

Tracked in `session.yaml`:

```yaml
quest_backlog:
  hauptquest:
    name: ""
    beschreibung: ""
    status: aktiv   # aktiv / geloest / fehlgeschlagen
    detail: ""
  nebenquests:
    - name: ""
      beschreibung: ""
      status: aktiv
```

---

## 6. Adventure Lifecycle

```
!new → setup
  ↓ (all players setup_status: ready)
session_0
  ↓ (!session0 complete)
aktiv
  ↓ (!save)
pausiert  →  aktiv (on next session)
```

Player entry in `status.yaml`:
```yaml
spieler:
  - name: "PlayerName"
    nummer: "+43..."
    setup_status: invited   # invited / ready
    private_gruppe: ""      # Signal group ID for setup channel
```

---

## 7. Open / Planned

- Private player→DM command during active play
- Trigger warnings as configurable template (default vs flavour-specific)
- Epilogue / adventure conclusion flow
- How a second player joins a scene already in progress
