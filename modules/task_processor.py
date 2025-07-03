import pandas as pd
import re
from typing import List
from Task import Task

def process_subtasks(tasks: List[Task]) -> pd.DataFrame:
    """
    ประมวลผล subtasks ทั้งหมดและสร้าง DataFrame
    """
    def week_sort_key(week_str: str) -> pd.Timestamp:
        # ตัวอย่าง week_str: "Week of 01-07 July 2024" หรือ "Week of 7-11 July 2025"
        # รองรับทั้งเลข 1 หลัก และ 2 หลัก
        m = re.search(r'(\d{1,2})-(\d{1,2}) (\w+) (\d{4})', week_str)
        if m:
            day1, day2, month, year = m.groups()
            try:
                # แปลงวันที่โดยรองรับเลข 1 หลัก
                dt = pd.to_datetime(f"{int(day1)} {month} {year}", format="%d %B %Y")
                return dt
            except:
                return pd.NaT
        return pd.NaT
    
    subtasks_data = []
    
    for main_task in tasks:
        # ดึงวันที่จากชื่อ main task (Week of DD-DD MMMM YYYY)
        week_period = main_task.name if main_task.name.startswith("Week of") else "Unknown Week"
        week_start_date = week_sort_key(week_period)  # เพิ่มการแปลงวันที่
        
        for subtask in main_task.subtasks:
            # แปลงเป็น Task object หาก subtask ยังเป็น dict
            if isinstance(subtask, dict):
                try:
                    subtask = Task.from_dict(subtask)
                except:
                    continue
            
            # ดึงข้อมูล assignee
            assignee_name = subtask.assignee.name if subtask.assignee else "ไม่ระบุ"
            
            # ดึงข้อมูล followers และรวมชื่อด้วย ";" (ไม่รวมชื่อผู้ที่ได้รับมอบหมาย)
            followers_names = []
            for follower in subtask.followers:
                follower_name = None
                if hasattr(follower, 'name'):
                    follower_name = follower.name
                elif isinstance(follower, dict) and 'name' in follower:
                    follower_name = follower['name']
                
                # เพิ่มเฉพาะชื่อที่ไม่ใช่ผู้ที่ได้รับมอบหมาย
                if follower_name and follower_name != assignee_name:
                    followers_names.append(follower_name)
            
            collab = "; ".join(followers_names) if followers_names else "-"
            
            # ดึงข้อมูล department จาก sections ของ main task (parent)
            try:
                # ดึง section จาก main_task แทนที่จะเป็น subtask
                departments = main_task.get_section_names()
                department = "; ".join(departments) if departments else "ไม่ระบุ"
            except (AttributeError, TypeError):
                # หากไม่สามารถดึง section names ได้ ให้ดึงข้อมูลแบบ manual จาก main_task
                departments = []
                for membership in main_task.memberships:
                    if isinstance(membership, dict):
                        if membership.get('section') and membership['section'].get('name'):
                            departments.append(membership['section']['name'])
                    elif hasattr(membership, 'section') and membership.section and hasattr(membership.section, 'name'):
                        departments.append(membership.section.name)
                department = "; ".join(departments) if departments else "ไม่ระบุ"
            
            # ดึงข้อมูล due date
            due_date = subtask.due_on if subtask.due_on else "ไม่ระบุ"
            
            # สร้าง completed status
            completed_status = "✅" if subtask.completed else "❌"
            
            subtasks_data.append({
                "Week": week_period,
                "Week_Start_Date": week_start_date,  # เพิ่มคอลัมน์วันที่เริ่มต้นสัปดาห์
                "Assign To": assignee_name,
                "Task Name": subtask.name,
                "Department": department,
                "Collab": collab,
                "Due Date": due_date,
                "Completed?": completed_status,
                "Completed_Bool": subtask.completed,  # สำหรับการ sort
                "Due_Date_Sort": subtask.due_on if subtask.due_on else "9999-12-31"  # สำหรับการ sort
            })
    
    return pd.DataFrame(subtasks_data)

