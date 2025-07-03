# Asana Tasks Report Dashboard

แอปพลิเคชันสำหรับแสดงรายงานงานจาก Asana ในรูปแบบ Dashboard

## การติดตั้ง

1. ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

2. รันแอปบน Web Browser:
```bash
streamlit run app.py
```

3. สร้างแอปพลิเคชันสำหรับ Desktop:
   - สำหรับ Windows:
   ```bash
   python build_windows_app.py
   ```
   - สำหรับ macOS:
   ```bash
   python build_macos_app.py
   ```

## คุณสมบัติ

- แสดงรายการงานทั้งหมดจาก Asana
- กรองข้อมูลตามบุคคล, สถานะ, และสัปดาห์
- แสดงสถิติงานที่เสร็จและยังไม่เสร็จ
- สรุปข้อมูลตามบุคคลและแผนก
- แสดงกราฟ Timeline จำนวนงานแต่ละแผนกในแต่ละสัปดาห์
- รองรับการทำงานทั้งแบบ Web Application และ Desktop Application (Windows และ macOS)
- สามารถเลือกไฟล์ข้อมูลได้ทั้งแบบอัปโหลดและแบบเลือกจากเครื่อง
- UI ที่สวยงามและใช้งานง่าย

## โครงสร้างโปรเจค

```
├── app.py                  # ไฟล์หลักของแอปพลิเคชัน
├── app_original.py         # ไฟล์เดิมก่อนแยกโมดูล (สำรอง)
├── desktop_app.py          # ไฟล์สำหรับรันแบบ Desktop Application
├── build_windows_app.py    # สคริปต์สร้าง Windows Desktop App
├── build_macos_app.py      # สคริปต์สร้าง macOS Desktop App
├── run_app.bat             # สคริปต์รันแอปบน Windows
├── run_app.sh              # สคริปต์รันแอปบน macOS/Linux
├── Task.py                 # คลาสสำหรับจัดการข้อมูล Task
├── modules/                # โฟลเดอร์เก็บโมดูลต่าง ๆ
│   ├── __init__.py
│   ├── data_loader.py      # โมดูลสำหรับโหลดข้อมูล
│   ├── task_processor.py   # โมดูลสำหรับประมวลผลข้อมูล Task
│   ├── visualizer.py       # โมดูลสำหรับการแสดงผลกราฟและตาราง
│   ├── utils.py            # โมดูลสำหรับฟังก์ชันยูทิลิตี้ต่าง ๆ
│   ├── desktop_utils.py    # โมดูลสำหรับฟังก์ชัน Desktop App
│   └── file_dialog.py      # โมดูลสำหรับไดอะล็อกเลือกไฟล์
├── static/                 # โฟลเดอร์เก็บไฟล์ static
│   └── css/                # โฟลเดอร์เก็บไฟล์ CSS
│       └── tabler-style.css
├── tasks.json              # ไฟล์ข้อมูล Task จาก Asana
├── task_template.json      # ไฟล์เทมเพลตสำหรับ Task
├── requirements.txt        # รายการ dependencies
├── README.md               # ไฟล์ README หลัก
├── SETUP.md                # คำแนะนำการติดตั้ง
└── DESKTOP_APP.md          # คำแนะนำการใช้งาน Desktop App
```

## เทคโนโลยีที่ใช้

- Python 3.12
- Streamlit
- Pandas
- Plotly

## การพัฒนาเพิ่มเติม

แอปนี้สามารถพัฒนาต่อได้ เช่น:
- เพิ่มการเชื่อมต่อกับ Asana API โดยตรง
- เพิ่มการแสดงผลกราฟแบบอื่น ๆ
- เพิ่มการส่งออกรายงานในรูปแบบ PDF หรือ Excel
- เพิ่มการแจ้งเตือนเมื่อใกล้ถึงกำหนดส่งงาน
