# Provider contracts

How solutions plug in. ADR-0003 is the decision; this document is the working
contract for provider authors.

Status: design target. [Delivery status](delivery-status.md) records the
interfaces and test definitions actually present. The catalogue's milestone
column is a planned introduction, not proof of an installed provider.
Read the [PRD source map](source-of-truth.md) and [product workflow](product-workflow.md)
for the behaviour a provider must preserve.

## Lifecycle of a provider

1. Implement the SPI — a `typing.Protocol` in `mulyankan-spi` — in your own
   package.
2. Pass the SPI's conformance suite (`mulyankan_spi.conformance.*`).
3. Bind it in the environment's `platform.yaml`.
4. The registry validates the binding at startup and refuses unknown or
   non-conformant providers.

Example binding:

```yaml
providers:
  kms:
    provider: mulyankan_provider_kms_local.provider:LocalKmsProvider
    config:
      key_id: dev-key-1
```

## Rules

- Providers depend on `mulyankan-spi` only — never on the platform core.
- Providers never mutate workflow state and never write audit events; the
  platform audits each interaction content-free.
- Validation/sealing-path SPIs must be deterministic; the bound provider's
  name and version are recorded in manifests and the audit chain.
- `describe()` returns the provider descriptor (name, version, deterministic
  flag, data-handling declaration) — the same pattern the gateway uses for
  model identity.
- A capability with no binding, or a provider removed from configuration, is
  refused at the next call.

## SPI catalogue (v1)

| SPI | Module | Conformance suite | First consumer | Milestone |
|---|---|---|---|---|
| kms | `mulyankan_spi.kms` | `conformance.kms` | sealing, export | M0 (reference) |
| identity | `mulyankan_spi.identity` | `conformance.identity` | sign-in | M1 |
| storage | `mulyankan_spi.storage` | `conformance.storage` | assets, sealing | M2 |
| sanitize | `mulyankan_spi.sanitize` | `conformance.sanitize` | asset upload | M2 |
| similarity | `mulyankan_spi.similarity` | `conformance.similarity` | validation | M2 |
| render | Node package, `apps/web/packages/render` | render fixtures | preview/review/a11y | M2 |
| gateway | `mulyankan_spi.gateway` | `conformance.gateway` | authoring proposals | M4 |
| notify | `mulyankan_spi.notify` | `conformance.notify` | lifecycle events | M4 |
| export | `mulyankan_spi.export` | `conformance.export` | readiness handoff | M4+ |

Telemetry is not in the catalogue: the proposed OpenTelemetry approach in
ADR-0011 uses OTel environment variables rather than `platform.yaml`;
see [observability](observability.md). ADR-0011 still says Proposed; this
catalogue does not mark it accepted or implemented. Diagnostic telemetry
must remain separate from the durable integrity/audit requirements.

M0 contains the `kms` interface and conformance suite, exercised with a test
double. The reference provider and environment binding remain planned;
`providers/` and `platform.yaml` are absent at the baseline. The remaining
SPIs are planned for the milestone that first consumes them.

The gateway's M4 target covers the connector slice. D-38's full Layer 2
curriculum ingestion, generation and metadata delivery needs a named owner
and schedule (R2); translation drafting additionally depends on D-48.
The `export` entry refers to controlled machine handoff, never an Admin
question-bank download or paper-assembly feature.
