# Wii IR Smart Remote: Green-Mode Successes, Yellow-Standby Blockers

**[日本語の概要はこちら / Japanese overview](README.ja.md)**

> **調査記録・否定的結果 / Research notes and negative results (2026-10-24–27)**
> Platform: original Nintendo Wii, ordinary green running mode vs. yellow WiiConnect24 standby.
> Status: **green-mode IR demonstrated; yellow-mode IR NOT demonstrated; green-mode power reduction NOT measured.**

## 目的 / Goal

既存のWii本体と純正の有線センサーバーを、Panasonic照明用の38 kHz赤外線スマートリモコンとして再利用できるか検証した。緑色の通常起動では、リモコン操作・時刻制御・Google Homeからの遠隔操作に成功した。次に、Broadway (PowerPC) が停止する黄色WiiConnect24待機で同様の機能を維持できるか調査したが、**純正IOSに任意の赤外線GPIO制御APIが見つからないなど、複数の独立した障害**を確認した。

**This repository prioritizes non-obvious failure modes, exact limits of static reverse engineering, and reproducible research methodology, not a working yellow-standby modification.**

## 最重要の結果 / Priority findings

| Finding | Evidence strength | Document |
| --- | --- | --- |
| Green: sensor bar sent real ON/OFF IR, schedule and Google Home worked | User-observed functional tests; no long-term uptime/power measurements | [History](docs/01-history.md) |
| Stock IOS58/IOS80 STM: no recognized 16-bit ioctl exposes arbitrary sensor-bar GPIO bit8 control | Static NAND analysis: **65,536 inputs**, 13 recognized commands, 65,523 default; 39 direct privileged writes | [STM negative result](docs/03-ios58-ios80-stm-negative-result.md) |
| Yellow sensor-bar positive supply on this board is **UNKNOWN** | Board diagrams conflict or cover other revisions; absence of light is not proof of absent positive rail | [Power / wiring](docs/06-sensorbar-rail-and-carrier.md) |
| WC24 networking is not a generic inbound HTTP server for the green Homebrew app | Public KD/CHANS docs and local source audits; unverified custom triggers | [WC24](docs/04-wc24-and-wakeup.md) |
| Old and current libogc idle threads **spin**, even if app threads sleep | Upstream v2.14.0 + master source inspection; hardware savings unmeasured | [Green power](docs/05-green-power-and-libogc-idle.md) |

[全ボトルネックと方針転換 / Decision matrix](docs/02-blockers-and-decisions.md)

## What this does **not** claim

- Not a proof that *all* undocumented IOS calls or third-party IOS modifications are impossible.
- Not proof that the sensor bar receives (or loses) power in yellow standby on any particular motherboard.
- Not proof that Doze/Nap saves a given number of AC watts on this console.
- Not a ready-to-install firmware, kernel exploit, GPIO script, or flashing guide.
- No evidence that the stock console receives Google Home commands while Broadway is off.

## Scope and provenance

- Stock IOS58 **rev6176** and IOS80 **rev6944** extracted **in RAM only** from an authorized owner's local NAND backup. Exact TMD SHA1 checks were performed before interpreting module content. Findings apply **to those inspected images and observed code paths**.
- The exact motherboard revision was **not independently confirmed**; references to RVL-CPU-01 are provisional.
- Public WiiBrew, IBM PowerPC 750CL, Nintendo, BitBuilt, ConsoleMods and devkitPro resources are linked in [sources](docs/08-sources.md).
- External image/firmware sources and code versions can change. The original NAND, keys, device IDs and remote-control cloud credentials are **not included**.

## Repository layout

- `docs/01-history.md`: experiments and sequence, distinguishing actual Wii observations from PC-only tests.
- `docs/02-blockers-and-decisions.md`: hard blockers, condition changes and rejected routes.
- `docs/03-ios58-ios80-stm-negative-result.md`: deepest original static result; command sweep and privileged writer inventory.
- `docs/04-wc24-and-wakeup.md`: standby communication, KD/CHANS and boot-mail limitations.
- `docs/05-green-power-and-libogc-idle.md`: real scheduler source findings and Doze/Nap caveats.
- `docs/06-sensorbar-rail-and-carrier.md`: uncertain electrical assumptions and IR timing.
- `docs/07-methodology-and-reproduction.md`: limits, reproducibility and safety/security.
- `evidence/audit-metrics.json`: summarized **observations**, not firmware.
- `tests/test_public_arithmetic.py`: runs public arithmetic/consistency checks only; **does not re-run private NAND analysis**.

## Open research questions / 未解決事項をGitHub Issuesで追跡

1. [黄色待機中のセンサーバー正極電圧を基板世代別に確認する](https://github.com/antarashi555/wii-ir-standby-research/issues/1) — no compatible verified voltage measurement.
2. [STM以外の純正IOSでGPIO8を操作する正規APIがあるか](https://github.com/antarashi555/wii-ir-standby-research/issues/2) — the current negative proof is scoped.
3. [libogcの安全なDoze復帰と実際の省電力効果を測る](https://github.com/antarashi555/wii-ir-standby-research/issues/3) — no real W measurement yet.
4. [WC24の安全な命令受信と起床遅延を検証する](https://github.com/antarashi555/wii-ir-standby-research/issues/4) — no reliable command-ingress service established.

## Reader guidance / 再現性と安全性

NAND/IOS binaries, decrypted ARM modules, keys, device serials, IP addresses, account tokens and personally identifying local paths are deliberately excluded. Do not copy firmware or sensitive dumps into issues or pull requests. **No electrical shorting, return-to-ground bypass, unauthorized fan stop, or unreviewed IOS installation is recommended.**

The original green controller was not changed in this publication. **This is a case study of what failed and why, not a deployable remote-control system.**

Start at [STM negative result](docs/03-ios58-ios80-stm-negative-result.md) if you are researching Starlet GPIO, or [green power](docs/05-green-power-and-libogc-idle.md) if you are trying to minimize idle AC watts.
