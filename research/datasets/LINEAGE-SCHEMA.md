# Dataset lineage schema

## Normative record

```yaml
object_id: "sha256:..."
schema_version: "1.0"
tenant_id: null
purpose: "quarantine|train|eval|redteam"
training_allowed: false
consent_record_id: null
source:
  uri: ""
  acquired_at: ""
  source_type: ""
  owner: ""
license:
  spdx_id: null
  evidence_uri: null
  reviewed_by: null
sensitivity:
  classification: "public|internal|confidential|restricted"
  pii_status: "unknown|detected|sanitized|clear"
  secrets_status: "unknown|detected|sanitized|clear"
content:
  raw_object_id: null
  canonical_object_id: null
  exact_hash: ""
  minhash_signature: ""
  semantic_fingerprint: ""
  ast_fingerprint: null
transformations: []
contamination:
  eval_registry_version: ""
  result: "unknown|clear|blocked|review"
  matches: []
quality:
  gate_version: ""
  verifier_artifacts: []
  reviewer_decisions: []
  status: "quarantined|rejected|eval_only|training_candidate|approved_snapshot"
split:
  name: null
  organization_group: null
  repository_group: null
  time_cutoff: null
retention:
  expires_at: null
  deletion_request_id: null
```

## Инварианты

- **VERIFIED FACT:** `training_allowed` отсутствует или не равно `true` — объект не читается train job.
- **VERIFIED FACT:** `training_allowed=true` допустимо только при непустых rights/consent evidence, clear privacy/secrets, clear contamination и approved quality status.
- **VERIFIED FACT:** `tenant_id != null` запрещает включение в general snapshot, кроме отдельного explicit opt-in workflow с новым derived object ID; raw object остаётся tenant-bound.
- **VERIFIED FACT:** Любая transformation append-only и содержит tool/version/config/operator/time/input/output hashes.
- **VERIFIED FACT:** Split assignment наследуется по connected provenance group; отдельные строки одного repository/event нельзя разнести между train и hidden eval.
- **RISK:** Ошибка metadata опаснее ошибки отдельного текста, поскольку масштабируется на snapshot; manifests подписываются и валидируются policy-as-code.

## Snapshot manifest

**VERIFIED FACT:** Manifest фиксирует ordered object IDs, dataset contract/version, query, exclusions, gate versions, reviewer approvals, storage URIs, creation time и signature. Checkpoint registry хранит точные manifest IDs всех train/eval inputs.

- **EXPERIMENT REQUIRED:** Проверить воспроизводимость выборки: два независимых builder job обязаны получить одинаковый Merkle root.
- **ENGINEERING HYPOTHESIS:** Lineage graph должен обеспечивать impact query «какие snapshots/checkpoints затронуты объектом» менее чем за 10 минут для operational-scale registry.
