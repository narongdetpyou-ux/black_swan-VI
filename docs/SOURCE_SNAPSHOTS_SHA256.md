# Source snapshots — local input checksum index

วันที่ตรวจ: 2026-10-27 · SHA-256 คำนวณจากไฟล์ ZIP ที่แนบในโครงการ ณ รอบตรวจนี้

**หมายเหตุ:** ตารางนี้เป็นดัชนีตรวจสอบความถูกต้องของอินพุต **ไม่ใช่หลักฐานว่า ZIP ถูกอัปโหลดเข้า GitHub**. Repository นี้เก็บเฉพาะเอกสารสรุปที่คัดกรองแล้วเท่านั้น.

| ชื่อไฟล์ต้นทาง | Files in ZIP | SHA-256 |
|---|---:|---|
| `back_swan-codex-colab-verified-runs.zip` | 92 | `6b8e8b043520402cbf806a7873ab89005946236bb5b5ca798abaf915243fa69d` |
| `back_swan-codex-collect-required-telemetry-evidence.zip` | 110 | `56ec418ee3ef3e228ee132f8d99f0bdc767e53c645cca4b18a5e34cae20548de` |
| `back_swan-codex-organize-v8-recovery.zip` | 69 | `ec1afbe45ca41ef0d9174c90de15115bf40c76ea0c9904cec888a3627b63f8f6` |
| `back_swan-codex-storage-experiment-workflows.zip` | 83 | `7d2166cad58599cba5731c77064a2cec57152ea5c06caa44090d26873a6c94f8` |
| `back_swan-codex-test-functionality.zip` | 19 | `599ca21745d12147bf92267e485435cf2ec661275fa761e67a26d1de44ef0af8` |
| `back_swan-validation-real-world-dataset-phase1.zip` | 100 | `30875529f666be4aff4c2f5eb109caba003e3ad6938acad39fc6bdcc2e9d83f8` |

**Cross-snapshot comparison:** 473 file occurrences, 126 unique relative paths, 10 paths with different content across available versions. แฮช ZIP เป็น transport-level digest ไม่ทดแทน per-file selection manifest; ยังไม่มีการประกาศ canonical HEAD จากข้อมูลเหล่านี้.

ก่อนนำ code/data เข้าสู่ repository ต้องระบุ version สำหรับไฟล์ที่ขัดแย้ง, บันทึก per-file provenance/hashes, ตรวจ secret/license/authorization และรัน tests ในสภาพแวดล้อมที่กำหนด.
