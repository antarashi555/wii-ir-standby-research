# WiiConnect24 (KD/CHANS) standby communication and wake-up routes

## Why working Google Home HTTP does not survive yellow

The demonstrated **green-mode** solution has Broadway executing an HTTP listener and IR driver. Transition into **WiiConnect24 yellow idle** shuts down Broadway execution. An already-opened green-mode socket and its callbacks cannot simply continue executing under Starlet. WiiConnect24 networking (KD) is not interchangeable with a userland HTTP server.

This is a *process and service-boundary problem*, not simply a missing Wi-Fi password or a public router port. DNS, DHCP and online reachability alone do not confer an inbound application API.

## What KD / CHANS actually expose

Documented WiiConnect24/KD supports scheduled transfers and mail-related processing. CHANS is a Starlet-side script interpreter that can run upon processing certain specially routed *downloaded WC24 mail*. Public CHANS methods include mail/storage operations, slot LED patterns, and application-launch behaviors — **no documented general sensor-bar GPIO8 bitstream/PWM interface**.

Important distinctions:
- A regular WC24 **download completion** does **not** imply a generic application callback.
- Special mail processing must be configured with matching title/mail resources; arbitrary SMTP e-mail does not activate all special WC24 download headers.
- A CHANS `setLedPattern` affects the *slot LED*, not the IR sensor bar.
- `launchApplication` is not a proof of keeping Broadway off; relevant title boot transitions toward waking the console.
- Historical official network endpoints were retired; a third-party mail revival does not guarantee generic webhook delivery or any particular polling latency.

**Result:** CHANS is evidence that some programmable Starlet behavior can occur during standby, but it does **not** solve the critical original sensor-bar carrier gap.

## Waking Broadway is a different design

The original Wii STM interface documents:

- `0x2004 STM_IdleMode`: request yellow WC24 idle.
- `0x2005 STM_Wakeup`: restore systems shut off by idle and hot-reset.

WC24 boot mail / `NANDBOOTINFO` offers a documented *conditional* mechanism to start a title after standby mail processing. It does **not** just execute an SD card Homebrew DOL while remaining yellow.

Historical implementation notes make this a poor instantaneous smart light controller:
- The inspected user's boot-mail enable flag was **disabled** at the time of the read-only audit.
- Provisioning is necessary: downloaded-mail configuration, preinstalled launcher/title, network service and command authentication.
- Requested schedule intervals (1/5/15/30/60 minutes in older utilities) are configuration choices, **not** measured guarantees. Even ideal 2-minute periodic polling averages ~1 minute waiting time, before network retry and boot. The exact actual service delay and rearm gating remain untested.
- Changing NAND config, enabling legacy unsigned payload behavior, and installing an obsolete title were specifically **not attempted**.

Other routes considered: Wii Remote Bluetooth POWER starts the console under standard pairing; physical disc insertion may auto-start. Emulating either route from Google Home requires extra devices / unproven protocol behavior. USB 5V in standby does not establish working USB host HID input or a native wake-on-LAN signal.

## Decision

The **wake-on-demand** idea can bypass yellow IR power, native standby GPIO and 38 kHz timing, but merely **relocates** uncertainty into authenticated external triggers, start-up latency, auto-launch and safe return to standby. It did not become a working device during this study.

Primary sources:
- https://wiibrew.org/wiki//dev/stm/immediate
- https://wiibrew.org/wiki//dev/net/kd/request
- https://wiibrew.org/wiki/WiiConnect24
- https://wiibrew.org/wiki/CHANS
- https://wiibrew.org/wiki/CHANS_reference
- https://wiibrew.org/wiki/Libwc24

See also [blocker matrix](02-blockers-and-decisions.md).
