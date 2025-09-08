#!/usr/bin/env python3
"""
Book Cover Generator - Main Workflow Script
AI-assisted book cover generation with market research and Ideogram API
"""

import argparse
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from workflow_state import WorkflowState
from market_research import MarketResearcher
from cover_generator import CoverGenerator
from ideogram_api import IdeogramClient

class BookCoverWorkflow:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.state_manager = WorkflowState(project_root)
        self.market_researcher = MarketResearcher()
        self.cover_generator = CoverGenerator()
        self.ideogram_client = IdeogramClient()
    
    def create_new_project(self, title: str, author: str, genre: str, description: str) -> str:
        """Create a new book cover project"""
        print(f"Creating new project for '{title}' by {author}")
        slug = self.state_manager.create_new_project(title, author, genre, description)
        print(f"✓ Project created: {slug}")
        print(f"  Location: projects/{slug}/")
        return slug
    
    def resume_project(self, slug: str):
        """Resume existing project from current step"""
        state = self.state_manager.load_project_state(slug)
        if not state:
            print(f"❌ Project '{slug}' not found")
            return False
        
        current_step = state.get("current_step")
        print(f"Resuming project: {slug}")
        print(f"Current step: {current_step}")
        
        return self.run_step(slug, current_step)
    
    def run_step(self, slug: str, step_id: str) -> bool:
        """Run a specific workflow step"""
        print(f"\\n🔄 Running step: {step_id}")
        
        try:
            if step_id == "market_research":
                return self._run_market_research(slug)
            elif step_id == "cover_strategy":
                return self._run_cover_strategy(slug)
            elif step_id == "prompt_generation":
                return self._run_prompt_generation(slug)
            elif step_id == "image_generation":
                return self._run_image_generation(slug)
            elif step_id == "output_organization":
                return self._run_output_organization(slug)
            else:
                print(f"❌ Unknown step: {step_id}")
                return False
                
        except Exception as e:
            print(f"❌ Error in step {step_id}: {str(e)}")
            return False
    
    def _run_market_research(self, slug: str) -> bool:
        """Step 2: Market Research"""
        self.state_manager.update_step_status(slug, "market_research", "in_progress")
        
        # Load project input
        project_dir = self.project_root / "projects" / slug
        input_data = self.state_manager._load_json(project_dir / "input.json")
        genre = input_data["book_info"]["genre"]
        
        print(f"🔍 Researching {genre} market trends...")
        research_data = self.market_researcher.research_genre(genre)
        
        # Save research results
        self.state_manager._save_json(project_dir / "research.json", research_data)
        self.state_manager.update_step_status(slug, "market_research", "completed", research_data)
        
        print("✓ Market research completed")
        return True
    
    def _run_cover_strategy(self, slug: str) -> bool:
        """Step 3: Cover Strategy Development"""
        self.state_manager.update_step_status(slug, "cover_strategy", "in_progress")
        
        project_dir = self.project_root / "projects" / slug
        input_data = self.state_manager._load_json(project_dir / "input.json")
        research_data = self.state_manager._load_json(project_dir / "research.json")
        
        print("🎨 Developing cover strategies...")
        strategies = self.cover_generator.develop_strategies(input_data, research_data)
        
        # Save strategies
        self.state_manager._save_json(project_dir / "strategies.json", strategies)
        self.state_manager.update_step_status(slug, "cover_strategy", "completed", strategies)
        
        print(f"✓ Generated {len(strategies.get('concepts', []))} cover concepts")
        return True
    
    def _run_prompt_generation(self, slug: str) -> bool:
        """Step 4: Ideogram Prompt Generation"""
        self.state_manager.update_step_status(slug, "prompt_generation", "in_progress")
        
        project_dir = self.project_root / "projects" / slug
        input_data = self.state_manager._load_json(project_dir / "input.json")
        strategies = self.state_manager._load_json(project_dir / "strategies.json")
        
        print("📝 Creating Ideogram prompts...")
        prompts = self.cover_generator.create_prompts(input_data, strategies)
        
        # Save prompts
        self.state_manager._save_json(project_dir / "prompts.json", prompts)
        self.state_manager.update_step_status(slug, "prompt_generation", "completed", prompts)
        
        print(f"✓ Generated {len(prompts.get('cover_concepts', []))} detailed prompts")
        return True
    
    def _run_image_generation(self, slug: str) -> bool:
        """Step 5: Generate Images with Ideogram API"""
        self.state_manager.update_step_status(slug, "image_generation", "in_progress")
        
        project_dir = self.project_root / "projects" / slug
        prompts_data = self.state_manager._load_json(project_dir / "prompts.json")
        
        print("🖼️  Generating cover images...")
        results = self.ideogram_client.generate_covers(slug, prompts_data, project_dir / "covers")
        
        # Save generation results
        self.state_manager._save_json(project_dir / "generation_results.json", results)
        self.state_manager.update_step_status(slug, "image_generation", "completed", results)
        
        print(f"✓ Generated {len(results.get('images', []))} cover images")
        return True
    
    def _run_output_organization(self, slug: str) -> bool:
        """Step 6: Organize and Document Output"""
        self.state_manager.update_step_status(slug, "output_organization", "in_progress")
        
        project_dir = self.project_root / "projects" / slug
        
        print("📁 Organizing output...")
        
        # Create final report
        report = self._create_final_report(slug)
        self.state_manager._save_json(project_dir / "final_report.json", report)
        
        self.state_manager.update_step_status(slug, "output_organization", "completed", report)
        
        print("✓ Project completed!")
        print(f"📍 Results in: projects/{slug}/")
        return True
    
    def _create_final_report(self, slug: str) -> dict:
        """Create final project report"""
        project_dir = self.project_root / "projects" / slug
        
        # Load all project data
        input_data = self.state_manager._load_json(project_dir / "input.json")
        
        report = {
            "project_summary": {
                "title": input_data["book_info"]["title"],
                "author": input_data["book_info"]["author"],
                "genre": input_data["book_info"]["genre"],
                "completed_date": self.state_manager.load_project_state(slug)["last_modified"]
            },
            "deliverables": {
                "cover_images": list((project_dir / "covers").glob("*.png")),
                "research_file": str(project_dir / "research.json"),
                "strategies_file": str(project_dir / "strategies.json"),
                "prompts_file": str(project_dir / "prompts.json")
            }
        }
        
        return report
    
    def list_projects(self):
        """List all projects"""
        projects = self.state_manager.list_projects()
        
        if not projects:
            print("No projects found.")
            return
        
        print("\\nProjects:")
        print("-" * 80)
        for project in projects:
            status_emoji = "✅" if project["completed_steps"] == 6 else "🔄"
            print(f"{status_emoji} {project['title']} by {project['author']}")
            print(f"   Slug: {project['slug']}")
            print(f"   Progress: {project['completed_steps']}/6 steps")
            print(f"   Current: {project['current_step']}")
            print(f"   Modified: {project['last_modified']}")
            print()

