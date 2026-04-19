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
3. Species question (if species flag active or `verfuegbare_spezies` set in setting.yaml)
4. Character development questions (one at a time)
5. Content preferences: no-gos always, wishes always, flag-extended if applicable
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
│   └── flags/
│       ├── mature_content/
│       │   ├── DUNGEON_MASTER.md
│       │   └── CHARACTER_SETUP.md
│       ├── booktok/
│       │   ├── DUNGEON_MASTER.md
│       │   ├── CHARACTER_SETUP.md
│       │   └── CONTENT_PREFERENCES.md
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
        ├── setting.yaml          # World, atmosphere, flags, verfuegbare_spezies
        ├── session.yaml          # Current state, quest backlog
        ├── npcs.yaml
        ├── spielprotokoll.jsonl  # Crash-safe log, cleared on !save
        └── characters/
            ├── [player].yaml
            └── [player]_avatar.png
```

---

## 3. Flag System

Flags are set in `setting.yaml` at `!new` time:

```yaml
flags:
  - mature_content
  - booktok
  - fantasy        # or: mythical, historical
```

The bot loads `_engine/flags/[flag]/[PHASE].md` for each active flag when building the system prompt for that phase. If no file exists for a flag+phase combination, it's silently skipped.

### Species flags

| Flag | Available species |
|------|------------------|
| `fantasy` | human, elf, dwarf, halfblood, witch/warlock |
| `mythical` | human, vampire, werewolf, nymph/fae, shapeshifter |
| `historical` | human only (species replaced by stand/herkunft) |
| *(none)* | human only |

`verfuegbare_spezies` in `setting.yaml` overrides all of the above with a custom list.

`booktok` stays human-only unless a species flag is also active.

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
  # mature_content_grenzen: []
  # booktok_no_gos: []
  # booktok_wishes: []
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
- Trigger warnings as configurable template (default vs flag-specific)
- Epilogue / adventure conclusion flow
- How a second player joins a scene already in progress
