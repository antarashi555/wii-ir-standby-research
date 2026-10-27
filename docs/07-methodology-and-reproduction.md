# Reproducibility, trust boundaries and security

## Source categories

| Label | Meaning | Examples |
| --- | --- | --- |
| **Hardware observed** | Someone actually exercised a feature on this owner-controlled Wii | Green Panasonic IR ON/OFF, scheduled lighting, Google Home response |
| **Static observed** | A program decoded specific instructions / headers from TMD-hash-verified owned NAND data *without executing them* | IOS58/80 STM 16-bit dispatch, syscall PID gate, 39 direct writers |
| **Public reference** | Published documentation or source code for an identifiable hardware/software version | WiiBrew, IBM 750CL, devkitPro old and current libogc |
| **Host model** | A synthetic test proving logic properties in a simplified model | Timestamp boundary tests, lost-wakeup counterexample |
| **Unknown** | No appropriately controlled proof; **never silently promote to known** | Yellow positive sensor rail, real 38kHz IOS jitter, actual watts |

## Static STM audit methodology (non-proprietary description)

1. Work on an authorized **read-only** backed-up source and retain console-specific key material **in volatile memory only**.
2. Parse TMD content records; validate size and SHA1 of content against metadata; identify which content belongs to IOS58/80.
3. Parse ARM big-endian ELF and decoder architecture correctly; map executable segments without conflating data/padding with instructions.
4. Follow the actual STM synchronous ioctl dispatcher's branches. Enumerate all 0x0000..0xFFFF values with a deterministic host-side interpreter; independently check 13 handler targets and default handling. Do not confuse 65,536 input cases with 65,536 independent code paths or complete 32-bit command coverage.
5. Identify all **direct BL** instructions targeting the STM's documented privileged ACRRegWrite veneer; reconstruct target register offset provenance, including conditional branches rather than naïve backward-7-instruction matching.
6. Audit GPIO bit masks and the inputs to shift operations at their actual callsites. A shift with unmasked input cannot be assumed safe just because normal callers pass 0/1. Distinguish direct callers from possible indirect execution.
7. Separately examine kernel syscall caller ACL, register offset whitelist and MMIO protection. Distinguish **static mapping descriptors** from runtime per-process mappings.
8. Classify findings under explicit scopes, preserving uncertainty about modules not subject to exhaustive interprocedural analysis.

**Disclosure choice:** we publish aggregate, non-identifying instruction addresses/branch facts and methods only. This repository **intentionally does not ship** raw or decrypted IOS, NAND images, key data, reverse-engineered device credentials, WADs, patch-ready console payloads, or third-party copyrighted source snapshots.

## What independent readers can repeat immediately

- Confirm WiiBrew's register names and published STM ioctls.
- Inspect original source of libogc v2.14.0 and current Tuxedo idle threads.
- Run `python -m unittest discover -s tests -v`. This checks public numeric invariants, arithmetic and data-summary consistency only. It **cannot reproduce analysis against private NAND**, and passing does not corroborate the actual code paths.
- Scrutinize our interpretation; send reproducible links, verifiable board revision facts, or independent **non-sensitive** counterexamples as issues.

## Data privacy and publication hygiene

**Not accepted for publication:** console serial ID, NAND/keys dump, decrypted titles, hardware console certificates, OAuth/App Home credentials, internal LAN IP address, unique metadata, personal filesystem paths, or a circuit modification presented as risk-free. A blob SHA of a public libogc source file is not a Nintendo device secret; hardware cryptographic secrets never leave RAM in the original local inspection.

Only put sanitized text and stand-alone public models in this repository. **Do not copy the local investigation folder wholesale.** It includes private recovery archives and executable firmware probes.

## Revisit criteria

The most valuable independently confirmable follow-ups are (1) compatible, board-revision-specific yellow sensor-positive measurement **from a reliable existing publication**; (2) an externally documented authorized stock STM/KD GPIO8 callback path; (3) a kernel scheduler architecture which truly enters Doze with proven interrupt race safety; and (4) same-console AC watts from controlled original-vs-optimized green mode.

No unreviewed experiment on a production Wii is requested by this publication.
