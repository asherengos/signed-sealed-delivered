# NEAR demo shots — filled from the built local prototype, 2026-11-04

Source: prototype/demo.sh output, verified 2026-11-04.
Original demo-plan.md is unchanged; this file fills its TO-FILL
shots with the actual built demo values. Nothing here claims a
real NEAR payment.

## Filled shots
- Shot 2 — exact demo task: count the words in the sample
  sentence "An agent that can pay should have to prove it did
  the work first." Result: 14 words, recomputable as
  len(sentence.split()). Task id: task-001-SAMPLE.
- Shot 4 — gate release: valid signed attestation for this task,
  amount 5 SAMPLE units, cap 10 SAMPLE units. Decision:
  RELEASED, labeled TESTNET, SAMPLE. Simulated only — no real
  NEAR payment is sent.
- Shot 5 — blocked cases, all actually produced by the prototype:
  (a) no proof: no attestation supplied, BLOCKED;
  (b) over cap: 99 SAMPLE units exceeds cap 10, BLOCKED;
  (c) tampered attestation: signature INVALID, BLOCKED.
- Shot 6 — close line, plus repo link TO-FILL until repo is
  public: "Built at NEAR HACKATHON. Testnet only. No real money."

## Recording rules that still bind
- Every payment screen labeled TESTNET and SAMPLE.
- No seed phrase, private key, credential, or full-access key
  on screen, in narration, or in captions. Demo keys are
  prototype/keys/ only, gitignored, never shown.
- No mainnet account, mainnet payment, or real-money claim.
- No Intents or Chain Signatures claimed.
- No contract address, method name, token amount, gas amount,
  or account name — amounts are abstract SAMPLE units only.
- Demo data labeled SAMPLE. Simulated result never presented
  as a real result.
- Owner publishes the video and the X post himself, with tags
  @NEARProtocol and #NEARHackathon, saying built at NEAR
  HACKATHON, linking repo and demo only once both exist.
