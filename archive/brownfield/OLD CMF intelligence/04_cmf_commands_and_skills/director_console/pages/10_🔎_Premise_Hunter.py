# Page 10: Premise Hunter V3 - Frame-First Batch System with CLI Trigger

import streamlit as st
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))
from db.connection import get_session, init_db
from db.models import Project, Coach
from config import VIDEO_VALUE, MONTHLY_GOAL, WEEKLY_GOAL, CURRENCY, CMF_ROOT
from utils.cli_executor import (
    trigger_premise_hunter, 
    get_queue_status, 
    execute_command_async,
    clear_completed
)

st.set_page_config(page_title="Premise Hunter", page_icon="🔎", layout="wide")
init_db()

# ============================================================
# SIDEBAR - PROGRESS + COMMAND QUEUE
# ============================================================
with st.sidebar:
    st.markdown("### 💰 Progress Tracker")
    
    with get_session() as session:
        now = datetime.now()
        current_month = now.month
        week_start = now - timedelta(days=now.weekday())
        
        total_completed = session.query(Project).filter(Project.current_stage == "completed").count()
        month_completed = session.query(Project).filter(Project.current_stage == "completed", Project.month == current_month).count()
        week_completed = session.query(Project).filter(Project.current_stage == "completed", Project.updated_at >= week_start).count()
    
    st.markdown(f"**📅 {now.strftime('%B')}**")
    st.progress(min(month_completed / MONTHLY_GOAL, 1.0))
    st.markdown(f"**{month_completed}/{MONTHLY_GOAL}** = {CURRENCY}{month_completed * VIDEO_VALUE:,}")
    
    st.divider()
    
    # Command Queue Status
    st.markdown("### 📋 Command Queue")
    queue = get_queue_status()
    
    if queue:
        for cmd in queue[-5:]:  # Show last 5
            status_icon = {"queued": "⏳", "ready_for_execution": "🟡", "completed": "✅", "failed": "❌"}
            st.caption(f"{status_icon.get(cmd['status'], '❓')} {cmd['phase']} ({cmd['status']})")
        
        if st.button("🧹 Clear Completed"):
            cleared = clear_completed()
            st.success(f"Cleared {cleared} commands")
    else:
        st.caption("No pending commands")

# ============================================================
# SESSION STATE
# ============================================================
if "batch_projects" not in st.session_state:
    st.session_state.batch_projects = []
if "batch_phase" not in st.session_state:
    st.session_state.batch_phase = "upload"
if "cli_tool" not in st.session_state:
    st.session_state.cli_tool = "claude"

# ============================================================
# MAIN HEADER
# ============================================================
st.title("🔎 Premise Hunter V3")
st.markdown("**Frame-First Batch System** — Define frames, trigger AI via CLI")

# CLI Tool selector
col1, col2 = st.columns([3, 1])
with col2:
    st.session_state.cli_tool = st.selectbox("CLI Tool", ["claude", "gemini"], label_visibility="collapsed")

# Phase indicator
phase_map = {
    "upload": "📁 Upload",
    "frame": "🎯 Frames (YOU)",
    "generate": "⚡ CLI Trigger",
    "review": "✅ Review"
}

cols = st.columns(4)
for i, (phase_key, phase_name) in enumerate(phase_map.items()):
    with cols[i]:
        if st.session_state.batch_phase == phase_key:
            st.success(f"**{phase_name}**")
        else:
            st.caption(phase_name)

st.divider()

