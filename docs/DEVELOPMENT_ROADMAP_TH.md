# Black Swan / ABC_AI — แผนพัฒนาแบบ Evidence-first

วันที่ปรับแผน: 2026-10-27 · **ข้อเสนอ ไม่ใช่ผลการทำงานสำเร็จ**

## เป้าหมาย

รักษา Logic v8 และ threshold เป็น frozen reference จนกว่าจะมี real/controlled telemetry ที่ผ่านทั้ง data contract และ quality admission, independent labels, chronological blind holdout ที่ล็อก และการประเมินที่ตรวจสอบซ้ำได้. การผ่านขั้นนี้ยังไม่ถือว่า production-ready.

## Gate 0 — Foundation, runtime และ security (P0)

- **BLK-001:** เลือก canonical snapshot, source SHA-256, conflict manifest, environment และ immutable baseline reference โดยไม่สมมุติว่า snapshot = HEAD ของ repository นี้.
- **BLK-002:** Reproduce `test_real_timeout_kills_and_recovers_three_times` บน Python 3.12 เทียบกับ 3.13.5; บันทึก route, reason, latency, worker lifecycle และ regression evidence; ห้ามแปลง fallback เป็น benign.
- **BLK-003:** ขอหลักฐาน revoke/rotate จาก credential issuer, secret scan, restore และ integrity checks โดยไม่เก็บ secrets ใน issue/log.
- **Gate PASS:** baseline ตรวจย้อนกลับได้, runtime regression ผ่านตาม target และความเสี่ยง credential ได้รับการปิดพร้อมหลักฐานหรือคงสถานะบล็อก promotion อย่างชัดเจน.

## Gate 1 — Data admission (P1)

- **BLK-004:** ตรวจสิทธิ์, provenance, labels, cadence, source diversity และ metric compatibility ของ candidate datasets.
- **BLK-005:** แปลง raw→hourly features โดยเก็บ transformation ID, timestamps UTC, entity grouping, duplicates, gaps และ missingness.
- **BLK-006:** แยก raw/features/hidden labels; split ตามเวลา baseline→calibration→blind_test ไม่ซ้อนกัน; `blind_test_locked=true` ก่อนประเมิน.
- **BLK-007:** ตรวจ quality admission โดยอิสระ. สำหรับ hourly calibration แบบเดิมต้องมีอย่างน้อย 72 baseline history windows **สำหรับ metric ที่ใช้จริง**; ไม่บังคับว่าทั้ง dataset ต้องมีครบ 10 metrics.
- **Gate PASS:** ผ่านทั้ง schema/contract **และ** quality admission ไม่ใช่เพียง validator exit 0.

## Gate 2 — Frozen evaluation & reliability (P2)

- **BLK-008:** Freeze code/config/transform/split hashes แล้ว evaluate แบบ replay/shadow กับ blind holdout ที่ล็อก.
- **BLK-009:** รายงาน attack alert recall, benign alert rate, review burden, fallback/hold share พร้อม numerator/denominator และ source/scenario breakdown.
- **BLK-010:** ตรวจ full-path events/s, tail latency p95/p99, queue/backpressure, lost jobs, worker recovery และ long-duration soak. อย่าอ้าง 10k–20k full decisions/s โดยไม่มีหลักฐาน end-to-end.
- **BLK-011:** Reviewer อิสระตรวจ provenance, labels, leakage, reliability และทำ GO / CONDITIONAL / NO-GO decision memo.

## Gate 3 — ABC Memory (P3, optional)

- **BLK-012:** ทดลอง retrieval เพื่อช่วย analyst อ่านเคสย้อนหลัง แยก observed facts / hypotheses และกัน evidence leakage. เปรียบเทียบ v8-only, simple rules, v8+ABC retrieval.
- **BLK-013:** Human-reviewed paired test ด้าน report correctness, review time, unsupported explanation และ workload; ไม่ให้ retrieval เปลี่ยน detector route หรือ threshold.

## Guardrails

- ไม่ใช้ผล synthetic แทน real validation.
- ไม่ใช้ blind holdout ชุดเดิมในการปรับโมเดลแล้วอ้างว่า independent.
- ไม่มี credential, direct identifiers หรือ hidden labels ใน public GitHub.
- หากไม่มี regression/security/admission evidence ให้รายงาน BLOCKED หรือ NOT VALIDATED แทนการเดาว่าผ่าน.

รายละเอียดต้นทาง: แผน Black Swan Development Plan v1.0 (2026-10-27) ที่แนบในโครงการ. เจ้าของงาน วันครบกำหนด และ SLA ยังไม่ผ่านการยืนยัน.
