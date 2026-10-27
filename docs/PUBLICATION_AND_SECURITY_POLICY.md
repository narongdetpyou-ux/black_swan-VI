# Public repository publication policy — pending checks

วันที่: 2026-10-27 · ใช้กับ `black_swan-VI` ซึ่งปัจจุบันเป็น **public repository**

## เหตุผลที่ยังไม่เผยแพร่ source archive ทั้งชุด

1. เอกสารชุดต้นทางระบุว่า credential เก่าเคยอยู่ในประวัติโครงการ; มีบันทึกว่าทำ Git history cleanup แล้ว แต่ **ยังไม่มี issuer confirmation ว่า revoke/rotate เสร็จสิ้น**. การลบ Git history ไม่ทำให้ credential ถูกเพิกถอน.
2. ZIP ต้นทางระบุ **GNU GPL v3** ขณะที่ repository ปลายทางมี `LICENSE` เป็น **Apache 2.0**. ต้องให้เจ้าของสิทธิ์ตรวจ provenance, การใช้ร่วมกัน/การเผยแพร่ และ attribution ก่อนย้าย source code.
3. Snapshot อาจมี telemetry, ground truth, artifact หรือข้อมูลจาก controlled environment ที่ไม่เหมาะกับ public distribution.
4. ยังไม่ยืนยัน canonical source tree หรือ differential tests สำหรับ runtime environments.

## เกณฑ์สำหรับการเผยแพร่รอบต่อไป

- **Security:** credential issuer ยืนยัน revoke/rotate; secret scan ทั้ง current tree, bundled archives และประวัติที่เกี่ยวข้อง; ห้ามเก็บ token ใน issue/PR/log.
- **License:** ตกลงกับผู้ถือสิทธิ์ว่าสามารถเผยแพร่ส่วนใดภายใต้ license ใด; รักษา notices และ provenance ที่จำเป็น.
- **Data:** ตรวจสิทธิ์ dataset, ข้อมูลส่วนบุคคล, identifiers, hidden labels และ data-leakage risk; ไม่ commit raw/private telemetry.
- **Reproducibility:** freeze chosen snapshots and per-file hashes; resolve conflicting versions; รัน tests/CI บน target environment ก่อน promotion.
- **Review:** เปิด pull request พร้อมรายการไฟล์ที่คัดกรองและผลตรวจ security/license/data. หากยังไม่มีหลักฐาน ให้ถือว่า source release เป็น **BLOCKED**.

## Scope ของการอัปเดตครั้งนี้

เผยแพร่เฉพาะ project summary, evidence limitations, roadmap และ checksum index ของไฟล์ input. **ไม่ได้**นำ source, ZIP, credentials, direct identifiers, raw telemetry หรือ hidden labels เข้าสู่ repository. ข้อความนี้ไม่ถือเป็นการรับรองว่า GitHub นี้มี build ที่รันใช้งานได้.
