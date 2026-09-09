# Page 2: Scripts Approval with Full Preview & Revision Comments

import streamlit as st
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))
from db.connection import get_session, init_db
from db.models import Project, StageApproval, Coach
from config import VIDEO_VALUE, MONTHLY_GOAL, WEEKLY_GOAL, CURRENCY, FILE_PATTERNS

st.set_page_config(page_title="Scripts", page_icon="📝", layout="wide")
init_db()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 💰 Progress Tracker")
    with get_session() as session:
        now = datetime.now()
        total_completed = session.query(Project).filter(Project.current_stage == "completed").count()
        month_completed = session.query(Project).filter(Project.current_stage == "completed", Project.month == now.month).count()
    
    st.progress(min(month_completed / MONTHLY_GOAL, 1.0))
    st.markdown(f"**{month_completed}/{MONTHLY_GOAL}** = {CURRENCY}{month_completed * VIDEO_VALUE:,}")

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def find_script_file(folder_path: str) -> Path | None:
    """Find the final_script.json file in a project folder."""
    folder = Path(folder_path)
    if not folder.exists():
        return None
    
    for pattern in FILE_PATTERNS.get("script", ["*final_script*.json"]):
        matches = list(folder.glob(pattern))
        if matches:
            return matches[0]
    return None


def load_script(script_path: Path) -> dict | None:
    """Load and parse the script JSON file."""
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading script: {e}")
        return None


def render_script_preview(script: dict, script_path: Path):
    """Render a formatted preview of the script."""
    
    # Script metadata
    col1, col2 = st.columns(2)
    with col1:
        arc_type = script.get("arc_type", "Unknown")
        client = script.get("client", "Unknown")
        st.markdown(f"**Arc Type:** {arc_type}")
        st.markdown(f"**Client:** {client}")
    with col2:
        coach = script.get("coach", "Unknown")
        duration = script.get("total_duration_seconds", 60)
        st.markdown(f"**Coach:** {coach}")
        st.markdown(f"**Duration:** {duration}s")
    
    # Frame
    frame = script.get("frame", "")
    if frame:
        st.info(f"**Frame:** {frame}")
    
    st.divider()
    
    # Scene sequence
    scenes = script.get("script_sequence", [])
    if scenes:
        st.markdown("### 🎬 Scene Sequence")
        
        for scene in scenes:
            cluster = scene.get("cluster", f"Scene {scene.get('position', '?')}")
            timestamp = scene.get("timestamp", "")
            quote = scene.get("quote", {})
            quote_text = quote.get("text", "") if isinstance(quote, dict) else ""
            viral_score = quote.get("viral_score", 0) if isinstance(quote, dict) else 0
            visual = scene.get("visual_direction", "")
            
            with st.container():
                # Scene header
                scene_col1, scene_col2, scene_col3 = st.columns([2, 1, 1])
                with scene_col1:
                    cluster_icon = {
                        "W1_HOOK": "🎣",
                        "W2_PROBLEM": "😰",
                        "W3_MECHANISM": "⚙️",
                        "W4_PROOF": "📊",
                        "W5_CLOSE": "🎯"
                    }.get(cluster, "📍")
                    st.markdown(f"**{cluster_icon} {cluster}**")
                with scene_col2:
                    st.markdown(f"⏱️ {timestamp}")
                with scene_col3:
                    if viral_score:
                        st.markdown(f"🔥 Score: {viral_score:.1f}")
                
                # Quote
                if quote_text:
                    st.markdown(f"> *\"{quote_text}\"*")
                
                # Visual direction
                if visual:
                    st.caption(f"📹 {visual}")
                
                st.markdown("---")
    
    # Validation
    validation = script.get("validation", {})
    if validation:
        st.markdown("### ✅ Validation Checklist")
        checks = [
            ("Client Protagonist", validation.get("client_protagonist", False)),
            ("Coach in Hook", validation.get("coach_in_hook", False)),
            ("Coach in Close", validation.get("coach_in_close", False)),
            ("Problem Specific", validation.get("problem_specific", False)),
            ("Mechanism Clear", validation.get("mechanism_clear", False)),
            ("Proof with Numbers", validation.get("proof_with_numbers", False)),
            ("Authentic Voice", validation.get("authentic_voice", False)),
            ("Duration Check", validation.get("duration_check", False)),
        ]
        
        cols = st.columns(4)
        for i, (label, passed) in enumerate(checks):
            with cols[i % 4]:
                icon = "✅" if passed else "❌"
                st.markdown(f"{icon} {label}")
        
        quality = validation.get("quality_score", 0)
        st.metric("Quality Score", f"{quality}/100")

# ============================================================
# MAIN
# ============================================================
st.title("📝 Scripts Approval")

# Get projects at scripts stage
with get_session() as session:
    projects = session.query(Project).filter(Project.current_stage == "scripts").all()
    project_data = []
    for p in projects:
        coach = session.query(Coach).filter(Coach.id == p.coach_id).first()
        project_data.append({
            "id": p.id,
            "code": p.full_code or p.project_id,
            "name": p.name,
            "coach": coach.name if coach else "Unknown",
            "folder_path": p.folder_path
        })

if not project_data:
    st.info("No projects pending script approval.")
    st.markdown("Go to **📥 Auto Import** to discover and import existing projects.")
