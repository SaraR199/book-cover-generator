#!/usr/bin/env python3
"""
Test script to verify the web app can start without errors
"""

import sys
from pathlib import Path

print("=" * 60)
print("Book Cover Generator - Web App Test")
print("=" * 60)
print()

# Test 1: Check imports
print("Test 1: Checking imports...")
try:
    from src.workflow_state import WorkflowState
    from src.market_research import MarketResearcher
    from src.cover_generator import CoverGenerator
    from src.ideogram_api import IdeogramClient
    print("✓ All workflow modules imported successfully")
except Exception as e:
    print(f"✗ Failed to import workflow modules: {e}")
    sys.exit(1)

try:
    from flask import Flask
    from flask_cors import CORS
    print("✓ Flask and Flask-CORS imported successfully")
except Exception as e:
    print(f"✗ Failed to import Flask: {e}")
    sys.exit(1)

print()

# Test 2: Check Flask app creation
print("Test 2: Creating Flask app...")
try:
    import app as webapp
    print("✓ Flask app module loaded successfully")
    print(f"✓ Projects directory: {webapp.PROJECTS_DIR}")
    print(f"✓ Base directory: {webapp.BASE_DIR}")
except Exception as e:
    print(f"✗ Failed to load Flask app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 3: Check directories
print("Test 3: Checking directories...")
projects_dir = Path("projects")
templates_dir = Path("templates")

projects_dir.mkdir(exist_ok=True)
templates_dir.mkdir(exist_ok=True)

print(f"✓ Projects directory: {projects_dir.absolute()}")
print(f"✓ Templates directory: {templates_dir.absolute()}")
print(f"✓ Template file exists: {(templates_dir / 'index.html').exists()}")

print()

# Test 4: Test API routes
print("Test 4: Checking Flask routes...")
try:
    with webapp.app.app_context():
        rules = list(webapp.app.url_map.iter_rules())
        print(f"✓ Found {len(rules)} routes:")
        for rule in sorted(rules, key=lambda r: str(r)):
            if not str(rule).startswith('/static'):
                print(f"  - {rule}")
except Exception as e:
    print(f"✗ Failed to check routes: {e}")
    sys.exit(1)

print()

# Test 5: Check WorkflowState functionality
print("Test 5: Testing WorkflowState...")
try:
    state = WorkflowState(str(projects_dir))
    print("✓ WorkflowState initialized")
    projects = state.list_projects()
    print(f"✓ Found {len(projects)} existing project(s)")
except Exception as e:
    print(f"✗ WorkflowState test failed: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("✓ All tests passed!")
print("=" * 60)
print()
print("Ready to start the web app!")
print("Run: python3 app.py")
print("Or: ./start_webapp.sh")
print()
