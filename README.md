# Playwriting skill

A skill for Claude that helps write, diagnose and revise stage plays: one-acts, full-lengths, ten-minute plays, scenes and monologues.

It looks for what each person wants from the other person onstage before it touches a line, keeps the writer's own formatting, and checks its own drafts before handing them over.

## What it does

- Reads a script cold and reports what's working and what isn't, scene by scene.
- Revises with a plan: what to keep, what to question, what it invented.
- Watches for common faults: characters reporting feelings, talking out front, trading perfect comebacks, choppy dialogue, too many stage directions.
- Checks that a play can be staged: props, costumes, entrances, quick changes, a small set, no crew.
- Builds a new Word file in the look of the writer's original. The original is never changed.

## Install

Copy the `playwriting` folder into your skills folder:

```bash
git clone https://github.com/PaoloCiara/playwriting-skill.git
mkdir -p ~/.claude/skills
cp -R playwriting-skill/playwriting ~/.claude/skills/
```

Start a new session and ask about a play, or type `/playwriting`.

## Scripts

All run offline with Python 3 and nothing else to install.

| Script | Use |
|---|---|
| `read_play.py PLAY` | Counts, rhythm and lines worth a second look, from a .docx or .txt |
| `build_play.py ORIGINAL.docx play.txt OUT.docx` | Builds a script in the original's formatting |
| `read_book.js BOOK.pdf OUT.txt` | Saves a PDF's text (macOS only) |

## Make it yours

`references/writer-voice.md` starts empty. The skill fills it with your notes, your formatting and your stage as you work. Keep your filled-in copy private.

## Credits and limits

- The craft checks are restated from Stuart Spencer's *The Playwright's Guidebook*. This project is independent of the author and publisher, includes none of the book's text, and works best alongside your own copy.
- The short list of habits kept from screenwriting was informed by the `scene-writing` skill in `a5c-ai/babysitter`.
- No plays are included. The flags are candidates, not verdicts, and nothing here replaces hearing a script read aloud.