# ============================================================
# PHASE 1: UPLOAD SOURCES
# ============================================================
if st.session_state.batch_phase == "upload":
    st.header("📁 Phase 1: Upload Sources")
    
    # Batch upload
    uploaded_files = st.file_uploader(
        "Upload Transcript Files",
        type=["txt", "md", "json"],
        accept_multiple_files=True
    )
    
    # Manual add
    with st.expander("➕ Add Single Project"):
        with st.form("add_project"):
            project_name = st.text_input("Project Name")
            coach_name = st.text_input("Coach Name")
            transcript = st.text_area("Paste Transcript", height=150)
            
            if st.form_submit_button("Add"):
                if project_name and transcript:
                    st.session_state.batch_projects.append({
                        "id": len(st.session_state.batch_projects) + 1,
                        "name": project_name,
                        "coach": coach_name,
                        "transcript": transcript,
                        "frame": None,
                        "script": None,
                        "status": "pending_frame"
                    })
                    st.rerun()
    
    # Process uploads
    if uploaded_files:
        for file in uploaded_files:
            content = file.read().decode('utf-8')
            name = file.name.replace(".md", "").replace(".txt", "")
            
            if not any(p["name"] == name for p in st.session_state.batch_projects):
                st.session_state.batch_projects.append({
                    "id": len(st.session_state.batch_projects) + 1,
                    "name": name,
                    "coach": "Unknown",
                    "transcript": content,
                    "frame": None,
                    "script": None,
                    "status": "pending_frame"
                })
        st.rerun()
    
    # Show batch
    if st.session_state.batch_projects:
        st.subheader(f"📋 Batch: {len(st.session_state.batch_projects)} projects")
        
        for proj in st.session_state.batch_projects:
            st.markdown(f"- {proj['name']} ({proj['status']})")
        
        if st.button("→ Define Frames", type="primary"):
            st.session_state.batch_phase = "frame"
            st.rerun()

# ============================================================
# PHASE 2: DEFINE FRAMES (Human Input)
# ============================================================
elif st.session_state.batch_phase == "frame":
    st.header("🎯 Phase 2: Define Frames")
    st.info("👤 **YOUR INPUT** — 2-3 min per project")
    
    completed = len([p for p in st.session_state.batch_projects if p["frame"]])
    st.progress(completed / len(st.session_state.batch_projects))
    st.caption(f"{completed}/{len(st.session_state.batch_projects)} frames defined")
    
    for proj in st.session_state.batch_projects:
        with st.expander(f"{'✅' if proj['frame'] else '⬜'} {proj['name']}"):
            st.text_area("Transcript", proj["transcript"][:500] + "...", height=100, disabled=True, key=f"t_{proj['id']}")
            
            with st.form(f"frame_{proj['id']}"):
                col1, col2 = st.columns(2)
                with col1:
                    topic = st.text_input("Topic", key=f"topic_{proj['id']}")
                    mechanism = st.text_input("Mechanism", key=f"mech_{proj['id']}")
                with col2:
                    outcome = st.text_input("Outcome", key=f"out_{proj['id']}")
                    coach_angle = st.text_input("Coach Angle", key=f"coach_{proj['id']}")
                
                frame_statement = st.text_area("Frame Statement", height=60, key=f"fs_{proj['id']}")
                
                if st.form_submit_button("💾 Save"):
                    proj["frame"] = {
                        "topic": topic, "mechanism": mechanism,
                        "outcome": outcome, "coach_angle": coach_angle,
                        "statement": frame_statement
                    }
                    proj["status"] = "ready"
                    st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.batch_phase = "upload"
            st.rerun()
    with col2:
        ready = len([p for p in st.session_state.batch_projects if p["status"] == "ready"])
        if st.button(f"→ Trigger CLI ({ready} ready)", type="primary", disabled=ready == 0):
            st.session_state.batch_phase = "generate"
            st.rerun()

