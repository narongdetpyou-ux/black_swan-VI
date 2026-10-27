# black_swan-VI

**Black Swan / ABC_AI — evidence-first project documentation**

> อัปเดต: 2026-10-27 (Asia/Bangkok) · **DOCUMENTATION-ONLY / NOT PRODUCTION-READY**

Repository นี้เป็น public และปัจจุบันเผยแพร่ **เอกสารสรุปจาก snapshot ของโครงการที่ตรวจทานแล้ว**; ยังไม่ได้รวม source code, raw telemetry, credentials หรือ artifact สำหรับ build/runtime. เนื้อหา ZIP ต้นทางหกชุดไม่ได้ถูกนำมาอัปโหลดที่นี่.

## เริ่มอ่าน

- [บันทึกความรู้และสถานะหลักฐาน (ภาษาไทย)](docs/PROJECT_MEMORY_AUDIT_TH.md) — ขอบเขตความทรงจำที่ตรวจสอบได้, ผลการทดลองและข้อจำกัด
- [Development roadmap (ภาษาไทย)](docs/DEVELOPMENT_ROADMAP_TH.md) — Stage gates 0–3, BLK-001 ถึง BLK-013 และ guardrails
- [รายการ ZIP ต้นทางและ SHA-256](docs/SOURCE_SNAPSHOTS_SHA256.md) — manifest ของอินพุตที่ตรวจ ไม่ใช่ไฟล์ที่อัปโหลด
- [นโยบายความปลอดภัยและการเผยแพร่](docs/PUBLICATION_AND_SECURITY_POLICY.md) — เงื่อนไขก่อนอนุญาตให้นำโค้ด/ข้อมูลขึ้น public repository

## สถานะย่อ

| ประเด็น | สถานะ |
|---|---|
| Logic v8 | มีหลักฐานจาก snapshot บน synthetic data; ไม่ใช่ real-world certification |
| Controlled telemetry | รอบ 2026-09-20: **REJECTED** โดย data admission |
| Runtime | Test record Python 3.13.5 มี failure 1/85 ใน timeout recovery; ยังต้อง differential check บน Python 3.12 |
| Independent blind evaluation | ยังไม่มีหลักฐานผ่าน gate |
| ABC Memory | Proposal สำหรับ analyst-side offline ablation; ไม่ควบคุม detector |
| Credential incident | ยังไม่ยืนยัน revoke/rotate ที่ issuer |
| Source publication | **BLOCKED** ระหว่างตรวจ secret, data permission, provenance และ licensing |

## License / security note

GitHub repository นี้มี `LICENSE` เป็น Apache 2.0 ขณะที่ snapshot โครงการต้นทางมี GNU GPL v3. **อย่าสมมุติว่า license ของ code ต้นทางเปลี่ยนตาม repository** ต้องตรวจสิทธิ์และ compatibility ก่อนนำโค้ดมาเผยแพร่. ห้าม commit secrets, direct identifiers, hidden labels หรือ raw/private telemetry.

## หลักการพัฒนา

รักษา frozen baseline, ตรวจ runtime และ credential, สร้าง dataset ที่ผ่านทั้ง contract และ quality admission, ประเมินด้วย independent chronological blind holdout แล้วจึงพิจารณาการใช้งานจริง. แยก security alerts ออกจาก operational escalations และไม่ตีความ `NO_SECURITY_ALERT` ว่าเป็นหลักฐานความปลอดภัย.

---
*เอกสารนี้เป็นการสรุปหลักฐานที่เข้าถึงได้ ณ วันที่ระบุ ไม่ใช่การรับรองความสมบูรณ์ของ source code หรือทุกความทรงจำของโปรเจกต์.*
