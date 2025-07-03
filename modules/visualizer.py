import streamlit as st
import pandas as pd
import plotly.express as px

def display_task_table(df: pd.DataFrame):
    """
    แสดงตาราง tasks
    """
    # เลือกคอลัมน์ที่จะแสดง (ไม่แสดงคอลัมน์ที่ใช้สำหรับ sort)
    display_df = df[["Week", "Assign To", "Task Name", "Department", "Collab", "Due Date", "Completed?"]].copy()
    
    # แสดงตารางด้วย st.dataframe เพื่อให้สามารถ sort ได้
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Week": st.column_config.TextColumn("สัปดาห์", width="medium"),
            "Assign To": st.column_config.TextColumn("มอบหมายให้", width="medium"),
            "Task Name": st.column_config.TextColumn("ชื่องาน", width="large"),
            "Department": st.column_config.TextColumn("แผนก", width="medium"),
            "Collab": st.column_config.TextColumn("ผู้ร่วมงาน", width="medium"),
            "Due Date": st.column_config.TextColumn("กำหนดส่ง", width="small"),
            "Completed?": st.column_config.TextColumn("สถานะ", width="small")
        }
    )

def display_task_stats(filtered_df: pd.DataFrame):
    """
    แสดงสถิติของ tasks
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Tasks ทั้งหมด", len(filtered_df))
    
    with col2:
        completed_count = len(filtered_df[filtered_df["Completed_Bool"] == True])
        st.metric("✅ เสร็จแล้ว", completed_count)
    
    with col3:
        pending_count = len(filtered_df[filtered_df["Completed_Bool"] == False])
        st.metric("⏳ ยังไม่เสร็จ", pending_count)
    
    with col4:
        completion_rate = (completed_count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("📈 อัตราเสร็จ", f"{completion_rate:.1f}%")

def display_person_summary(person_summary: pd.DataFrame):
    """
    แสดงข้อมูลสรุปตามบุคคล
    """
    # Create a copy of the dataframe to avoid modifying the original
    styled_df = person_summary.copy()
    
    # Add a column for styling based on completion rate
    if "อัตราเสร็จ (%)" in styled_df.columns:
        # Ensure the column is a numeric type
        styled_df["อัตราเสร็จ (%)"] = pd.to_numeric(styled_df["อัตราเสร็จ (%)"], errors='coerce')
        
        # Create a styled dataframe
        styled_df = styled_df.style.apply(lambda x: ['background-color: #FF0000' 
                                  if v < 0.3 else 'background-color: #FFA500' 
                                  if v < 0.7 else 'background-color: #0000FF' 
                                  for v in x], 
                                  subset=['อัตราเสร็จ (%)'])
    
    st.dataframe(
        styled_df if isinstance(styled_df, pd.DataFrame) else person_summary,
        use_container_width=True,
        column_config={
            "จำนวนงานทั้งหมด": st.column_config.NumberColumn("จำนวนงานทั้งหมด"),
            "จำนวนงานเสร็จ": st.column_config.NumberColumn("จำนวนงานเสร็จ"),
            "อัตราเสร็จ (%)": st.column_config.ProgressColumn(
                "อัตราเสร็จ (%)", 
                min_value=0, 
                max_value=1,
            )
        }
    )

def display_section_summary(section_summary: pd.DataFrame):
    """
    แสดงข้อมูลสรุปตาม Section
    """
    # Create a copy of the dataframe to avoid modifying the original
    styled_df = section_summary.copy()
    
    # Add a column for styling based on completion rate
    if "อัตราเสร็จ (%)" in styled_df.columns:
        # Ensure the column is a numeric type
        styled_df["อัตราเสร็จ (%)"] = pd.to_numeric(styled_df["อัตราเสร็จ (%)"], errors='coerce')
        
        # Create a styled dataframe
        styled_df = styled_df.style.apply(lambda x: ['background-color: #FF0000' 
                                  if v < 0.3 else 'background-color: #FFA500' 
                                  if v < 0.7 else 'background-color: #0000FF' 
                                  for v in x], 
                                  subset=['อัตราเสร็จ (%)'])
    
    st.dataframe(
        styled_df if isinstance(styled_df, pd.DataFrame) else section_summary,
        use_container_width=True,
        column_config={
            "จำนวนงานทั้งหมด": st.column_config.NumberColumn("จำนวนงานทั้งหมด"),
            "จำนวนงานเสร็จ": st.column_config.NumberColumn("จำนวนงานเสร็จ"),
            "อัตราเสร็จ (%)": st.column_config.ProgressColumn(
                "อัตราเสร็จ (%)", 
                min_value=0, 
                max_value=1
            )
        }
    )

def display_timeline_chart(timeline_summary: pd.DataFrame):
    """
    แสดงกราฟ timeline โดยใช้วันที่เริ่มต้นของสัปดาห์
    """
    # แปลง Week_Start_Date เป็น format ที่อ่านง่าย (dd/mm/yyyy)
    timeline_summary['Display_Date'] = pd.to_datetime(timeline_summary['Week_Start_Date']).dt.strftime('%d/%m/%Y')
    
    fig = px.line(
        timeline_summary,
        x="Display_Date",  # ใช้วันที่เริ่มต้นของสัปดาห์แทน Week
        y="Task Name",
        color="Department",
        markers=True,
        title="Timeline: จำนวนงานแต่ละแผนกตามวันที่เริ่มต้นของสัปดาห์"
    )
    fig.update_layout(xaxis_title="วันที่", yaxis_title="จำนวนงาน", legend_title="แผนก")
    st.plotly_chart(fig, use_container_width=True)

def display_main_task_stats(stats: dict):
    """
    แสดงสถิติของ tasks หลัก
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Tasks ทั้งหมด", stats["total_tasks"])
    
    with col2:
        st.metric("✅ เสร็จแล้ว", stats["completed_tasks"])
    
    with col3:
        st.metric("⏳ รอดำเนินการ", stats["pending_tasks"])
    
    with col4:
        st.metric("📝 Subtasks ทั้งหมด", stats["total_subtasks"])
    
    # แสดงความคืบหน้า
    st.progress(stats["completion_rate"] / 100)
    st.write(f"**ความคืบหน้าโดยรวม: {stats['completion_rate']:.1f}%**")
