# Green-mode power optimization: why blocking the app is not sleeping Broadway

## Existing power measurements — external Wii units only

Power consumption is a **full-system** question. AC supply conversion losses, board revision, optical drive board, IR bar and wireless activity matter independently of a Homebrew task's instruction count.

| Source and condition | Value | Valid interpretation |
| --- | ---: | --- |
| California 2010 report (older Wii sample) | **10.5 W idle / 16.4 W active** | Published historical measurement, not this Wii |
| LBNL 2013 in-home study | **10.9 W median / 13.12 W mean when on** | Mixed on-state activities and different board generations, not idle-only |
| BitBuilt board comparison (CPU-01, bar and disc drive, game scene) | **15.9 W** | Same-scenario community sample; unit reportedly had GPU anomalies, not green Homebrew wattage |
| BitBuilt CPU-50, bar attached, no drive (game scene) | **9.9 W** | Hardware revision/configuration comparison, **not** software optimization |

The exact *green HTTP + Panasonic IR app at idle* and its fan/rail/sensor-bar power have **never been metered** by this research. Comparisons above should not be combined to claim a watts-saved number.

## Local source observation: a normal HTTP test uses video-frame cadence

The studied `wii-idle-http-probe` source (an **experiment, not proven to be the production controller**) loops over `WPAD_ScanPads`, `PAD_ScanPads`, `net_select(...,{0,0})` and `VIDEO_WaitVSync()`. The final call blocks on a retrace; this is a **frame-paced** loop, *not* a demonstrated 100%-busy user thread.

A rewritten event-driven design can reduce needless frame/UI work and allocate network polling based on the next command/time deadline. However, **this discovery alone does not establish that the Broadway CPU clocks stop**.

## New source-level bottleneck: old AND current libogc idle thread spins

**Historical libogc v2.14.0**, `libogc/lwp.c` lines 131–135:

```c
static void* idle_func(void *arg)
{
    while(1);
    return 0;
}
```

It is installed as an idle thread when all other threads block. **Current libogc/Tuxedo**, `tuxedo/thread.c` lines 28–31, likewise implements:

```c
static void KThreadIdleMain(void)
{
    for (;;);
}
```

The current `__libogc_nanosleep` calls `KThreadSleepTicks`, which blocks the *calling thread*; `net_select` calls IOS `net_poll`, with finite timeout. If all user threads block, the libogc idle thread remains runnable and spins. **An application-level 60Hz→4Hz poll reduction is not a 15× reduction in processor cycles or wall AC power.**

The precise startup/scheduler version linked into the owner's *deployed* DOL is **not established**, so these findings pertain to inspected upstream source versions.

## CPU hardware capability: DPM vs Doze/Nap/Sleep

The original IBM PowerPC **750CL** manual documents:
- `HID0[DPM]`: dynamic clock gating for unused internal execution units, **not CPU sleep or a powered-down rail**.
- `Doze`: low power with timebase/decrementer running, external/timer interrupt-based wakeup; a research candidate for the scheduler's true idle thread.
- `Nap`: deeper inactivity, with bus-snooping/coherency handshake (QACK) implications; unsuitable for a first experiment.
- `Sleep`: timebase/decrementer stops; inappropriate for an ordinary time-scheduled network controller without an independently proven wake source.

Current libogc `tuxedo/early_init.S` **sets HID0_DPM**. Thus simply toggling DPM is not a demonstrated new power gain. Doze/Nap is not the same feature and isn't automatically used by the idle loop above.

Directly modifying app-level HID0/MSR or trying 729→486 MHz PLL transitions is **NOT advised**. Clock switching requires Starlet-side handling, and a wrong transition can hang or corrupt system behavior. Fan/rails must not be disabled for unattended tests.

## Additional source-level trap: Wii `net_select`

The current upstream `libogc/network_wii.c` has two non-obvious contract details:

- `net_select` **dereferences the timeout pointer**; explicitly pass a non-NULL finite `struct timeval` in this version.
- `net_poll` rejects **zero monitored sockets** with `-EINVAL`; if disconnected, use bounded timer/backoff rather than calling select on an empty set.

These are API/logic observations, not measured CPU power. The exact deployed build may differ.

## Required wake race and future measurements

A naïve `check work → enter low-power` sequence can lose an interrupt arriving between the steps. A safe scheduler-level Doze implementation would need documented atomic check/park semantics, interrupt enable state, decrementer wakeup, IOS/Wi-Fi IPC completion, cache/bus correctness, reset callbacks and an escape/recovery plan. Host-only scenario tests demonstrate the logical race, **not real-CPU correctness**.

An honest follow-up requires **same-console, wall-socket true-power meter** readings with identical ambient/console conditions, comparing working original app vs. one alteration at a time, while retaining light ON/OFF, schedule accuracy, command latency, reconnect and normal cooling. Until then **no W savings claim**.

Primary:
- https://github.com/devkitPro/libogc/blob/v2.14.0/libogc/lwp.c
- https://github.com/devkitPro/libogc/blob/master/tuxedo/thread.c
- https://github.com/devkitPro/libogc/blob/master/tuxedo/early_init.S
- https://github.com/devkitPro/libogc/blob/master/libogc/network_wii.c
- https://github.com/devkitPro/libogc/blob/master/libogc/timesupp.c
- https://fail0verflow.com/media/files/ppc_750cl.pdf
- https://escholarship.org/uc/item/2k74d6km
- https://bitbuilt.net/forums/threads/shanks-wii-super-thread.66/
