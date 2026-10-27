# ボトルネックと条件変更 / Blocking dependencies

## Non-negotiable gates for **staying yellow**

The hoped-for design was: Google Home → Wii while yellow (Broadway off) → Starlet executes command → wired original sensor bar sends a roughly 38 kHz Panasonic IR frame → light switches, all without modified IOS or extra electronics.

| Gate | Current status | Why it matters |
| --- | --- | --- |
| Sensor-positive voltage in yellow | **Unknown; not measured** | If the LED bank is unpowered, code alone cannot emit IR |
| Correct GPIO ownership and write permission | **No supported stock STM API identified** | GPIO bit8 is normally Broadway-facing; Starlet-facing writes require different ownership/privilege |
| Persistent execution inside live standby IOS | **Not established** | Standalone Starlet code replaces/interrupts the IOS environment used by WC24 |
| 38 kHz waveform with bounded jitter | **Not tested in stock resident IOS** | Nominal timer resolution is not proof of real-time pulse delivery |
| Authenticated, timely command ingestion | **Not established** | KD/CHANS processes scheduled WC24 traffic; it is not the green application's generic HTTP listener |
| Thermal/automatic recovery safety | **Not established** | Yellow ordinarily stops the fan; intensive code must not be presumed safe |

These gates are **conjunctive**: fixing any one does not eliminate the others.

## What relaxing a requirement changes

| Relax one requirement | Removes or reduces | Still unresolved |
| --- | --- | --- |
| Permit ordinary **GREEN** boot | Yellow IR rail, yellow GPIO path, yellow-specific residency and network access | Green watts, long-running stability, headless operation |
| Permit custom IOS/STM | Could change residency/privilege architecture | Electrical rail, real-time timing, cloud ingress, firmware/recovery risk |
| Permit external transmitter/controller | Could remove Wii GPIO + timer burden | Integration and hardware design; becomes a different project |
| Permit external Bluetooth trigger and boot | Could avoid yellow optical output, if emulation succeeds | Wake protocol, extra always-on device, boot latency and auto-launch |
| Permit slower scheduled wake mail | Could avoid native yellow IR | Boot-mail enablement/installed title, security, unknown real latency |
| Permit newer Wii motherboard | Might lower green baseline | Extra physical hardware; no guarantee idle Doze works |

## Prioritization by evidence, not enthusiasm

- **Highest value original negative result**: the stock STM command inventory and the 39 direct privileged write destinations. It answers a concrete question that a GPIO wiki cannot alone settle for these IOS versions.
- **Most important unresolved hardware gate**: yellow sensor rail of a precisely identified board revision. Existing board photos cannot settle it.
- **Highest practical green-mode bottleneck**: legacy and modern libogc's continuously runnable idle thread. Changing the application into a sleeping loop alone does not put Broadway into Doze/Nap.
- **Practical decision**: keep the already-working green implementation intact until an actual AC wattmeter study justifies invasive optimization.

## Research closure criteria

A route is **not** called “solved” until it has: explicit permission/safety checks; demonstrated device-specific operation (not merely static checks); repeatable IR commands; Google Home delivery with measurable latency; safe recovery; and same-console wall-power readings.

No arbitrary “5W target” is asserted: the present console has not been measured under comparable green, yellow, and modified-green conditions.
