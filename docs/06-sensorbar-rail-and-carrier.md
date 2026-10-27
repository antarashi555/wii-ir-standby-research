# Wired Wii sensor bar: unresolved yellow rail and ~38 kHz carrier

## Critical electrical misconception: 2-pin does not mean permanent ground

The original wired Wii sensor bar is an **infrared LED emitter assembly**, not a camera/sensor. On board configurations described by community engineers, its supply is sourced from the Wii's nominal 12 V path (often with a series resistor), while the LED return is connected to a **transistor-controlled low-side switch** (Q24 in a reported revision), **not necessarily hard-wired to board ground**.

Published information varies by board revision: one six-layer build describes **R164 = 39 Ω / 1W** on the positive feed; another early RVL-40 trace suggested a different supply topology. Those are source-specific, not universal specifications. Loaded sensor-bar terminal voltage is reported around 7–7.5 V in typical operation in some public pinout references, distinct from the unloaded nominal adapter voltage.

**What was NOT measured:** yellow standby voltage from the sensor bar's **positive node to actual board ground**, the return switch state, and the connector's behavior on the particular investigated Wii motherboard.

A dark IR-camera observation in yellow has **at least two possible explanations**:

1. There is no positive supply available.
2. A positive supply exists, but the low-side gate is **open/off**, so no current can flow.

Therefore, darkness or a two-terminal potential reading without topology context is **not proof** of a dead positive power rail.

> Safety: **Do not short the negative bar pin to ground, bypass the low-side switch, bridge connector contacts, or apply unregulated 12V externally.** These notes do not authorize physical probing, fan-off operation, or modification. A professional isolated measurement procedure and revision-verified schematic would be separate work.

## Original Panasonic infrared frames used for the normal-powered experiments

Standalone ARM test source (not deployable as stock IOS resident) encoded two 40-bit messages, for the tested appliance:

- **ON:** `2C 52 09 2D 24`
- **OFF:** `2C 52 09 2F 26`

These are **one specific tested remote's observed command codes**, not universal commands for Panasonic lights.

Nominal source timing: leader mark **3480 µs**, leader space **1740 µs**, 40 data marks **435 µs**; spaces **435 µs** for 0 bits, **1305 µs** for 1 bits; trailer mark **435 µs**.

Derived, not oscilloscope-measured:

| Command | Number of 1 bits | Whole ideal frame duration |
| --- | ---: | ---: |
| ON | 14 | **52,635 µs** |
| OFF | 16 | **54,375 µs** |

The fail0verflow MINI-style hardware timer estimate **1.898 MHz** would support an ideal **50-tick / cycle ≈ 37,960 Hz** carrier, if its oscillator and timer behavior are retained. That is **nominal time resolution, not proof of accurate GPIO output under IOS scheduling**. A carrier requires ~13.2 µs per half-cycle and sufficiently consistent signal timing. The actual electrical drive capacity, IOS permission/priority, timer jitter and transistor/LED output were **not measured in yellow**.

A 53–54 ms burst contains an estimated **~809 carrier cycles** in its mark segments, equivalent to roughly 1,618 edges **only during the burst**. It would be misleading to call this a continuous 76k-edges/sec workload all day.

## The remaining unknowns are independent

- Power: Is the positive source actually energized in yellow on the specific board?
- Privilege: Can an authorized IOS resident drive SENSOR_BAR bit8 while Broadway is powered off?
- Ownership: Who owns GPIO bit8 in yellow, and can switching occur safely?
- Timing: Is real GPIO output sufficiently jitter-free while WC24 tasks execute?
- Communication: How does an authenticated Google Home command arrive with useful latency?
- Recovery: Can this safely run when the fan is normally stopped?

It takes affirmative evidence for **all** of the above to claim viability. This research does not provide it.

Public references:
- https://wiibrew.org/wiki/Hollywood/GPIOs
- https://consolemods.org/wiki/Wii:Connector_Pinouts
- https://bitbuilt.net/forums/threads/guide-release-noldendo-wii-miicro-v1-1.3750/
- https://bitbuilt.net/forums/threads/shanks-wii-super-thread.66/
- https://www.gc-forever.com/forums/viewtopic.php?t=3235
- https://github.com/fail0verflow/mini
