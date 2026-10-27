"""Public arithmetic and metadata consistency tests ONLY.

This file DOES NOT re-run the original NAND/firmware static analysis.
Passing tests are not independent evidence that any real IOS dispatch result,
pin voltage, waveform, GPIO ownership, or hardware power consumption is correct.
"""
import json
import unittest
from pathlib import Path

EVIDENCE = json.loads((Path(__file__).resolve().parents[1] /
                       "evidence" / "audit-metrics.json").read_text(encoding="utf-8"))

class SummaryChecks(unittest.TestCase):
    def test_command_space(self):
        c = EVIDENCE["stm_ioctl_u16"]
        self.assertEqual(c["tested_inputs"], c["domain_max"] - c["domain_min"] + 1)
        self.assertEqual(len(c["recognized_hex"]), c["recognized_count"])
        self.assertEqual(len(set(c["recognized_hex"])), c["recognized_count"])
        self.assertEqual(c["default_count"], c["tested_inputs"] - c["recognized_count"])
        self.assertFalse(c["u32_exhaustively_tested"])

    def test_writer_inventory(self):
        w = EVIDENCE["stm_direct_acr_register_writers"]
        self.assertEqual(sum(w["counts_by_offset"].values()), w["total"])
        self.assertEqual(w["resolved_offsets"], w["total"])
        self.assertEqual(w["counts_by_offset"]["0x0E0"], w["gpio_e0_direct_calls"])
        self.assertEqual(w["counts_by_offset"]["0x0FC"], w["gpio_owner_fc_direct_calls"])
        self.assertEqual(w["counts_by_offset"]["0x0E4"], w["gpio_dir_e4_direct_calls"])
        self.assertEqual(w["gpio_b_out_0xc0_direct_calls"], 0)
        self.assertTrue(all(x in (1, 2, 3, 5) for x in w["observed_gpio_e0_bits"]))
        self.assertFalse(w["dynamic_shift_helper_indirect_callers_excluded"])

    def test_frame_math(self):
        x = EVIDENCE["panasonic_frame_model"]
        self.assertEqual(x["source_timer_hz_nominal"] //
                         x["timer_ticks_per_carrier_cycle"], x["carrier_hz_nominal"])
        for prefix in ("on", "off"):
            raw = bytes.fromhex(x[f"{prefix}_hex"])
            self.assertEqual(len(raw)*8, x["bits_per_command"])
            ones = sum(byte.bit_count() for byte in raw)
            self.assertEqual(ones, x[f"{prefix}_ones"])
            zeros = x["bits_per_command"] - ones
            frame = (x["header_mark_us"] + x["header_space_us"] +
                     x["bits_per_command"]*x["bit_mark_us"] +
                     ones*x["one_space_us"] + zeros*x["zero_space_us"] +
                     x["trail_mark_us"])
            self.assertEqual(frame, x[f"{prefix}_ideal_frame_us"])

    def test_claim_boundaries(self):
        self.assertFalse(EVIDENCE["device_runtime_tests"])
        self.assertEqual(EVIDENCE["sensor_positive_voltage_yellow"], "unknown_not_measured")
        self.assertEqual(EVIDENCE["console_wall_watt_measurements"], "none")
        self.assertFalse(EVIDENCE["panasonic_frame_model"]["yellow_real_waveform_tested"])
        self.assertFalse(EVIDENCE["libogc_idle"]["processor_doze_measured"])
        self.assertFalse(EVIDENCE["libogc_idle"]["green_watt_savings_measured"])

if __name__ == "__main__":
    unittest.main()