# ============================================================
# PHASE 3-5: CLI TRIGGER (Automated)
# ============================================================
elif st.session_state.batch_phase == "generate":
    st.header("⚡ Phase 3-5: CLI Trigger")
    st.info(f"🤖 **Trigger {st.session_state.cli_tool.upper()} CLI** for script generation")
    
    ready_projects = [p for p in st.session_state.batch_projects if p["status"] == "ready"]
    
    st.subheader(f"Ready: {len(ready_projects)} projects")
    
    for proj in ready_projects:
        st.markdown(f"- **{proj['name']}**: {proj['frame'].get('statement', '')[:60]}...")
    
    st.divider()
    
    # Trigger button
    if st.button("🚀 Queue for CLI Execution", type="primary"):
        # Prepare batch data
        batch_data = []
        for proj in ready_projects:
            batch_data.append({
                "name": proj["name"],
                "coach": proj["coach"],
                "transcript": proj["transcript"],
                "frame": proj["frame"]
            })
        
        # Queue command
        command_id = trigger_premise_hunter(batch_data, st.session_state.cli_tool)
        
        st.success(f"✅ Command queued: `{command_id}`")
        
        # Generate execution instructions
        result = execute_command_async(command_id, st.session_state.cli_tool)
        
        st.code(result, language="bash")
        
        st.info("""
        **Next Steps:**
        1. Copy the prompt file path above
        2. In your terminal, run the CLI command
        3. Or ask me directly: "Execute premise_hunter command {command_id}"
        4. Scripts will be generated and saved
        5. Return here to review
        """)
        
        # Mark projects as pending
        for proj in ready_projects:
            proj["status"] = "pending_generation"
    
    # Check for generated scripts
    st.divider()
    
    if st.button("🔄 Check for Generated Scripts"):
        # Look for generated script files
        output_dir = Path(__file__).parent.parent / "outputs"
        if output_dir.exists():
            script_files = list(output_dir.glob("**/script*.json"))
            if script_files:
                st.success(f"Found {len(script_files)} generated scripts!")
                for sf in script_files:
                    st.caption(str(sf))
                
                # Load and attach to projects
                # (Implementation would match files to projects)
                
                for proj in st.session_state.batch_projects:
                    if proj["status"] == "pending_generation":
                        proj["status"] = "pending_review"
                        proj["script"] = {"placeholder": True}  # Would load actual script
            else:
                st.warning("No scripts found yet.")
        else:
            st.warning("Output directory not found.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Frames"):
            st.session_state.batch_phase = "frame"
            st.rerun()
    with col2:
        has_scripts = any(p.get("script") for p in st.session_state.batch_projects)
        if st.button("→ Review Scripts", type="primary", disabled=not has_scripts):
            st.session_state.batch_phase = "review"
            st.rerun()

# ============================================================
# PHASE 6: REVIEW & APPROVE
# ============================================================
elif st.session_state.batch_phase == "review":
    st.header("✅ Phase 6: Review & Approve")
    st.info("👤 **YOUR INPUT** — 1-2 min per project")
    
    for proj in st.session_state.batch_projects:
        status_icon = {"pending_review": "⏳", "approved": "✅", "rejected": "❌"}
        
        with st.expander(f"{status_icon.get(proj['status'], '❓')} {proj['name']}"):
            st.markdown(f"**Frame:** {proj['frame'].get('statement', 'N/A')}")
            
            if proj.get("script"):
                st.json(proj["script"])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve", key=f"app_{proj['id']}"):
                    proj["status"] = "approved"
                    st.rerun()
            with col2:
                if st.button("🔄 Revise", key=f"rev_{proj['id']}"):
                    proj["status"] = "pending_frame"
                    proj["frame"] = None
                    st.session_state.batch_phase = "frame"
                    st.rerun()
    
    st.divider()
    
    # Export
    approved = [p for p in st.session_state.batch_projects if p["status"] == "approved"]
    
    if approved:
        if st.button(f"📤 Export {len(approved)} Scripts", type="primary"):
            export = {"projects": [{"name": p["name"], "frame": p["frame"], "script": p["script"]} for p in approved]}
            st.download_button("⬇️ Download", json.dumps(export, indent=2), "approved_scripts.json")
    
    if st.button("🔄 New Batch"):
        st.session_state.batch_projects = []
        st.session_state.batch_phase = "upload"
        st.rerun()
