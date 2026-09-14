# Canonicalization — current bytes and proposed v1

Status: current implementation record, 14 September 2026. The PRD v1 profile
is **proposed**, not ratified. See D-01/D-02 in [the decision register](prd-decisions.md)
and R6 in [reconciliation](prd-reconciliation.md).

## Implemented audit format: draft-v0.1

Source: [audit/chain.py](../platform/core/src/mulyankan_platform/audit/chain.py).

- `CANONICAL_SCHEMA_VERSION` is `draft-v0.1`.
- `canonical_bytes` serializes a Python dictionary with `json.dumps`,
  `sort_keys=True`, compact `(',', ':')` separators and `ensure_ascii=False`,
  then encodes UTF-8. It does not perform the PRD's Unicode normalization,
  HTML/equation normalization or a verified RFC 8785 number/string profile.
- The audit link includes canonical schema version, event identifier,
  sequence, timestamp, actor, action, object references, payload hash and
  previous hash. It excludes the final event hash.
- The event hash is SHA-256 of decoded previous-hash bytes concatenated with
  the canonical link bytes. Genesis is 64 hexadecimal zeros.
- An optional payload is hashed then discarded; audit events retain its
  hash, not its question content.
- Existing tests cover deterministic key order, Unicode encoding, chain
  verification, alteration/removal detection and concurrent appends.
  They do not certify a cross-language canonicalization standard.

Preserve these bytes for existing records. Changing whitespace, normalization,
fields, number handling or schema version changes hashes. A future database
store must preserve verification of this format or provide an explicitly
versioned migration/verification strategy.

## PRD proposal: canonicalization_rule_version 1.0

Annex §8.4 proposes a JCS container, NFC text handling, deterministic restricted
HTML and equation serialization, stable option order, integer/decimal-string
numbers, and asset checksums/alternatives covered by the content hash. This
is a wider content/decision/manifest/audit contract than today's audit helper.

Before implementation, Technical Lead and Security must ratify the precise
profile, its standard references, compatibility rules and byte-level fixtures.
Resolve Unicode sorting, bidirectional controls, whitespace that may be
semantically significant, numeric values and invalid inputs explicitly; do
not equate the annex's shorthand description with proven conformance.

Required acceptance artefacts: canonical input/output fixtures for every
supported content kind and language, cross-runtime equality checks,
version-aware verification, malformed-input refusal, manifest/hash coverage,
and historic-chain/restore verification. These are planned checks, not
existing test results. This documentation adds no new canonical byte format.
