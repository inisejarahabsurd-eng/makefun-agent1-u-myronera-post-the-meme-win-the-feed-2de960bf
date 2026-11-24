[![make.fun bounty](https://make.fun/badge/u-myronera-post-the-meme-win-the-feed-2de960bf.svg)](https://make.fun/bounty/u-myronera-post-the-meme-win-the-feed-2de960bf?utm_source=github&utm_medium=readme&utm_campaign=u-myronera-post-the-meme-win-the-feed-2de960bf)
[![rank](https://make.fun/badge/u-myronera-post-the-meme-win-the-feed-2de960bf/inisejarahabsurd-eng/makefun-agent1-u-myronera-post-the-meme-win-the-feed-2de960bf/rank.svg)](https://make.fun/bounty/u-myronera-post-the-meme-win-the-feed-2de960bf?utm_source=github&utm_medium=readme&utm_campaign=u-myronera-post-the-meme-win-the-feed-2de960bf)
[![reward](https://make.fun/badge/u-myronera-post-the-meme-win-the-feed-2de960bf/inisejarahabsurd-eng/makefun-agent1-u-myronera-post-the-meme-win-the-feed-2de960bf/reward.svg)](https://make.fun/bounty/u-myronera-post-the-meme-win-the-feed-2de960bf?utm_source=github&utm_medium=readme&utm_campaign=u-myronera-post-the-meme-win-the-feed-2de960bf)

# Post the Meme, Win the Feed — Entry

Agent-generated meme about make.fun for AI agent builders, posted on X with `@_myronera` and a make.fun play code in the post text.

## What this repo does

1. **Generates the meme image** (`generate_meme.py`) — pure Python + Pillow, no external assets. Renders a 1080x1350 phone-legible meme: bold Impact-style top/bottom text over a drawn agent-robot graphic. Multiple templates and jokes selectable via CLI.
2. **Builds the post text** (`post_text.py`) — writes `out/post_text.txt` containing `@_myronera`, the play code, and short meme copy. Validates constraints.
3. **Validates everything** (`validate_entry.py`) — image exists, dimensions/format, post text contains `@_myronera` and the play code, text length fits X, no accidental secrets in `out/`.
4. **Entrypoint** (`cli/makefun.mjs`) — runs the full pipeline; `node cli/makefun.mjs bundle` delegates to the official make.fun kit CLI if present (run from the unpacked kit for transcript bundling).

## Meme

Template `grind`: an agent robot at a terminal, glowing leaderboard, text:

> TOP TEXT: AGENT GRINDS BOUNTIES ALL NIGHT
> BOTTOM TEXT: GETS PAID IN CRYPTO. WORTH IT.

Short, spelled correctly, readable at phone size (min 72pt Impact-style bold).

Other templates: `paid`, `leaderboard`, `bugs` — see `jokes.py`.

## Usage

```bash
pip install -r requirements.txt
node cli/makefun.mjs run --joke grind --play-code MF-XXXX-XXXX
# outputs:
#   out/meme.png        (1080x1350 PNG, <5MB)
#   out/post_text.txt

python validate_entry.py --image out/meme.png --text out/post_text.txt --play-code MF-XXXX-XXXX
```

## Posting (manual step, by the entrant)

1. Verify the generated image and post text.
2. Post from the entrant's **public** X account at/after the bounty opening, before the deadline.
3. Post text must contain `@_myronera` and a valid make.fun play code.
4. Attach `out/meme.png` as the image.
5. Keep the post up. Do not buy engagement, use bots, pods, or fake accounts — disqualification risk. Organic reach only.
6. Record the post URL in `out/post_url.txt`.

## Transcript bundle (required by make.fun)

Run from the **unpacked official kit**, not from this repo:

```bash
node cli/makefun.mjs bundle \
  --session <harness-session-log.json> \
  --redact "<full name>" --redact "<phone number>"   # only personal details judging doesn't need
node cli/makefun.mjs check <bundle.tar.gz>
```

- Bundle the top-level session plus every subagent/worker session, whole, unchanged harness logs.
- Redact only personal details (name, e-mail, phone, address, DOB, ID/bank numbers). Never redact code, shipped files, commands, tool output, or reasoning — that can disqualify the entry.
- Never hand-write or summarise sessions from memory. Upload harness logs as saved.

## Submission fields

- `repo_url`: this GitHub repo (`https://github.com/<owner>/<repo>`)
- `commit_sha`: full 40-char sha of the entered commit, on a branch
- `bundle`: the kit-produced `.tar.gz` transcript bundle
- Meme asset: `out/meme.png`; post text: `out/post_text.txt`

## Edge cases handled

- Text auto-wraps and auto-shrinks to fit the canvas; refuses to render unreadably small.
- Image compressed under X's 5MB upload limit (PNG optimized, JPEG fallback).
- Post text validated: mentions, play-code format, length under 280 chars.
- Deterministic rendering (seeded), so the commit reproduces the exact asset.
- `validate_entry.py` fails non-zero with clear messages on any violation.
- No network calls in the generator — fully offline, reproducible.

## Files

- `cli/makefun.mjs` — entrypoint (run / bundle delegate)
- `generate_meme.py` — image renderer
- `jokes.py` — copy deck
- `post_text.py` — post text builder
- `validate_entry.py` — entry checker
- `run_pipeline.py` — orchestrator
- `requirements.txt`

## License

MIT.