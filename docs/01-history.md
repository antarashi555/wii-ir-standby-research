# 研究の経緯 / Research chronology

**2026-10-23–27 JST.** Experimental observations from one owner's modified Wii and subsequent PC-only read-only reverse engineering. Results marked *Observed* were reported during actual testing; *Static* and *Proposed* were not verified in hardware.

| Phase | What happened | Kind of evidence | Outcome |
| --- | --- | --- | --- |
| Initial remote | Wii Remote A/B used to control a Panasonic ceiling light via the wired sensor bar | **Observed green-mode hardware** | ON and OFF worked |
| Clock automation | Time-triggered ON/OFF added | **Observed green-mode hardware** | Several scheduled transitions worked |
| Google Home | Cloud-to-cloud account linking; commands forwarded through existing working Wi-Fi/HTTP path to the Wii | **Observed green-mode hardware** | Remote control worked, with occasional response issues reported; no guaranteed reliability figure |
| Yellow standby feasibility | Broadway is powered down; Starlet/IOS/KD manage WC24; green HTTP listener stops along with Broadway | Documentation, local comparisons | Green-mode service cannot simply survive the power transition |
| Alternate Starlet IR | Standalone ARM/ArmbootNow test sent Panasonic IR in ordinary powered mode | **Observed green-mode hardware**, separate environment | Proves ARM timer/LED concept, **not** coexistence with IOS/WC24 or operation in yellow |
| Native IOS exploration | Evaluated custom module paths, STM GPIO ownership and public GPIO interfaces | **PC-only source research** | Privilege, residency and deployment constraints identified |
| Stock IOS audit | SHA1-validated IOS58/IOS80 kernel and STM content analyzed locally in memory | **PC-only static analysis** | STM public API did not expose sensor bit8 control; enumerated 65,536 16-bit ioctl values |
| Yellow hardware rail | Community board pinouts and series resistor/low-side transistor reports compared | **Public board evidence; NO measurement on target board** | Yellow sensor-positive supply still unknown |
| Green power pivot | Compared Wii energy studies and both historical/current libogc scheduler | **Public literature and source audit** | Lower-risk direction, but real processor idle thread remains busy-spin; watts unmeasured |
| Host-only models | Calendar events, command deduplication, race scenarios | **Abstract PC tests** | Useful for checking assumptions; **not evidence of hardware safety** |

## Results actually achieved

- Panasonic IR commands operated the real light in green mode with the original Wii sensor bar.
- Programmed time schedules operated the light.
- The existing Google Home integration operated the light remotely. This does **not** establish uninterrupted availability, latency guarantees, or compliance with security requirements.
- The independent ARM test is **not** an ordinary loaded IOS module; it must not be treated as proof Starlet can emit IR while retaining WC24 in yellow.

## Decisions and why

1. **Stay-yellow, stock IOS, no additional hardware**: retained as a research question, **not production-ready**. GPIO privilege + positive supply + precise timing + inbound command channel are independent unresolved gates.
2. **Wake Broadway on demand**: `STM_Wakeup` exists, and boot mail is documented, but a custom, authenticated, timely wake-trigger path remains unproven. Boot-mail requires setup and may have minutes-scale delays.
3. **Green always-on**: known working functionality, but power efficiency and stability need measurements. Do not equate less application polling with processor power gating.
4. **External IR device or repurposed bar**: pragmatically viable concept, but would change the original Wii-only/no-extra-hardware requirement. Electrical safety and a tested driver still matter.

**No attempt described here provides a validated, repeatable, low-watt yellow-mode smart remote.**
