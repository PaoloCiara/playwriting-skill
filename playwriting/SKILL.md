---
name: playwriting
description: Write, diagnose, revise and format stage plays (one-acts, full-lengths, ten-minute plays, single scenes, monologues). Use whenever the user mentions a play, playwriting, a script for the stage, a one-act, stage directions, a monologue, a staged reading or a production they wrote, or uploads a script with character cues and scenes. Use it for notes like "the dialogue feels stiff", "it's too on the nose", "they just talk at the audience", "the middle drags", "the ending doesn't land", or "make this scene work", even if they don't say "playwriting". Covers what each character wants, conflict, subtext, exposition, direct address, beats, scene order, playable staging and manuscript format. For film or TV screenplays, use scene-writing instead.
---

# Playwriting

A play is people in a room wanting things from each other, watched by people in another part of the same room. Nearly every script problem traces back to one of those halves: the wanting is missing, or the staging ignores the room.

These are tools, not rules. Reach for one when something isn't working. A scene that is alive doesn't need to be fixed to satisfy a checklist, and the play belongs to the writer, not to you.

## Work from what you've been given

Use all four sources every time: the writer's notes (`references/writer-voice.md`), the book, the plays they've shared (`references/from-plays.md`), and their own draft. When they disagree, the writer's notes win, then the writer's draft.

The checks here lean on Stuart Spencer's *The Playwright's Guidebook*. If the writer has a copy and shares it, open `references/guidebook-checks.md`, read the pages it lists for the job, and name them in the report; a summary in this skill doesn't count as having used the book. If they don't have it, use the checks on their own and don't cite pages. Either way, check your own drafts **before** delivering, the same way as the writer's.

## Choose the job

| The user wants | Do |
|---|---|
| Notes or "what's wrong with this?" | Steps 1–2, then report. Don't rewrite. |
| A revision | Steps 1–6 |
| Dialogue fixed, story untouched | Step 1, then Step 4. Say so if the real problem is structural. |
| A new play or scene | `references/getting-unstuck.md` (starting from an image), then Steps 3–6 |
| Help with a reading or audience notes | `references/readings-and-feedback.md` |
| "Check over everything" | `references/full-check.md`, then report; fix if asked to revise |
| Characters, setting or time page | `references/manuscript-format.md`, and the last part of `references/full-check.md` |
| Formatting only | `references/manuscript-format.md` |

Read `references/writer-voice.md` before writing any dialogue for this user. Read `references/craft-tools.md` when a diagnosis needs more than the table below.

## Step 1: Read it cold

Get the text and a first scan:

```bash
python3 -I <skill>/scripts/read_play.py "Play.docx"          # structure, counts, flagged lines
python3 -I <skill>/scripts/read_play.py "Play.docx" --text   # the labelled script
```

Read the whole play before judging any of it. Then answer these in a sentence each. If an answer won't come, that's a finding.

1. **Whose play is it?** Who wants something most?
2. **What does each person want from the other, in this room?** Name something you could hand over, refuse or see happen: a key, a name said aloud, a chair given up. "Love" or "closure" is the want underneath; find the object that carries it.
3. **What stops them?** If both want the same thing, there's no conflict, only noise.
4. **What changes, and who sees it happen?**
5. **Why today?** What makes this day different from the others these people have had?
6. **What is already alive?** List the lines and moments to protect. Do this before listing faults; revision kills good things by accident.

## Step 2: Diagnose, structure before lines

Fix causes in this order. Polishing dialogue in a scene with no want makes a smoother scene that still doesn't work.

| Symptom | Likely cause | Try |
|---|---|---|
| Characters tell each other things both know | Information has no want pushing it out | Give someone a reason to need it now, or have someone else dig for it, or cut it and see if anyone misses it |
| Actors drift out to face the house | Nothing to do to the other person; feelings reported, not pursued | Turn each report into an attempt. Put an object between them |
| Long fight, no movement | Disagreement about the past, not conflict | Find what each needs the other to *do* tonight |
| Nice scene, nobody cares | Little to gain or lose | Closer ties; make this person the only one who can give it |
| Bleak and static | No hope left | Reopen a door the character can believe in |
| One character keeps trying to leave | Their want is offstage | Give them something only this room has |
| Everything clear by page three | No subtext | Let the first want cover a second; hold one fact back |
| Confusing, meant as mysterious | Too little given | Suspense needs information: show the bomb, hide the timer |
| Scenes could be reordered | Episodes, not plot | Make each scene's change cause the next scene's want |
| Ending feels unearned | The obstacle dissolved by itself, or offstage | The people in the play must cause it, where we can see it, at some cost |
| Ending scene is flat | Everyone already agrees | Someone must still be able to say no |
| Every line lands; both people are witty all the time; "too perfect" | Written for the sound of the line instead of the state of the person saying it | Name each person's main emotion in the scene, mark every line that doesn't come from it, replace those (see Step 4) |
| Hero is dull | Over-protected by the writer | Two wants that pull against each other, played one beat at a time |

