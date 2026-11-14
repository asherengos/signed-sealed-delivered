# Signed, Sealed, Delivered — LOCAL-ONLY prototype

Status: local-only prototype. No NEAR account, no wallet, no key,
no seed phrase, no mainnet, no real testnet call, no spending,
no repo publication, no X post, no submission.

## The one complete moment

From `prep-2026-10-31/demo-plan.md`:

1. A human posts a task with rules and a cap.
2. An agent does a verifiable task and produces evidence.
3. A signed, timestamped attestation is issued for that evidence.
4. A gate checks the attestation and the rules.
5. Only then is a payment RELEASED (labeled TESTNET, SAMPLE)
   or BLOCKED with a stated reason (no proof, over cap).

The demo task is deterministic and independently checkable:
count the words in a fixed sample sentence. Any checker can
recompute the count from the sentence itself.

## Run it

Python 3.11+, standard library only. No pip installs, no network.

```bash
bash demo.sh                 # tests, then the end-to-end demo
python3 -m unittest test_signed_sealed -v
python3 signed_sealed.py demo
```

## Files

- `signed_sealed.py` — task posting, verifiable task, attestation
  issuance and verification, payment gate, demo runner.
- `ed25519.py` — pure-stdlib Ed25519 (RFC 8032) pattern reused
  from the Receipts prototype. Demo only, not production-grade.
- `test_signed_sealed.py` — unit tests (see below).
- `demo.sh` — runs tests, then the demo.
- `.gitignore` — excludes `keys/`, `__pycache__/`, `*.pyc`.
- `keys/` — created on first demo run: a fresh DEMO-ONLY
  keypair. Never publish it, never reuse it for anything real,
  never use a production or verify-atom key here.

## What is demonstrated

- A human task with rules and a cap (cap in abstract SAMPLE
  units, not NEAR, not tokens, not gas).
- A verifiable task with recomputable evidence.
- A signed, timestamped attestation, verified by signature.
- A gate that RELEASES only on a valid attestation within cap,
  labeled TESTNET and SAMPLE.
- A gate that BLOCKS with a stated reason on: no attestation
  ("no proof"), an amount over cap ("over cap"), a tampered
  attestation, and an attestation for a different task.

## What is explicitly NOT demonstrated

- NO real NEAR payment. RELEASED is a simulated local gate
  decision only. This code sends no payment anywhere.
- NO testnet account, NO wallet, NO seed phrase created or used.
- NO real testnet call, NO mainnet, NO real money.
- NO contract address, method name, token amount, gas amount,
  or account name. None is invented here.
- NO Intents, NO Chain Signatures. They are future work only
  and are not claimed as implemented.
- NO repo publication, NO X post, NO submission.

## UNDECIDED for any real testnet call

From `prep-2026-10-31/repo-skeleton/docs/GUARDRAIL-NOTE.md`,
unchanged by this prototype:

- Receiver contract: UNDECIDED
- Method names: UNDECIDED (must be explicit, never blank)
- Allowance: UNDECIDED (sized from measured gas use, never blank)
- Any function-call key stays scoped; the full-access key and
  funds stay with the owner. The owner creates his own testnet
  account, writes down his own seed phrase, and never shares it.

Until the owner decides those values and supplies his own
testnet account, no real testnet step can or should be attempted.