def apply_filters(df: pd.DataFrame, selected_assignees=None, completion_filter=None, selected_weeks=None, selected_sections=None):
    """
    กรองข้อมูลตามเงื่อนไขที่กำหนด
    """
    filtered_df = df.copy()
    
    # Filter by assignee and collaborators
    if selected_assignees and "ทุกคน" not in selected_assignees:
        # สร้าง condition สำหรับกรองทั้ง Assign To และ Collab
        condition = filtered_df["Assign To"].isin(selected_assignees)
        
        # เพิ่ม condition สำหรับ Collab
        for person in selected_assignees:
            collab_condition = filtered_df["Collab"].str.contains(person, na=False, regex=False)
            condition = condition | collab_condition
        
        filtered_df = filtered_df[condition]
    
    # Filter by completion status
    if completion_filter == "เสร็จแล้ว":
        filtered_df = filtered_df[filtered_df["Completed_Bool"] == True]
    elif completion_filter == "ยังไม่เสร็จ":
        filtered_df = filtered_df[filtered_df["Completed_Bool"] == False]
    
    # Filter by week
    if selected_weeks and "ทุกสัปดาห์" not in selected_weeks:
        filtered_df = filtered_df[filtered_df["Week"].isin(selected_weeks)]
    
    # Filter by section/department
    if selected_sections and "ทุกแผนก" not in selected_sections:
        # สร้าง mask สำหรับกรองตามแผนก
        section_mask = pd.Series(False, index=filtered_df.index)
        for section in selected_sections:
            # ใช้ str.contains เพื่อรองรับกรณีที่มีหลายแผนกในช่อง Department (คั่นด้วย ";")
            section_mask = section_mask | filtered_df["Department"].str.contains(section, na=False, regex=False)
        filtered_df = filtered_df[section_mask]
    
    # Sort by Assign To name and Due Date
    filtered_df = filtered_df.sort_values(["Assign To", "Due_Date_Sort"])
    
    return filtered_df

def get_all_assignees(df: pd.DataFrame):
    """
    รวบรวมชื่อทั้งหมดจาก Assign To และ Collab
    """
    all_assignees = set(df["Assign To"].unique())
    
    # เพิ่มชื่อจาก Collab (แยกด้วย ";")
    for collab_str in df["Collab"].unique():
        if collab_str and collab_str != "-":
            collab_names = [name.strip() for name in collab_str.split(";")]
            all_assignees.update(collab_names)
    
    return sorted(list(all_assignees))

def create_person_summary(df: pd.DataFrame):
    """
    สร้างข้อมูลสรุปตามบุคคล
    """
    person_summary = df.groupby("Assign To").agg({
        "Task Name": "count",
        "Completed_Bool": ["sum", lambda x: (x.sum() / len(x))]
    }).round(3)
    
    person_summary.columns = ["จำนวนงานทั้งหมด", "จำนวนงานเสร็จ", "อัตราเสร็จ (%)"]
    person_summary = person_summary.sort_values("อัตราเสร็จ (%)", ascending=False)
    
    return person_summary

def create_section_summary(df: pd.DataFrame):
    """
    สร้างข้อมูลสรุปตาม Section
    """
    # แยก department/section ที่มีหลายชื่อแยกด้วย ";"
    section_data = []
    for _, row in df.iterrows():
        departments = row["Department"].split(";") if row["Department"] != "ไม่ระบุ" else ["ไม่ระบุ"]
        for dept in departments:
            dept = dept.strip()
            section_data.append({
                "Section": dept,
                "Task Name": row["Task Name"],
                "Completed_Bool": row["Completed_Bool"]
            })
    section_df = pd.DataFrame(section_data)
    
    if not section_df.empty:
        section_summary = section_df.groupby("Section").agg({
            "Task Name": "count",
            "Completed_Bool": ["sum", lambda x: (x.sum() / len(x))]
        }).round(3)
        section_summary.columns = ["จำนวนงานทั้งหมด", "จำนวนงานเสร็จ", "อัตราเสร็จ (%)"]
        section_summary = section_summary.sort_values(["อัตราเสร็จ (%)", "จำนวนงานทั้งหมด"], ascending=[False, False])
        
        return section_summary, section_df
    
    return None, None

def prepare_timeline_data(df: pd.DataFrame):
    """
    เตรียมข้อมูลสำหรับ timeline
    """
    timeline_rows = []
    for _, row in df.iterrows():
        departments = row["Department"].split(";") if row["Department"] != "ไม่ระบุ" else ["ไม่ระบุ"]
        for dept in departments:
            timeline_rows.append({
                "Week": row["Week"],
                "Department": dept.strip(),
                "Task Name": row["Task Name"],
                "Week_Start_Date": row["Week_Start_Date"]
            })
    timeline_df = pd.DataFrame(timeline_rows)
    
    if not timeline_df.empty:
        timeline_summary = timeline_df.groupby(["Week", "Department"]).agg({
            "Task Name": "count",
            "Week_Start_Date": "first"
        }).reset_index()
        timeline_summary = timeline_summary.sort_values("Week_Start_Date")
        
        return timeline_summary
    
    return None

def get_task_statistics(tasks):
    """
    รวบรวมสถิติของ tasks
    """
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.completed)
    pending_tasks = total_tasks - completed_tasks
    total_subtasks = sum(len(task.subtasks) for task in tasks)
    completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "total_subtasks": total_subtasks,
        "completion_rate": completion_rate
    }
