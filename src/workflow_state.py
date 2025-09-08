"""
Workflow State Management for Book Cover Generator
Handles pause/resume functionality and project tracking
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class WorkflowState:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.projects_dir = self.project_root / "projects"
        self.config_dir = self.project_root / "config"
        
    def create_project_slug(self, title: str) -> str:
        """Convert book title to filesystem-safe slug"""
        import re
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        slug = re.sub(r'\s+', '-', slug.strip())
        return slug[:50]  # Limit length
    
    def create_new_project(self, title: str, author: str, genre: str, description: str) -> str:
        """Create new project structure and return project slug"""
        slug = self.create_project_slug(title)
        project_dir = self.projects_dir / slug
        
        # Create project directory structure
        project_dir.mkdir(parents=True, exist_ok=True)
        (project_dir / "covers").mkdir(exist_ok=True)
        
        # Initialize input.json
        input_data = {
            "book_info": {
                "title": title,
                "author": author,
                "genre": genre,
                "description": description
            },
            "metadata": {
                "created_date": datetime.now().isoformat(),
                "project_slug": slug
            }
        }
        
        # Initialize workflow state
        workflow_state = {
            "project_slug": slug,
            "created_date": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "current_step": "input_collection",
            "completed_steps": [],
            "step_status": {
                "input_collection": {"status": "completed", "timestamp": datetime.now().isoformat()},
                "market_research": {"status": "pending"},
                "cover_strategy": {"status": "pending"},
                "prompt_generation": {"status": "pending"},
                "image_generation": {"status": "pending"},
                "output_organization": {"status": "pending"}
            },
            "step_data": {},
            "errors": []
        }
        
        # Save files
        self._save_json(project_dir / "input.json", input_data)
        self._save_json(project_dir / "workflow.json", workflow_state)
        
        return slug
    
    def load_project_state(self, slug: str) -> Optional[Dict]:
        """Load existing project workflow state"""
        project_dir = self.projects_dir / slug
        workflow_file = project_dir / "workflow.json"
        
        if not workflow_file.exists():
            return None
            
        return self._load_json(workflow_file)
    
    def update_step_status(self, slug: str, step_id: str, status: str, data: Optional[Dict] = None):
        """Update status of a specific workflow step"""
        state = self.load_project_state(slug)
        if not state:
            raise ValueError(f"Project {slug} not found")
        
        # Update step status
        state["step_status"][step_id] = {
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
        # Update completed steps list
        if status == "completed" and step_id not in state["completed_steps"]:
            state["completed_steps"].append(step_id)
        
        # Update current step
        if status == "in_progress":
            state["current_step"] = step_id
        elif status == "completed":
            state["current_step"] = self._get_next_step(step_id)
        
        # Save step data if provided
        if data:
            state["step_data"][step_id] = data
        
        # Update last modified
        state["last_modified"] = datetime.now().isoformat()
        
        # Save state
        project_dir = self.projects_dir / slug
        self._save_json(project_dir / "workflow.json", state)
    
    def get_current_step(self, slug: str) -> Optional[str]:
        """Get the current step for a project"""
        state = self.load_project_state(slug)
        return state.get("current_step") if state else None
    
    def is_step_completed(self, slug: str, step_id: str) -> bool:
        """Check if a step is completed"""
        state = self.load_project_state(slug)
        if not state:
            return False
        return state["step_status"].get(step_id, {}).get("status") == "completed"
    
    def list_projects(self) -> List[Dict]:
        """List all projects with their status"""
        projects = []
        if not self.projects_dir.exists():
            return projects
            
        for project_dir in self.projects_dir.iterdir():
            if project_dir.is_dir():
                workflow_file = project_dir / "workflow.json"
                input_file = project_dir / "input.json"
                
                if workflow_file.exists() and input_file.exists():
                    workflow_data = self._load_json(workflow_file)
                    input_data = self._load_json(input_file)
                    
                    projects.append({
                        "slug": project_dir.name,
                        "title": input_data.get("book_info", {}).get("title", "Unknown"),
                        "author": input_data.get("book_info", {}).get("author", "Unknown"),
                        "current_step": workflow_data.get("current_step", "unknown"),
                        "completed_steps": len(workflow_data.get("completed_steps", [])),
                        "last_modified": workflow_data.get("last_modified", "")
                    })
        
        return sorted(projects, key=lambda x: x["last_modified"], reverse=True)
    
    def _get_next_step(self, current_step: str) -> Optional[str]:
        """Get the next step in the workflow"""
        steps = ["input_collection", "market_research", "cover_strategy", 
                "prompt_generation", "image_generation", "output_organization"]
        
        try:
            current_index = steps.index(current_step)
            if current_index < len(steps) - 1:
                return steps[current_index + 1]
        except ValueError:
            pass
        return None
    
    def _save_json(self, filepath: Path, data: Dict):
        """Save data as JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_json(self, filepath: Path) -> Dict:
        """Load JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)