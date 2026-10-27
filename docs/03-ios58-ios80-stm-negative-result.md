# Original result: stock IOS58/IOS80 STM has no verified sensor-bar GPIO8 API

**Status: scoped NEGATIVE result — 2026-10-27.** Based on hash-verified **IOS58 rev6176 and IOS80 rev6944** from one owned Wii NAND archive, parsed read-only entirely in RAM. No raw copyrighted binaries, proprietary contents or device-specific keys are in this repository.

## Precise question

Can an ordinary Broadway Homebrew program (or authorized IOS client) invoke an existing stock STM service to drive **Hollywood SENSOR_BAR GPIO bit8 = 0x100** while the Broadway is off in yellow WiiConnect24 idle?

**Finding:** No such callable path was identified through the actual, inspected **STM /dev/stm/immediate** dispatcher or its observed direct privileged hardware writes. This is **not** a proof against every possible private code path or IOS replacement.

## A. Complete 16-bit command-space static enumeration

A Python interpreter of the real ARM big-endian dispatcher at **0x20300104–0x203002A4** classified every integer in the **0x0000–0xFFFF** range.

| Result | Count |
| --- | ---: |
| Distinct 16-bit command inputs | **65,536** |
| Recognized command values | **13** |
| Default/unrecognized handler | **65,523** |

Recognized values (hex): **0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x3001, 0x3002, 0x4001, 0x4002, 0x5001, 0x6001, 0x6002, 0x7001**.

Among these, 0x2004 requests idle, 0x2005 wake, 0x6001 LEDFlash and 0x6002 LEDMode. The LED operations concern the **blue disc-slot LED (bit5)**, not **SENSOR_BAR (bit8)**. Five >0xFFFF command samples also reached default, but **the full 32-bit space was not enumerated**. No claim is made that the enumeration covers non-STM drivers or dynamic code modification.

The 13 known branches + eight independent static conditions gave **21/21** checks in the local source-level validation. “Recognized” means the dispatcher routes a value, **not** necessarily that calling it in an arbitrary power state is safe.

## B. Direct STM privilege-call inventory

The inspected, identical STM content used by both IOS58 and IOS80 had **39 direct ARM BL callsites** to its `ACRRegWrite` syscall-0x56 veneer. Register-offset provenance was resolved for every direct site, including **14** that had been conservatively unclassified in a shorter first scan.

| Hardware target (offset from Hollywood base) | Count |
| --- | ---: |
| `0x0E0` — HW_GPIO_OUT | **7** |
| `0x0E4` — HW_GPIO_DIR | **1** |
| `0x0FC` — HW_GPIO_OWNER | **3** |
| `0x0C0` — HW_GPIOB_OUT | **0** |
| Other power/reset/video/clock offsets | **28** |
| **Total** | **39** |

Of the 7 GPIO_OUT direct writers, immediate/observed call-flow effects are for **shutdown bit1, fan bit2, Broadway DC/DC bit3, and slot LED bit5** — not sensor-bar bit8.

A subtle exception matters: the slot-LED helper at **0x20301734** uses an **unmasked** `input << 5`. Viewed in isolation, an input of 8 could put a bit into 0x100, so **do not claim the instruction can only affect bit5 for every hypothetical caller**. Two observed **direct** callsites (0x20301A00 and 0x20301A9C) pass only 0/1 on their analyzed paths; therefore neither observed direct caller sets bit8 through that helper. Indirect invocations were **not exhaustively excluded**.

Three GPIO_OWNER direct writes (at 0x20301010, 0x20301910, 0x20301AB0) change bit5, with a corresponding DIR bit5 output setter. The two `#0x100` ARM immediate occurrences found by the corrected scan refer to **HW_IFPOWER offset 0x198** and to LED-pattern counter arithmetic, not a proven GPIO8 setter.

## C. Kernel privilege / address mapping barriers

In both inspected IOS kernels:

- **syscall 0x56, ACRRegWrite**, branches to reject any caller with process ID **other than STM PID14**. This is a directly observed Thumb branch, not a guess from device names.
- The kernel's register-offset allowlist does not authorize `0xC0` (GPIOB_OUT) through 0x56; the `0xE0`/ `0xFC` path is **special** and does not grant arbitrary GPIO access to other PIDs.
- The kernel has a Hollywood MMIO mapping descriptor for **0x0D800000** of size **0xD0000**, **domain15**, which is privileged in the documented default scheme. A static descriptor is **not** proof against every later process-specific mapping.
- IOS native module-launch syscall 0x5A has a **UID0 gate**; its existence is not permission for an unprivileged client to load new Starlet code.

For context, the public GPIO documentation states that **HW_GPIO_OWNER bit8=1** selects Broadway access via **GPIOB**, whereas **bit8=0** uses Starlet's bank. Its *typical* ownership setting should **not** be assumed for every standby runtime state.

## D. Cross-module caveat

A TMD-verified scan of all **19 IOS58** and **15 IOS80** content records found **32 and 30** distinct `/dev` path strings respectively; neither had an explicitly named GPIO/IR/sensorbar device. Strings alone **cannot** prove lack of an API (aliases, computed strings and ioctl behavior exist). More broadly, one additional bounded ARM literal-address scan did not identify a ready public sensor GPIO8 writer outside STM; it **does not** constitute a complete interprocedural proof across every IOS service.

`/dev/stm/eventhook` is for STM event notifications, not established arbitrary waveform output. Do not apply the original-Wii conclusion to vWii-only commands such as `0x8001`.

## Claims, carefully limited

- **Supported:** no known stock STM immediate command to supply programmable ~38kHz sensor-bar bit8 output on the two inspected IOS versions, via the examined direct call paths.
- **Unsupported:** “no possible undocumented IOS mechanism”, “all 32-bit ioctl values tested”, “yellow sensor-bar rail has no power”, “custom privileged drivers are impossible”, or “stock IOS will always have identical bytes”.
- **Also required independently:** voltage on this exact board, permitted GPIO ownership changes, runnable real-time code during WC24, and authenticated timely inbound command delivery.

**Result is a case-specific API-negative with branch checks, NOT a proof of physical impossibility.**

### Public references

- [WiiBrew STM immediate](https://wiibrew.org/wiki//dev/stm/immediate)
- [WiiBrew eventhook](https://wiibrew.org/wiki//dev/stm/eventhook)
- [WiiBrew Hollywood GPIO](https://wiibrew.org/wiki/Hollywood/GPIOs)
- [WiiBrew IOS syscalls](https://wiibrew.org/wiki/IOS/Syscalls)

Detailed method and reproducibility limitations: [Method](07-methodology-and-reproduction.md).
