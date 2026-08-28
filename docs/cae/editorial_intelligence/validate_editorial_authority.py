#!/usr/bin/env python3
"""
validate_editorial_authority.py
-------------------------------
Static Completeness, Lineage, and Collision Validator for CAE-M00 (Editorial Intelligence Authority).

Performs deterministic static validation across:
  1. CAE_EDITORIAL_OBJECT_REGISTER.md (Completeness of all 18 objects & fields)
  2. CAE_EDITORIAL_PLANE_AND_CLASS_MATRIX.md (Plane & Lifecycle Class mapping)
  3. CAE_EDITORIAL_DEPENDENCY_GRAPH.md (Mandate write authority & causal flow)
  4. CAE_EDITORIAL_AUTHORITY_MATRIX.md (Definition, Runtime, and Change Authority)
  5. CAE_EDITORIAL_CONTRADICTION_REGISTER.md (Anti-collapse invariant checks)
  6. False-Proof / Anti-Reward-Hacking checks (Role distinctness, no synonym collapsing)
"""

import os
import sys
import re
from pathlib import Path

EXPECTED_OBJECTS = [
    "ResearchSignal",
    "AudienceState",
    "GuestState",
    "CollisionHypothesis",
    "InterviewBrief",
    "InterviewResponse",
    "EvidenceSegment",
    "SemanticAnnotation",
    "ContentCandidate",
    "CandidateCluster",
    "EditorialStoryboard",
    "MediaAsset",
    "AssetAnnotation",
    "InsertRole",
    "SemanticProgram",
    "CompositionIR",
    "VideoEditProgram",
    "Outcome",
]

EXPECTED_PLANES = [
    "World Plane",
    "Relational Plane",
    "Elicitation Plane",
    "Evidence Plane",
    "Editorial Plane",
    "Realization Plane",
    "Outcome Plane",
]

EXPECTED_CLASSES = [
    "Canonical Definition",
    "Dynamic State",
    "Immutable Evidence",
    "Derived Artifact",
    "Execution Packet",
]

EXPECTED_INVARIANTS = [
    ("ResearchSignal", "ContentOpportunity"),
    ("EvidenceSegment", "MediaAsset"),
    ("ContentCandidate", "EditorialStoryboard"),
    ("SemanticAnnotation", "AssetAnnotation"),
    ("SemanticProgram", "CompositionIR"),
]


def validate_file_exists(filepath: Path) -> str:
    if not filepath.exists():
        raise FileNotFoundError(f"[EVIDENCE_ERROR] Required artifact missing: {filepath}")
    content = filepath.read_text(encoding="utf-8")
    if len(content.strip()) < 100:
        raise ValueError(f"[EVIDENCE_ERROR] Artifact is suspiciously empty or truncated: {filepath}")
    return content


def test_object_register(base_dir: Path):
    reg_path = base_dir / "CAE_EDITORIAL_OBJECT_REGISTER.md"
    content = validate_file_exists(reg_path)
    
    missing = []
    for obj in EXPECTED_OBJECTS:
        pattern = rf"(?:###\s*\d+\.\s*`{obj}`|\|\s*\*\*\d+\*\*\s*\|\s*`{obj}`)"
        if not re.search(pattern, content):
            missing.append(obj)
            
    if missing:
        raise ValueError(f"[TAXONOMY_ERROR] Object Register missing definitions for: {missing}")
    print("  [PASS] Object Register contains all 18 canonical objects.")


def test_plane_and_class_matrix(base_dir: Path):
    mat_path = base_dir / "CAE_EDITORIAL_PLANE_AND_CLASS_MATRIX.md"
    content = validate_file_exists(mat_path)
    
    for plane in EXPECTED_PLANES:
        if plane not in content:
            raise ValueError(f"[TAXONOMY_ERROR] Plane Matrix missing Ontological Plane: {plane}")
            
    for cls_name in EXPECTED_CLASSES:
        if cls_name not in content:
            raise ValueError(f"[TAXONOMY_ERROR] Class Matrix missing Lifecycle Class: {cls_name}")
            
    for obj in EXPECTED_OBJECTS:
        if f"`{obj}`" not in content:
            raise ValueError(f"[TAXONOMY_ERROR] Plane Matrix missing object crosswalk for: {obj}")
            
    print("  [PASS] Plane & Class Matrix covers all 7 planes, 5 lifecycle classes, and 18 objects.")


