#!/usr/bin/env python3
"""Signed, Sealed, Delivered — LOCAL-ONLY prototype.

Standard library only. No network, no NEAR account, no wallet,
no seed phrase, no mainnet, no real testnet call, no spending,
no repo publication, no X post, no submission.

The one complete moment (from prep-2026-10-31/demo-plan.md):
  1. A human posts a task with rules and a cap.
  2. An agent does a verifiable task and produces evidence.
  3. A signed, timestamped attestation is issued for that evidence.
  4. A gate checks the attestation and the rules.
  5. Only then is a payment RELEASED (labeled TESTNET, SAMPLE)
     or BLOCKED with a stated reason (no proof, over cap).

SAMPLE labeling — read this before using any output:
  - Every simulated result in this prototype is labeled SAMPLE.
  - Amounts here are abstract SAMPLE units. They are NOT NEAR,
    NOT tokens, NOT gas, and NOT a real payment amount.
  - The RELEASED result is a simulated gate decision, NOT a
    real NEAR payment. No payment is sent by this code.
  - Intents and Chain Signatures are NOT implemented and are
    NOT claimed here. They are future work only.
  - No contract address, method name, token amount, gas amount,
    or account name is invented here. For any real testnet call,
    receiver, methods, and allowance remain UNDECIDED (see README).

Attestation signing reuses the pure-stdlib Ed25519 pattern from
the Receipts prototype (ed25519.py, RFC 8032). The keypair used
here is a fresh DEMO-ONLY keypair in prototype/keys/, gitignored.
It is never a production key, never a verify-atom key, and must
never be used for anything real.

Usage:
  python3 signed_sealed.py demo
  python3 signed_sealed.py demo --out /tmp/ssd-demo.json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ed25519

BASE = os.path.dirname(os.path.abspath(__file__))
KEY_DIR = os.path.join(BASE, "keys")
SEED_PATH = os.path.join(KEY_DIR, "demo_seed.hex")
PUBLIC_PATH = os.path.join(KEY_DIR, "demo_public.hex")

SAMPLE = "SAMPLE"
AGENT_ID = "demo-agent-SAMPLE"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def ensure_keypair():
    """Create a fresh demo-only keypair if none exists."""
    os.makedirs(KEY_DIR, exist_ok=True)
    if os.path.exists(SEED_PATH) and os.path.exists(PUBLIC_PATH):
        with open(SEED_PATH) as f:
            seed = bytes.fromhex(f.read().strip())
        with open(PUBLIC_PATH) as f:
            public = bytes.fromhex(f.read().strip())
        return seed, public
    seed = ed25519.generate_seed()
    public = ed25519.publickey_from_seed(seed)
    with open(SEED_PATH, "w") as f:
        f.write(seed.hex() + "\n")
    with open(PUBLIC_PATH, "w") as f:
        f.write(public.hex() + "\n")
    os.chmod(SEED_PATH, 0o600)
    return seed, public


def post_task(task_id="task-001-SAMPLE",
              description="Count the words in the sample sentence.",
              cap_sample_units=10,
              rules=None):
    """Step 1: a human posts a task with rules and a cap.

    The cap is in abstract SAMPLE units, not NEAR or tokens.
    """
    return {
        "task_id": task_id,
        "description": description,
        "cap_sample_units": cap_sample_units,
        "rules": rules or [
            "Payment releases only with a valid signed attestation.",
            "Payment amount must not exceed the cap.",
            "This is a local SAMPLE demo. No real payment is sent.",
        ],
        "label": SAMPLE,
    }


def do_verifiable_task(task):
    """Step 2: the agent does a verifiable task and produces evidence.

    The demo task is deterministic and independently checkable:
    count the words in a fixed sample sentence. Any checker can
    recompute the count from the sentence itself.
    """
    sentence = "An agent that can pay should have to prove it did the work first."
    evidence = {
        "task_id": task["task_id"],
        "method": "word-count",
        "sample_sentence": sentence,
        "word_count": len(sentence.split()),
        "check": "Recompute len(sentence.split()) to verify.",
    }
    return evidence


def issue_attestation(task, evidence, agent_id=AGENT_ID):
    """Step 3: issue a signed, timestamped attestation for the evidence."""
    content = {
        "task_id": task["task_id"],
        "agent_id": agent_id,
        "evidence": evidence,
        "timestamp": now_iso(),
        "label": SAMPLE,
    }
    seed, public = ensure_keypair()
    signature = ed25519.sign(canonical(content), seed, public)
    attestation = dict(content)
    attestation["signature_hex"] = signature.hex()
    attestation["public_key_hex"] = public.hex()
    attestation["verification_note"] = (
        "Verification proves issuance only: this attestation was "
        "signed with the demo key and is unaltered since signing. "
        "It does not prove a real NEAR payment happened.")
    return attestation


def verify_attestation(attestation):
    """Check an attestation's signature. Returns (ok, content, detail)."""
    try:
        signature = bytes.fromhex(attestation["signature_hex"])
        public = bytes.fromhex(attestation["public_key_hex"])
    except Exception as exc:
        return False, None, f"attestation is missing a valid signature/public key: {exc}"
    content = {k: v for k, v in attestation.items()
               if k not in ("signature_hex", "public_key_hex",
                            "verification_note")}
    ok = ed25519.verify(signature, canonical(content), public)
    if ok:
        return True, content, "signature valid: content is exactly what was signed"
    return False, content, ("signature INVALID: content has been altered "
                            "since signing, or the key does not match")


