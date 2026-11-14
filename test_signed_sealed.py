#!/usr/bin/env python3
"""Tests for the Signed, Sealed, Delivered local-only prototype.

Stdlib unittest only. Run: python3 -m unittest test_signed_sealed -v
No network, no NEAR account, no wallet, no key, no seed phrase,
no mainnet, no real testnet call, no spending.
Tests use a temp key directory, never the demo key in keys/.
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ed25519
import signed_sealed


class TestEd25519(unittest.TestCase):
    def test_rfc8032_vector(self):
        seed = bytes.fromhex(
            "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
        expected_pub = ("d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a")
        expected_sig = ("e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155"
                        "5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b")
        pub = ed25519.publickey_from_seed(seed)
        self.assertEqual(pub.hex(), expected_pub)
        sig = ed25519.sign(b"", seed, pub)
        self.assertEqual(sig.hex(), expected_sig)
        self.assertTrue(ed25519.verify(sig, b"", pub))
        self.assertFalse(ed25519.verify(sig, b"tampered", pub))


class TestAttestationAndGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        signed_sealed.KEY_DIR = self.tmp.name
        signed_sealed.SEED_PATH = os.path.join(self.tmp.name, "seed.hex")
        signed_sealed.PUBLIC_PATH = os.path.join(self.tmp.name, "public.hex")
        self.task = signed_sealed.post_task()
        self.evidence = signed_sealed.do_verifiable_task(self.task)

    def tearDown(self):
        self.tmp.cleanup()

    def test_attestation_sign_verify(self):
        att = signed_sealed.issue_attestation(self.task, self.evidence)
        ok, content, _ = signed_sealed.verify_attestation(att)
        self.assertTrue(ok)
        self.assertEqual(content["task_id"], self.task["task_id"])
        self.assertEqual(att["label"], "SAMPLE")

    def test_evidence_is_recomputable(self):
        # Word count must match a fresh recomputation from the sentence.
        self.assertEqual(
            self.evidence["word_count"],
            len(self.evidence["sample_sentence"].split()))

    def test_gate_passes_on_valid_attestation_within_cap(self):
        att = signed_sealed.issue_attestation(self.task, self.evidence)
        decision = signed_sealed.gate_check(self.task, att, 5)
        self.assertEqual(decision["decision"], "RELEASED")
        self.assertEqual(decision["network_label"], "TESTNET")
        self.assertEqual(decision["label"], "SAMPLE")

    def test_gate_passes_at_exact_cap(self):
        att = signed_sealed.issue_attestation(self.task, self.evidence)
        decision = signed_sealed.gate_check(
            self.task, att, self.task["cap_sample_units"])
        self.assertEqual(decision["decision"], "RELEASED")

    def test_gate_blocks_on_missing_attestation(self):
        decision = signed_sealed.gate_check(self.task, None, 5)
        self.assertEqual(decision["decision"], "BLOCKED")
        self.assertIn("no proof", decision["reason"])

    def test_gate_blocks_on_over_cap(self):
        att = signed_sealed.issue_attestation(self.task, self.evidence)
        decision = signed_sealed.gate_check(self.task, att, 99)
        self.assertEqual(decision["decision"], "BLOCKED")
        self.assertIn("over cap", decision["reason"])

    def test_tampered_attestation_fails(self):
        att = signed_sealed.issue_attestation(self.task, self.evidence)
        tampered = dict(att)
        tampered["evidence"] = dict(self.evidence)
        tampered["evidence"]["word_count"] = 999
        ok, _, _ = signed_sealed.verify_attestation(tampered)
        self.assertFalse(ok)
        decision = signed_sealed.gate_check(self.task, tampered, 5)
        self.assertEqual(decision["decision"], "BLOCKED")

    def test_gate_blocks_attestation_for_other_task(self):
        att = signed_sealed.issue_attestation(self.task, self.evidence)
        other_task = signed_sealed.post_task(task_id="task-999-SAMPLE")
        decision = signed_sealed.gate_check(other_task, att, 5)
        self.assertEqual(decision["decision"], "BLOCKED")

    def test_demo_end_to_end(self):
        result = signed_sealed.run_demo()
        self.assertEqual(result["gate_released"]["decision"], "RELEASED")
        self.assertEqual(result["gate_blocked_no_proof"]["decision"], "BLOCKED")
        self.assertEqual(result["gate_blocked_over_cap"]["decision"], "BLOCKED")
        self.assertEqual(result["gate_blocked_tampered"]["decision"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