else:
    st.subheader(f"📋 Pending: {len(project_data)} scripts")
    
    # Batch actions
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("✅ Approve All", type="primary"):
            with get_session() as session:
                for proj in project_data:
                    p = session.query(Project).get(proj["id"])
                    if p:
                        p.current_stage = "assets"
            st.success("All approved! → Assets stage")
            st.rerun()
    
    st.divider()
    
    # Individual projects
    for proj in project_data:
        with st.expander(f"📄 {proj['code']} - {proj['name']} ({proj['coach']})", expanded=True):
            
            # Find and load script
            script_path = find_script_file(proj["folder_path"])
            
            if script_path and script_path.exists():
                script = load_script(script_path)
                
                if script:
                    # Render script preview
                    render_script_preview(script, script_path)
                    
                    st.divider()
                    
                    # Revision notes
                    st.markdown("### 📝 Revision Notes")
                    revision_key = f"revision_{proj['id']}"
                    revision_notes = st.text_area(
                        "Add comments for regeneration:",
                        key=revision_key,
                        placeholder="e.g., 'Change hook to use the mountain story instead', 'Need more specific numbers in proof section'..."
                    )
                    
                    # Action buttons
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
                    with col1:
                        if st.button("✅ Approve", key=f"app_{proj['id']}", type="primary"):
                            with get_session() as session:
                                p = session.query(Project).get(proj["id"])
                                if p:
                                    p.current_stage = "assets"
                            st.success("Approved! → Assets")
                            st.rerun()
                    
                    with col2:
                        if st.button("🔄 Request Revision", key=f"rev_{proj['id']}"):
                            # Save revision notes to a file
                            notes_path = Path(proj["folder_path"]) / "revision_notes.md"
                            with open(notes_path, 'w', encoding='utf-8') as f:
                                f.write(f"# Revision Notes for {proj['code']}\n\n")
                                f.write(f"**Date:** {datetime.now().isoformat()}\n\n")
                                f.write(f"## Comments:\n\n{revision_notes}\n")
                            
                            # Mark for regeneration
                            st.session_state[f"regenerate_{proj['id']}"] = True
                            st.rerun()
                    
                    # Check if regeneration is requested
                    if st.session_state.get(f"regenerate_{proj['id']}", False):
                        st.divider()
                        st.markdown("### 🔄 Regenerate Script")
                        st.success(f"✅ Revision notes saved to `revision_notes.md`")
                        
                        # Arc selection
                        arc_options = {
                            "The Witness (Testimonial)": "witness_hunter",
                            "Core Transformation": "core_transformation_hunter",
                            "Breakthrough": "breakthrough_hunter",
                            "Quiet Reflection": "quiet_reflection_hunter",
                            "Confrontation": "confrontation_hunter",
                            "Divine Spark": "divine_spark_hunter",
                            "Call to Adventure": "call_to_adventure_hunter",
                            "Rally": "rally_hunter",
                            "Ticking Clock": "ticking_clock_hunter",
                            "Sacred Return": "sacred_return_hunter",
                            "Shared Struggle": "shared_struggle_hunter",
                            "Warning": "warning_hunter",
                        }
                        
                        selected_arc = st.selectbox(
                            "Select Arc Type",
                            list(arc_options.keys()),
                            key=f"arc_{proj['id']}"
                        )
                        
                        # Generate prompt
                        if st.button("📝 Generate Arc Hunter Prompt", key=f"gen_prompt_{proj['id']}", type="primary"):
                            # Load transcript
                            transcript_path = None
                            folder = Path(proj["folder_path"])
                            for f in folder.glob("*TRANSCRIPT*.md"):
                                transcript_path = f
                                break
                            if not transcript_path:
                                for f in folder.glob("*.md"):
                                    if "transcript" in f.name.lower():
                                        transcript_path = f
                                        break
                            
                            if transcript_path:
                                transcript_content = transcript_path.read_text(encoding='utf-8')[:5000]  # Truncate for prompt
                                
                                # Build the prompt
                                prompt = f"""# Arc Hunter Task: {selected_arc}

## Project: {proj['code']} - {proj['name']}
## Coach: {proj['coach']}

## Revision Notes:
{revision_notes}

## Instructions:
1. Use THE WITNESS HUNTER arc structure (W1-W5)
2. Extract quotes per cluster from the transcript
3. Ensure coach is mentioned in W1_HOOK and W5_CLOSE
4. W4_PROOF must contain specific numbers/metrics
5. Output as final_script.json in Witness Hunter format

## Transcript (truncated):

{transcript_content}

## Output Format:
Generate a JSON file matching the Witness Hunter format with:
- arc_type, agent, client, coach, frame
- script_sequence with W1_HOOK through W5_CLOSE
- validation checklist
- key_metrics
"""
                                
                                # Show the prompt
                                st.text_area(
                                    "📋 Copy this prompt to Claude/Gemini:",
                                    prompt,
                                    height=400,
                                    key=f"prompt_output_{proj['id']}"
                                )
                                
                                # Save prompt
                                prompt_path = folder / "regeneration_prompt.md"
                                prompt_path.write_text(prompt, encoding='utf-8')
                                st.info(f"💾 Prompt saved to `{prompt_path.name}`")
                                
                                # Option to clear regeneration state
                                if st.button("✅ Done - Hide Regeneration", key=f"done_regen_{proj['id']}"):
                                    del st.session_state[f"regenerate_{proj['id']}"]
                                    st.rerun()
                            else:
                                st.error("Could not find transcript file in project folder.")
                    
                    with col3:
                        # Show file path for reference
                        st.caption(f"📁 `{script_path.name}`")
                else:
                    st.error("Could not parse script file.")
            else:
                st.warning(f"No script file found in: `{proj['folder_path']}`")
                st.markdown("Use the **🔎 Premise Hunter** page to generate a script first.")
                
                # Quick action to go to premise hunter
                if st.button("Go to Premise Hunter", key=f"hunt_{proj['id']}"):
                    st.switch_page("pages/10_🔎_Premise_Hunter.py")
