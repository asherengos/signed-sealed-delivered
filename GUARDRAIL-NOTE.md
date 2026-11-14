# Guardrail note (skeleton placeholder)

See the full design in the goal folder:
`files/near-guardrail-design.md` and `files/near-testnet-setup-guide.md`.

Summary only, no values invented here:

- Testnet demo only. No real money.
- Adam holds funds and the full-access key, and keeps the seed phrase.
  None of these are ever given to the agent.
- The agent gets ONLY a function-call access key scoped to one
  receiver contract, an explicit method list, and a gas allowance,
  with no attached NEAR tokens.
- Receiver contract: TO-FILL (undecided).
- Method names: TO-FILL (undecided; must be explicit, never blank).
- Allowance: TO-FILL (undecided; sized from measured gas use, never blank).
- Revocation: Adam deletes the key with the full-access key.
- Intents and Chain Signatures: future work only, NOT implemented.
