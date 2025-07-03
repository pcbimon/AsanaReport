# วิธีการติดตั้งและรัน Asana Tasks Report Dashboard

## ขั้นตอนการติดตั้ง

1. ติดตั้ง Python 3.x (แนะนำเวอร์ชัน 3.10+)
   - ดาวน์โหลดได้จาก: https://www.python.org/downloads/

2. โคลนหรือดาวน์โหลดโปรเจคนี้มาไว้ในเครื่อง

3. เปิด Command Prompt หรือ PowerShell และเข้าไปที่โฟลเดอร์ของโปรเจค
   ```
   cd path\to\AsanaReport
   ```

4. (แนะนำ) สร้าง virtual environment เพื่อแยกแพ็คเกจของโปรเจคนี้
   ```
   python -m venv .venv
   ```

5. เปิดใช้งาน virtual environment
   - สำหรับ Windows (PowerShell):
   ```
   .\.venv\Scripts\Activate.ps1
   ```
   - สำหรับ Windows (Command Prompt):
   ```
   .\.venv\Scripts\activate.bat
   ```

6. ติดตั้ง dependencies ที่จำเป็น
   ```
   pip install -r requirements.txt
   ```

## วิธีการรันแอปพลิเคชัน

### วิธีที่ 1: รันเป็น Web Application

1. หลังจากติดตั้งเสร็จแล้ว รันคำสั่งนี้เพื่อเริ่มแอปพลิเคชัน
   ```
   streamlit run app.py
   ```

2. เว็บเบราว์เซอร์จะเปิดขึ้นโดยอัตโนมัติ หรือคุณสามารถเข้าถึงแอปได้ที่:
   ```
   http://localhost:8501
   ```

### วิธีที่ 2: สร้างและรันเป็น Desktop Application

#### Windows
1. สร้าง Desktop Application สำหรับ Windows:
   ```
   python build_windows_app.py
   ```

2. หลังจากการสร้างเสร็จสมบูรณ์ ไฟล์ executable จะอยู่ใน `dist/AsanaReportApp`
   ให้เปิดโฟลเดอร์นั้นและเรียกใช้ไฟล์ `AsanaReportApp.exe`

#### macOS
1. สร้าง Desktop Application สำหรับ macOS:
   ```
   python build_macos_app.py
   ```

2. หลังจากการสร้างเสร็จสมบูรณ์ แอปพลิเคชันจะอยู่ใน `dist/AsanaReportApp.app`
   ให้เปิดโฟลเดอร์ `dist` และเรียกใช้แอป `AsanaReportApp.app`

## ข้อมูลเพิ่มเติม

- หากต้องการใช้ข้อมูล tasks อื่น ให้วางไฟล์ JSON ที่มีชื่อว่า `tasks.json` ไว้ในโฟลเดอร์หลักของโปรเจค
- โครงสร้างของไฟล์ JSON ต้องมี key "data" ที่เป็น array ของ tasks ตามโครงสร้างของ Asana API

## การแก้ไขปัญหาเบื้องต้น

1. **ปัญหา: ไม่สามารถรัน streamlit ได้**
   - ตรวจสอบว่าได้ติดตั้ง streamlit แล้ว: `pip install streamlit`
   - ตรวจสอบว่า virtual environment ถูกเปิดใช้งานอยู่

2. **ปัญหา: ไม่พบไฟล์ tasks.json**
   - ตรวจสอบว่ามีไฟล์ tasks.json อยู่ในโฟลเดอร์หลักของโปรเจค
   - ตรวจสอบว่าโครงสร้างของไฟล์ JSON ถูกต้อง

3. **ปัญหา: แอปแสดงผลไม่ถูกต้อง**
   - ตรวจสอบว่าได้ติดตั้ง dependencies ทั้งหมดแล้ว: `pip install -r requirements.txt`
