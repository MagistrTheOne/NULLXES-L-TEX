# Decision snapshot at 48d217c

- **VERIFIED FACT:** Git commit: `48d217c`.
- **VERIFIED FACT:** Original directly modified canonical path: `docs/ARCHITECTURE.md`.
- **VERIFIED FACT:** Inherited primary design path: `docs/branches/E-01.md` from commit ancestry.
- **VERIFIED FACT:** The snapshot retained the Qwen 480B Instruct direct-foundation decision while tightening disabled-by-default DAPT, immutable BF16 merge boundaries and separate conversion/merge jobs.
- **VERIFIED FACT:** Exact content is preserved in Git and can be reconstructed with `git show 48d217c:<original-path>`.
- **RISK:** The improved lineage controls did not make the derivative weight parent compatible with the later independent E-01 decision.