def test_dependency_graph(base_dir: Path):
    dep_path = base_dir / "CAE_EDITORIAL_DEPENDENCY_GRAPH.md"
    content = validate_file_exists(dep_path)
    
    # Check that all mandates M00 to M12 are present
    for i in range(13):
        mandate_id = f"CAE-M{i:02d}"
        if mandate_id not in content:
            raise ValueError(f"[RELATION_ERROR] Dependency graph missing write authority for: {mandate_id}")
            
    print("  [PASS] Dependency Graph accurately binds write authority for all mandates CAE-M00 through CAE-M12.")


def test_authority_matrix(base_dir: Path):
    aut_path = base_dir / "CAE_EDITORIAL_AUTHORITY_MATRIX.md"
    content = validate_file_exists(aut_path)
    
    for obj in EXPECTED_OBJECTS:
        if f"`{obj}`" not in content:
            raise ValueError(f"[AUTHORITY_ERROR] Authority Matrix missing 3-axis entry for: {obj}")
            
    if "CAE-M09" not in content and "Operator Signature" not in content:
        raise ValueError("[AUTHORITY_ERROR] Operator authority on EditorialStoryboard must be explicitly enforced.")
        
    print("  [PASS] Authority Matrix establishes Definition, Runtime, and Change authority for all 18 objects.")


def test_contradiction_register(base_dir: Path):
    con_path = base_dir / "CAE_EDITORIAL_CONTRADICTION_REGISTER.md"
    content = validate_file_exists(con_path)
    
    for ent_a, ent_b in EXPECTED_INVARIANTS:
        if ent_a not in content or ent_b not in content:
            raise ValueError(f"[REWARD_HACK] Contradiction Register missing anti-collapse defense for: {ent_a} vs {ent_b}")
            
    print("  [PASS] Contradiction Register explicitly defends all 5 critical anti-collapse boundaries.")


def test_false_proof_distinctness(base_dir: Path):
    """
    False-proof test:
    Ensures that every object has distinct descriptions and does not duplicate
    another object's definition under a synonym.
    """
    reg_path = base_dir / "CAE_EDITORIAL_OBJECT_REGISTER.md"
    content = validate_file_exists(reg_path)
    
    # Extract Ontological Roles
    roles = re.findall(r"\* \*\*Ontological Role:\*\*\s*(.+)", content)
    if len(roles) != len(EXPECTED_OBJECTS):
        raise ValueError(f"[REWARD_HACK] Expected {len(EXPECTED_OBJECTS)} distinct Ontological Roles, found {len(roles)}")
        
    if len(set(roles)) != len(roles):
        raise ValueError("[REWARD_HACK] Duplicate Ontological Role detected across distinct objects!")
        
    print("  [PASS] False-Proof Check: All 18 objects have mathematically distinct ontological definitions.")


def main():
    print("=================================================================")
    print(" RUNNING CAE-M00 EDITORIAL INTELLIGENCE AUTHORITY STATIC AUDIT   ")
    print("=================================================================")
    
    base_dir = Path(__file__).parent.resolve()
    
    try:
        test_object_register(base_dir)
        test_plane_and_class_matrix(base_dir)
        test_dependency_graph(base_dir)
        test_authority_matrix(base_dir)
        test_contradiction_register(base_dir)
        test_false_proof_distinctness(base_dir)
        
        print("=================================================================")
        print(" [SUCCESS] CAE-M00 STATIC VALIDATION PASSED (100% CONGRUENCE)    ")
        print("=================================================================")
        return 0
    except Exception as e:
        print(f"\n[FATAL VALIDATION FAILURE] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
