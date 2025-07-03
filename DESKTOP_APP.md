# วิธีการใช้งาน Asana Tasks Report เป็น Desktop Application

## วิธีการสร้าง Desktop Application

### ขั้นตอนการเตรียมการ

1. ติดตั้ง Python 3.x (แนะนำเวอร์ชัน 3.10+)
   - ดาวน์โหลดได้จาก: https://www.python.org/downloads/

2. ติดตั้ง dependencies ที่จำเป็น
   ```
   pip install -r requirements.txt
   ```

### สร้าง Desktop Application สำหรับ Windows

1. รันคำสั่งต่อไปนี้เพื่อสร้าง Windows application:
   ```
   python build_windows_app.py
   ```

2. รอให้กระบวนการสร้างเสร็จสมบูรณ์ (อาจใช้เวลาสักครู่)

3. ไฟล์ executable จะอยู่ในโฟลเดอร์ `dist/AsanaReportApp`

4. คุณสามารถคัดลอกโฟลเดอร์ `AsanaReportApp` ไปยังตำแหน่งที่ต้องการและเรียกใช้ `AsanaReportApp.exe`

### สร้าง Desktop Application สำหรับ macOS

1. รันคำสั่งต่อไปนี้เพื่อสร้าง macOS application:
   ```
   python build_macos_app.py
   ```

2. รอให้กระบวนการสร้างเสร็จสมบูรณ์ (อาจใช้เวลาสักครู่)

3. แอปพลิเคชันจะอยู่ในโฟลเดอร์ `dist` ชื่อ `AsanaReportApp.app`

4. คุณสามารถย้ายแอป `AsanaReportApp.app` ไปยัง Applications folder หรือตำแหน่งอื่นที่ต้องการ

## วิธีการใช้งาน Desktop Application

1. เรียกใช้แอปพลิเคชัน:
   - Windows: เปิด `AsanaReportApp.exe`
   - macOS: เปิด `AsanaReportApp.app`

2. แอปพลิเคชันจะเปิดขึ้นในหน้าต่างของตัวเอง โดยไม่จำเป็นต้องใช้เว็บเบราว์เซอร์

3. คุณสามารถเลือกไฟล์ tasks.json ได้ 2 วิธี:
   - ลากไฟล์ JSON มาวางในพื้นที่อัปโหลด
   - คลิกปุ่ม "เลือกไฟล์จากเครื่อง" เพื่อเปิด File Explorer หรือ Finder และเลือกไฟล์

4. หลังจากเลือกไฟล์ แอปพลิเคชันจะประมวลผลและแสดงรายงานตามปกติ

## ข้อควรรู้

- หากมีการอัปเดตแอปพลิเคชัน คุณจำเป็นต้องสร้าง Desktop Application ใหม่
- Desktop Application จะมีขนาดไฟล์ค่อนข้างใหญ่ เนื่องจากต้องรวม Python runtime และ libraries ทั้งหมดไว้ในไฟล์เดียว
- หากพบปัญหาการใช้งาน ให้ลองรันในโหมด Web Application ด้วยคำสั่ง `streamlit run app.py` เพื่อตรวจสอบว่าเป็นปัญหาจากโค้ดหรือจากการสร้าง Desktop Application