Report findings by scene, biggest first, each with the line or moment it comes from. Separate what you can show on the page from what's a guess about performance.

## Step 3: Agree the choices

Every given is a choice: the place, the hour, who enters first, the gap between scenes. Before rewriting, write down:

- **Keep:** story, characters, title, protected lines, and their page formatting.
- **Question:** two or three givens that may be causing the trouble.
- **Invent:** any new fact about the characters' past.

If the user gave creative freedom, go ahead and list the inventions at the end. Otherwise ask first about inventions and anything that changes the ending.

Make a card for each scene before writing it:

```
SCENE / where, when, time since the last scene
A wants (object):            underneath:
B wants (object):            underneath:
In the way:
Tactics in order (beats):    1.   2.   3.   4.
What changes (from → to):    whose mind changes:
What the audience learns:    what it still wants to know:
Exit that makes the next scene necessary:
```

A scene with fewer than three tactics is probably one long beat. A card whose "from → to" is blank isn't a scene yet.

## Step 4: Write it, then do the line pass

Draft freely first; feeling lines are allowed in a draft because they tell you what the line should do. Then go through every line:

- **Report or attempt?** "I feel like you don't trust me" reports. "Then give me the car keys" attempts. Keep the attempt; the report is usually implied.
- **Does it answer, or pursue?** People dodge and trade, but a dodge still shows they heard. Let a question go unanswered when the silence is the answer, not to skip to the next topic.
- **Does the next line hear it?** Each line should do something to the one after. Point to the word or act in the line above that set this one off. If there isn't one, it's a jump.
- **Who already knows this?** If both do, it needs a reason to be said.
- **Would they have this line ready, right now?** Nervous, hurt and cornered people mishear, over-explain logistics, give a boring answer, repeat themselves, start over, say the wrong thing, go quiet. A comeback is only right when having one ready is the point.
- **Whose word is it?** Cover the names. If you can't tell who's talking, fix the wants before the vocabulary.
- **Could an object, a pause or an exit say it?**

Don't sterilise. A bald line can be the best in the play if a character is driven to it and it costs something. Allow about one such line per character per play, and build to it.

> Report: "You treat me like a child, and it makes me feel like you don't trust me."
> Attempt: "Give me the car keys." / "It's raining." / "I know it's raining. I'm standing in it."

**Too perfect is a fault too.** Turning every report into a jab swaps explaining for quipping; both are the writer talking. This skill's own drafts do it, so check for it every time:

- Ration the clean hits: three or four a scene, kept for where they cost something. Follow each with a plain line or nothing.
- Give each person a different relation to wit. One may be quick; then the other is literal, slow, sincere. Quickness should fail when they're scared.
- Don't trade quips for tics. If both people now stumble and apologise the same way, the draft has lost their characters. The quick one stays quick; the wit just stops working.
- Let a joke die, a question get no answer, a good line be left unsaid: "Because if she comes in here, I'll—" / "Is that the bus?"
- Let the room interrupt only with something already onstage that changes what they're doing (the phone, the drink). Passing trucks and errands are noise.
- Vary turn length. Don't swap snappy volleys for flat ones ("Okay." "Yeah." "What?"), and don't sprinkle "um" for texture.
- Cut echoes that come back too neatly.

**Direct address** is a choice, not a fault. If it's used, decide who the audience *is* to the speaker (jury, congregation, the dead brother), what the speaker wants from them, and set the rule early. If it wasn't intended, remove the conditions that cause it: speeches with no target, facts with no want, chairs facing front.

**Jumping around is a fault.** Invented details don't make talk sound natural; staying on something does. This skill's drafts have filled scenes with them, so check every time (160–165):

- List the topics in order, a word or two each. A short scene holds one spine and three or four topics under it. More than about six is a warning.
- Between each pair, name the line that turned one into the next. No line, cut the second topic or write the turn.
- Cut any fact that's mentioned once and never used: a hobby, an errand, a minor name, an object nobody touches.
- Ask of each person at each line: what are they trying to find out or get right now? If the answer changed, what changed it?
- Come back to the spine. A scene about the car keys ends on the car keys.