def main():
    parser = argparse.ArgumentParser(description='AI-assisted book cover generator')
    parser.add_argument('--new', nargs=4, metavar=('TITLE', 'AUTHOR', 'GENRE', 'DESCRIPTION'),
                        help='Create new project: --new "Title" "Author" "Genre" "Description"')
    parser.add_argument('--resume', help='Resume project by slug')
    parser.add_argument('--step', nargs=2, metavar=('SLUG', 'STEP'), 
                        help='Run specific step: --step project-slug step-name')
    parser.add_argument('--list', action='store_true', help='List all projects')
    parser.add_argument('--status', help='Show project status')
    
    args = parser.parse_args()
    workflow = BookCoverWorkflow()
    
    if args.new:
        title, author, genre, description = args.new
        slug = workflow.create_new_project(title, author, genre, description)
        print(f"\\nNext: python workflow.py --resume {slug}")
        
    elif args.resume:
        workflow.resume_project(args.resume)
        
    elif args.step:
        slug, step = args.step
        workflow.run_step(slug, step)
        
    elif args.list:
        workflow.list_projects()
        
    elif args.status:
        state = workflow.state_manager.load_project_state(args.status)
        if state:
            print(f"Project: {args.status}")
            print(f"Current step: {state['current_step']}")
            print(f"Completed: {len(state['completed_steps'])}/6 steps")
        else:
            print(f"Project '{args.status}' not found")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()