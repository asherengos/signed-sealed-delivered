# Demo plan — Signed, Sealed, Delivered (DRAFT, not recorded)

Status: plan only. No video has been recorded, no demo post has been
published, and no prototype step below has been verified yet. Every
shot that depends on a built prototype must be re-checked against
the built prototype before recording; do not record a shot that
claims a feature the prototype does not demonstrate.

Rules that bind this plan (from HACKATHON.md, rechecked 2026-10-31):

- The demo must be a VIDEO. Q-012: screenshots alone are not enough
  when judges cannot open the demo. A local-only demo is OK with a
  public repo, a reproducible README, and an X post with a video.
- The X post must say the project was built at NEAR HACKATHON and
  tag @NEARProtocol and #NEARHackathon (optionally also @NearLegion
  and @NearBuilders).
- A good demo post, per HACKATHON.md: lead with the user problem,
  show one complete moment (real user action to visible result),
  explain NEAR's role concretely, give a next step (demo and repo
  links, genuine question or invitation for feedback). Skip long
  intros, architecture slides, and setup.
- Hosted demo is optional, not required. If one is ever hosted,
  keep it up to 2026-11-18, ideally 2026-11-25. None is planned
  in this draft.
- Testnet only. Every payment screen must label testnet. Testnet
  tokens have no real value, and the demo must say so.
- No seed phrase, private key, credential, or full-access key on
  screen, in narration, or in captions, at any point.
- Demo data, if any, must be labeled as sample. Do not present a
  simulated result as a real result.
- Intents and Chain Signatures are future work only. Do not show
  or narrate them as implemented.
- Adam records and publishes the demo post himself. Drafting help
  only (see `x-announcement-draft.md`).

## The one complete moment (the whole video is built around this)

A human posts a task with rules and a cap. An agent does the
verifiable task. Verify-atom issues a signed, timestamped attestation
with evidence. The payment gate checks the attestation and the rules.
Only then does a NEAR testnet payment release — and the screen says
TESTNET at that moment.

That is the only story the video needs to tell. If a shot does not
serve that moment, cut it.

## Shot plan (target: short; exact runtime TO-FILL after recording)

Shot 0 — Problem, one line (a few seconds, text on screen):
  "An agent that can pay should have to prove it did the work first."
  No setup, no intro slides beyond this line.

Shot 1 — Human sets the task and the rules:
  Show the task being posted with its rules and cap, in plain
  language. Do not show any credential, key, or account secret.
  Narration line (draft): "A human posts a task, with rules and a cap."

Shot 2 — Agent does the verifiable task:
  Show the agent completing the task and the evidence it produces.
  Only show tasks the prototype actually builds. TO-FILL: the exact
  demo task, once built and verified.

Shot 3 — Attestation:
  Show the signed, timestamped verify-atom attestation with its
  evidence. Point to what a judge can check: signature, timestamp,
  evidence. Do not claim an attestation the prototype does not issue.

Shot 4 — Gate check, then release:
  Show the gate checking the attestation against the rules, then
  the testnet payment releasing, with TESTNET labeled on screen.
  Narration line (draft): "Proof checks out, rules check out, so
  the testnet payment releases. No proof would mean no payment."

Shot 5 — Blocked case (only if the prototype actually shows it):
  Show a payment blocked with its stated reason — for example,
  no proof, or over cap — with the reason on screen. Name only
  block reasons the built prototype actually produces. If the
  prototype does not produce a blocked case, cut this shot and do
  not claim one.

Shot 6 — Close, one line (a few seconds, text on screen):
  "Built at NEAR HACKATHON. Testnet only. No real money."
  Plus the repo link on screen only once the repo is public
  (TO-FILL until then).

## What must NOT appear in the video

- Any seed phrase, private key, or credential.
- Any full-access key, or any screen showing key management.
- Any mainnet account, mainnet payment, or real-money claim.
- Any claim that Intents or Chain Signatures are implemented.
- Any contract address, method name, token amount, gas amount, or
  account name that has not been verified from the built prototype.
- Any simulated result presented as a real result, or any demo
  data presented without a sample label.

## Recording checklist (before Adam publishes)

- [ ] Every shot re-checked against the built prototype; no shot
      claims an unbuilt feature.
- [ ] TESTNET labeled on every payment screen.
- [ ] No secret on screen, in narration, or in captions.
- [ ] Video, not screenshots alone, attached to the X post.
- [ ] X post text checked against `x-announcement-draft.md`:
      says built at NEAR HACKATHON, tags @NEARProtocol and
      #NEARHackathon, links repo and demo only once both exist.
- [ ] Repo link and demo post link verified from a signed-out
      browser before the submission payload is finalized.
- [ ] Adam publishes the post himself and supplies the link.
      Nobody posts on his behalf without his explicit confirmation
      for that step.