def gate_check(task, attestation, amount_sample_units):
    """Step 4-5: gate a payment against attestation and rules.

    Returns a decision dict. RELEASED here means only that the
    local gate passed; it is labeled TESTNET and SAMPLE and it
    sends no payment anywhere.
    """
    if attestation is None:
        return {
            "decision": "BLOCKED",
            "reason": "no proof: no attestation supplied",
            "label": SAMPLE,
        }
    ok, content, detail = verify_attestation(attestation)
    if not ok:
        return {
            "decision": "BLOCKED",
            "reason": f"invalid attestation: {detail}",
            "label": SAMPLE,
        }
    if content.get("task_id") != task["task_id"]:
        return {
            "decision": "BLOCKED",
            "reason": "attestation is for a different task",
            "label": SAMPLE,
        }
    if amount_sample_units > task["cap_sample_units"]:
        return {
            "decision": "BLOCKED",
            "reason": (f"over cap: amount {amount_sample_units} SAMPLE units "
                       f"exceeds cap {task['cap_sample_units']} SAMPLE units"),
            "label": SAMPLE,
        }
    return {
        "decision": "RELEASED",
        "network_label": "TESTNET",
        "label": SAMPLE,
        "reason": ("proof checks out, rules check out: valid attestation "
                   "for this task, amount within cap. "
                   "SIMULATED ONLY — no real NEAR payment is sent."),
        "amount_sample_units": amount_sample_units,
    }


def run_demo():
    """Run the one complete moment, plus both blocked cases."""
    task = post_task()
    evidence = do_verifiable_task(task)
    attestation = issue_attestation(task, evidence)
    released = gate_check(task, attestation, amount_sample_units=5)
    blocked_no_proof = gate_check(task, None, amount_sample_units=5)
    blocked_over_cap = gate_check(task, attestation, amount_sample_units=99)
    tampered = dict(attestation)
    tampered["evidence"] = dict(evidence)
    tampered["evidence"]["word_count"] = 999
    blocked_tampered = gate_check(task, tampered, amount_sample_units=5)
    return {
        "task": task,
        "evidence": evidence,
        "attestation": attestation,
        "gate_released": released,
        "gate_blocked_no_proof": blocked_no_proof,
        "gate_blocked_over_cap": blocked_over_cap,
        "gate_blocked_tampered": blocked_tampered,
        "label": SAMPLE,
        "disclaimer": ("LOCAL-ONLY SAMPLE DEMO. No NEAR account, wallet, "
                       "key, seed phrase, mainnet, or real testnet call. "
                       "No real payment is sent."),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Signed, Sealed, Delivered — local-only demo")
    parser.add_argument("command", choices=["demo"])
    parser.add_argument("--out", help="write demo JSON to this file")
    args = parser.parse_args(argv)
    result = run_demo()
    out = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w") as f:
            f.write(out + "\n")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
