# Sources and attribution

This repository is written as a **new, independently summarized case study**, not a mirror of copyrighted system binaries or third-party manuals. Inline numbers are scoped to their source and measurement conditions. Some source-specific comments are unverified hardware community hypotheses and should not be treated as official specifications.

## Device APIs, firmware / power

- [WiiBrew: Hollywood/GPIOs](https://wiibrew.org/wiki/Hollywood/GPIOs) — 0x0D8000C0–FC GPIO banks, bit8 SENSOR_BAR, bit5 slot LED, bit2 fan, OWNER semantics.
- [WiiBrew: /dev/stm/immediate](https://wiibrew.org/wiki//dev/stm/immediate) — idle, wake, slot LED, other documented ioctls.
- [WiiBrew: /dev/stm/eventhook](https://wiibrew.org/wiki//dev/stm/eventhook) — event notifications.
- [WiiBrew: IOS/Syscalls](https://wiibrew.org/wiki/IOS/Syscalls) — syscall identities, PID/UID privilege context.
- [WiiBrew: IOS/Kernel](https://wiibrew.org/wiki/IOS/Kernel) — process/memory map design.
- [WiiBrew: WiiConnect24](https://wiibrew.org/wiki/WiiConnect24), [CHANS](https://wiibrew.org/wiki/CHANS), [CHANS_reference](https://wiibrew.org/wiki/CHANS_reference) and [/dev/net/kd/request](https://wiibrew.org/wiki//dev/net/kd/request) — scheduled standby network, mail/script semantics and special triggers.
- [WiiBrew: Libwc24](https://wiibrew.org/wiki/Libwc24) — historic public WC24 library context.

## Board and IR electrical references

- [ConsoleMods: Wii connector pinouts](https://consolemods.org/wiki/Wii:Connector_Pinouts) — original sensor bar connector and typical voltage descriptions.
- [ConsoleMods: Wii buying guide](https://consolemods.org/wiki/Wii:Buying_Guide) — CPU board revision caveats.
- [BitBuilt: Noldendo Wii Miicro v1.1](https://bitbuilt.net/forums/threads/guide-release-noldendo-wii-miicro-v1-1.3750/) — *particular six-layer board* component notes; do not generalize R164.
- [BitBuilt: Shank's Wii Super Thread](https://bitbuilt.net/forums/threads/shanks-wii-super-thread.66/) — low-side circuit and watt-per-revision comparisons with stated conditions and caveats.
- [GC-Forever sensor bar wiring discussion](https://www.gc-forever.com/forums/viewtopic.php?t=3235) — community board photos and supply-trace discussion.
- [fail0verflow MINI](https://github.com/fail0verflow/mini) — nominal Hollywood timer information; not a stock IOS real-time guarantee.

## CPU, RTOS and power metering

- [IBM PowerPC 750CL User's Manual](https://fail0verflow.com/media/files/ppc_750cl.pdf) — HID0[DPM], Doze, Nap, Sleep, interrupts and coherence requirements.
- [devkitPro/libogc 2.14.0 LWP](https://github.com/devkitPro/libogc/blob/v2.14.0/libogc/lwp.c) — older idle_func with while(1).
- [devkitPro/libogc modern Tuxedo idle](https://github.com/devkitPro/libogc/blob/master/tuxedo/thread.c) — KThreadIdleMain with for(;;).
- [devkitPro/libogc modern early_init](https://github.com/devkitPro/libogc/blob/master/tuxedo/early_init.S) — HID0_DPM initialization.
- [devkitPro/libogc current Wii network wrapper](https://github.com/devkitPro/libogc/blob/master/libogc/network_wii.c) — net_select/net_poll contract.
- [devkitPro/libogc current nanosleep](https://github.com/devkitPro/libogc/blob/master/libogc/timesupp.c) — KThreadSleepTicks.
- [LBNL/UC energy study](https://escholarship.org/uc/item/2k74d6km) — on-state measurements across multiple Wii units.
- [California plug-load report (2010)](https://www.calmac.org/publications/BCE_Final_Report_2010.04.26.pdf) — older Wii idle/active figures.

## Original analysis provenance

The case-specific 65,536-code STM enumeration, all 39 direct writer classification, discovered exception with `input << 5`, and local kernel privilege/descriptor checks came from a **private, read-only, hash-validated analysis of an owner-controlled NAND archive on 2026-10-27**. No source license for proprietary Nintendo IOS was assumed. The public site includes exact **findings and methodological limitations** but not Nintendo binary contents.

Report an independently verified correction with a source link and explicitly stated hardware/IOS version; do not send private backups or keys.
