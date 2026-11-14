#!/usr/bin/env bash
# Signed, Sealed, Delivered — local-only demo.
# Runs tests, then the end-to-end demo. No network, no NEAR call.
set -e
cd "$(dirname "$0")"
echo "=== Tests ==="
python3 -m unittest test_signed_sealed -v
echo
echo "=== Demo: one complete moment (SAMPLE, TESTNET label, no real payment) ==="
python3 signed_sealed.py demo