**Choppy is a fault.** Run the rhythm check. When most turns are eight words or fewer, the scene is trading lines instead of talking. Join thoughts with "and", "so", "because"; let an answer run past its question; keep a subject going; save the volley for the moment someone is cornered. `references/from-plays.md` has the method and comparison numbers. Compare with the writer's own draft too: if a revision's turns are much shorter than theirs, the revision caused it.

## Step 5: Stage it

Film can cut; the stage has to get there. Check:

- **Eyes:** at every moment, can the actor look at a person or touch a thing?
- **Business:** each scene has a physical job under the talk (packing, eating, counting). It should get harder to do as the scene does.
- **Transitions:** what one scene leaves onstage should start the next. Prefer changes done in view, one garment or prop at a time. Trace each costume and prop from scene to scene.
- **Entrances and exits:** every one has a reason; note what the person has just come from.
- **Directions must be playable.** Write what can be seen or heard. "She wishes she hadn't come" isn't playable; "She picks up her bag and puts it down again" is. Better still, put the action in the dialogue so it can't be skipped. Leave actors room: cut directions that tell them how to say a line.
- **Budget:** cast size, set, smoking, food, weapons, intimacy, running time.
- **Directions on a diet.** Set the scene once at the top, then write only entrances, exits, handovers and touches. Keep "(Beat.)" for a silence that changes something. Aim for directions at about a quarter of the spoken words or less. See `references/from-plays.md`.
- **The set they really have.** Read `writer-voice.md` for it before inventing anything. If it isn't known, ask for no more than the writer's own draft asked for, and say so. A new door, window, sign, vehicle, second entrance or quick change is a cost the writer pays, so list each one you added and cut it unless the scene can't happen without it. Small objects the back row can't read need to be said aloud or made bigger.
- **Run it with no crew.** Go through the directions alone and write down, per scene, where every prop and garment is at the start and the end, who moved it, and how many seconds the actor has offstage. If a prop can stay onstage for the whole play, let it. If two people who can't be in the same time have to swap something, let them do it in view.

From screenwriting, keep: enter late and leave early, a change in every scene, visual evidence over statement, subtext, an exit hook, the cut-any-line test. Leave behind: sluglines, transitions, montage, intercutting, camera thinking.

## Step 6: Check it cold, then deliver

Work through `references/full-check.md`. Run `read_play.py` on the new draft and compare counts with the old one. Flags are candidates, not verdicts. Then read it through and ask:

- Have the guidebook checks been run on *this* draft, line by line for the lead?
- Did the biggest problem from Step 2 actually go away, or did it move?
- Does someone in every scene still have the power to say no?
- Does the main obstacle break onstage?
- **Too neat?** Count repeated lines and returning props. Three or so strong echoes land; a dozen start to look like the writer's hand. Cut the cleverest ones first.
- **Too quick?** Compare the RHYTHM line with the writer's own draft: average turn length, longest run of short turns, share that stumble. Roughening adds words, so trim after.
- Do facts, dates, props, keys and costumes hold up across scenes? Does anyone quote a line that was never said?
- Are the protected lines still there?
- Is it longer? Say by how much, spoken words and direction words separately. When directions pass about two-thirds of the spoken words, or grow much faster than the dialogue, look for moments the dialogue should be carrying.
- Did the fix cause a new fault? Removing explanation from the dialogue often pushes it into the directions.

Build the Word file from the user's own document and keep their formatting exactly: indents, blank lines, where directions sit, what's centred, how scenes start, front matter and costume notes. Don't tidy it, and don't apply the book's or any house layout to it; theirs wins. Always build from their original, not from an earlier draft of yours, and never overwrite it:

```bash
python3 -I <skill>/scripts/build_play.py --describe original.docx     # learn their formatting first
python3 -I <skill>/scripts/build_play.py original.docx play.txt "Play (revised).docx"
python3 -I <skill>/scripts/build_play.py --describe "Play (revised).docx"   # should match
```

`build_play.py --help` gives the `play.txt` markup. Report: what wasn't working, what changed by scene, what was invented, what wasn't checked (page breaks, read-aloud). Finish with two or three questions only a reading can answer.

Update `references/writer-voice.md` when the user accepts, rejects or rewrites something, so the next draft starts closer.
