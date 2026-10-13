---
name: linkedin-agent
description: Draft LinkedIn posts about this project (MGA Mobile) from recent git history and project docs. Use when the user runs /linkedin-agent or asks for a LinkedIn post, announcement, or update about the work in this repo. Takes an optional topic, language (fr/en), and tone as arguments.
---

# LinkedIn agent

Draft ready-to-paste LinkedIn posts about the work in this repository.
This skill only drafts text: it never posts to LinkedIn, and it never invents
features, numbers, clients or results that the repo does not show.

## Arguments

`/linkedin-agent [topic] [lang=fr|en] [tone=pro|casual|technical] [n=1..3]`

- **topic**: what the post is about (e.g. "sprint 1", "deployment", a commit
  range). If omitted, use the most recent meaningful work in git history.
- **lang**: default `fr` (the project docs are in French). `en` on request.
- **tone**: default `pro`.
- **n**: number of variants to draft, default 2.

## Steps

1. **Gather facts** (read only, keep it short):
   - `git log --oneline -20` and, for the chosen topic, `git show --stat <sha>`.
   - Skim the relevant parts of `ARCHITECTURE.md`, `DEPLOYMENT.md`,
     `MOBILE_DEPLOYMENT.md`, `backend/` and `mobile/` only as far as needed.
   - Note concrete, verifiable facts: stack (React Native/Expo, FastAPI,
     Postgres, Dolibarr integration), what shipped, what problem it solves.
2. **Check for confidential details** before writing. Leave out internal
   hostnames, API keys, client data, credentials, internal URLs and anything
   from `.env` files. Name the client or company (e.g. MG Assistances) only if
   the user confirms that is fine; otherwise say "un client" / "a client".
3. **Draft** `n` variants following the format rules below.
4. **Save** the drafts to `linkedin/drafts/YYYY-MM-DD-<slug>.md` in the repo
   (create the folder if needed) and show them in the reply. Do not commit
   unless the user asks.
5. **Ask** once whether the user wants changes (shorter, other tone, other
   language, mention the client by name).

## Post format

- **Hook** (first 1–2 lines, under ~200 characters): this is all that shows
  before "voir plus" / "see more", so lead with the outcome or a sharp
  observation, not "Je suis heureux d'annoncer…".
- **Body**: 3–6 short paragraphs or a short list. What was built, why it
  matters, one technical detail people in the field will appreciate, one
  lesson learned.
- **Close**: one question or call to action to invite comments.
- **Hashtags**: 3–5 relevant ones at the end (e.g. #ReactNative #FastAPI
  #Dolibarr #MobileDev #CRM).
- Length: 120–250 words. Plain text: no markdown headings, no bold (LinkedIn
  does not render it). Emoji: at most 2–3, only if tone is not `technical`.
- First person, active voice, concrete nouns. No buzzword stacks
  ("synergie", "game-changer", "révolutionnaire").

## Output template

```
--- Variante 1 (<angle>) ---
<post text>

--- Variante 2 (<angle>) ---
<post text>
```

Give each variant a different angle (e.g. product outcome vs. technical
architecture vs. lessons learned).
