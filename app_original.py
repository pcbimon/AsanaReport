import streamlit as st
from datetime import datetime
import pandas as pd

# นำเข้าโมดูลที่สร้างขึ้นใหม่
from modules.data_loader import load_tasks_data
from modules.task_processor import (
    process_subtasks, apply_filters, get_all_assignees,
    create_person_summary, create_section_summary,
    prepare_timeline_data, get_task_statistics
)
from modules.visualizer import (
    display_task_table, display_task_stats,
    display_person_summary, display_section_summary,
    display_timeline_chart, display_main_task_stats
)
from modules.utils import get_current_time

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Asana Tasks Report",
    page_icon="📋",
    layout="wide"
)

# หัวข้อหลัก
st.title("📋 Asana Tasks Report Dashboard")

# โหลดข้อมูล tasks
tasks_file = "tasks.json"
tasks = load_tasks_data(tasks_file)

# ประมวลผล subtasks
if tasks:
    subtasks_df = process_subtasks(tasks)
    
    if not subtasks_df.empty:
        st.markdown("---")
        st.subheader("📋 ตาราง Tasks ทั้งหมด")
        
        # สร้าง filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Filter ตามคน (Assign To และ Collab)
            all_assignees = get_all_assignees(subtasks_df)
            selected_assignees = st.multiselect(
                "กรองตาม บุคคล (มอบหมาย/ร่วมงาน):",
                options=["ทุกคน"] + all_assignees,
                default=["ทุกคน"]
            )
        
        with col2:
            # Filter ตาม completion status
            completion_filter = st.selectbox(
                "กรองตามสถานะ:",
                options=["ทั้งหมด", "เสร็จแล้ว", "ยังไม่เสร็จ"]
            )
        
        with col3:
            # Filter ตาม Week
            all_weeks = sorted(subtasks_df["Week"].unique())
            selected_weeks = st.multiselect(
                "กรองตามสัปดาห์:",
                options=["ทุกสัปดาห์"] + list(all_weeks),
                default=["ทุกสัปดาห์"]
            )
        
        # Apply filters
        filtered_df = apply_filters(
            subtasks_df,
            selected_assignees,
            completion_filter,
            selected_weeks
        )
        
        # แสดงสถิติ
        st.markdown("### 📊 สถิติ")
        display_task_stats(filtered_df)
        
        # แสดงตาราง
        st.markdown("### 📋 รายละเอียด")
        display_task_table(filtered_df)
        
        # สรุปตามคน และ สรุปตาม Section
        st.markdown("---")
        col_person, col_section = st.columns(2)
        
        with col_person:
            st.markdown("### 👥 สรุปตามบุคคล")
            person_summary = create_person_summary(filtered_df)
            display_person_summary(person_summary)
        
        with col_section:
            st.markdown("### 🏢 สรุปตาม Section")
            section_summary, section_df = create_section_summary(filtered_df)
            
            if section_summary is not None:
                display_section_summary(section_summary)
                
                # กราฟ Timeline
                timeline_summary = prepare_timeline_data(filtered_df)
                if timeline_summary is not None:
                    display_timeline_chart(timeline_summary)
            else:
                st.write("ไม่พบข้อมูล Section")

else:
    st.warning("ไม่พบข้อมูล subtasks ในระบบ")

# แสดงข้อมูลสรุป Tasks หลัก
if tasks:
    st.markdown("---")
    st.subheader("📊 สรุปข้อมูล Tasks")
    
    # สถิติพื้นฐาน
    stats = get_task_statistics(tasks)
    display_main_task_stats(stats)
    
    st.markdown("---")
else:
    st.warning("ไม่พบข้อมูล tasks หรือไม่สามารถโหลดข้อมูลได้")

# แสดงวันที่และเวลาปัจจุบัน
current_time = get_current_time()
st.caption(f"เวลาปัจจุบัน: {current_time}")
st.caption(f"ข้อมูลจากไฟล์: {tasks_file}")
