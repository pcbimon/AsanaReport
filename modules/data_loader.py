import streamlit as st
import json
import os
from typing import List
from Task import Task

@st.cache_data
def load_tasks_data(file_source):
    """
    อ่านข้อมูล tasks จากไฟล์ JSON และแปลงเป็น Task objects
    ใช้ @st.cache_data เพื่อ cache ข้อมูลและไม่ต้องอ่านใหม่ทุกครั้ง
    
    สามารถรับได้ทั้ง:
    - file_path (str): เส้นทางไฟล์ JSON
    - uploaded_file (UploadedFile): ไฟล์ที่อัปโหลดผ่าน st.file_uploader
    """
    try:
        with st.spinner("กำลังโหลดข้อมูล tasks..."):
            # ตรวจสอบว่าเป็น uploaded file หรือ file path
            if hasattr(file_source, 'read'):
                # กรณีเป็น uploaded file
                data = json.loads(file_source.read().decode('utf-8'))
            else:
                # กรณีเป็น file path (string)
                if not os.path.exists(file_source):
                    st.error(f"ไม่พบไฟล์: {file_source}")
                    return []
                
                with open(file_source, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            
            # ตรวจสอบว่ามี key "data" หรือไม่
            if "data" not in data:
                st.error("ไฟล์ JSON ไม่มีโครงสร้าง 'data' array")
                return []
            
            tasks_data = data["data"]
            st.info(f"พบข้อมูล {len(tasks_data)} tasks")
            
            # แปลงข้อมูลเป็น Task objects
            tasks = []
            progress_bar = st.progress(0)
            
            for i, task_data in enumerate(tasks_data):
                try:
                    task = Task.from_dict(task_data)
                    tasks.append(task)
                    # อัพเดต progress bar
                    progress_bar.progress((i + 1) / len(tasks_data))
                except Exception as e:
                    st.warning(f"ไม่สามารถ parse task ID {task_data.get('gid', 'unknown')}: {str(e)}")
                    continue
            
            progress_bar.empty()
            st.success(f"โหลดข้อมูลสำเร็จ: {len(tasks)} tasks")
            return tasks
            
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON: {str(e)}")
        return []
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return []
