#!/usr/bin/env python3
"""
Book Cover Generator - Main Workflow Script
AI-assisted book cover generation with market research and Ideogram API
"""

import argparse
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

# Load environment variables from .env file
def load_env():
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, _, value = line.partition('=')
                    if key and value:
                        os.environ[key] = value

load_env()

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
        print(f"Project created: {slug}")
        print(f"  Location: projects/{slug}/")
        return slug
    
    def create_interactive_project(self) -> str:
        """Create a new project using interactive input"""
        print("=== Interactive Book Cover Project Creation ===\n")
        
        # Get title
        title = input("Book Title: ").strip()
        if not title:
            print("Error: Title is required")
            return None
        
        # Get author
        author = input("Author Name: ").strip()
        if not author:
            print("Error: Author name is required")
            return None
        
        # Get genre with suggestions
        print("\nCommon genres: romance, thriller, fantasy, mystery, sci-fi, literary fiction, horror")
        genre = input("Genre: ").strip()
        if not genre:
            print("Error: Genre is required")
            return None
        
        # Get description with multi-line support
        print("\nBook Description/Blurb:")
        print("(You can paste your full book blurb here. Press Enter twice when finished)\n")
        
        description_lines = []
        empty_lines = 0
        
        while True:
            try:
                line = input()
                if line.strip() == "":
                    empty_lines += 1
                    if empty_lines >= 2:
                        break
                    description_lines.append(line)
                else:
                    empty_lines = 0
                    description_lines.append(line)
            except EOFError:
                break
        
        description = "\n".join(description_lines).strip()
        
        if not description:
            print("Error: Description is required")
            return None
        
        # Show summary and confirm
        print("\n" + "="*50)
        print("PROJECT SUMMARY")
        print("="*50)
        print(f"Title: {title}")
        print(f"Author: {author}")
        print(f"Genre: {genre}")
        print(f"Description: {description[:100]}{'...' if len(description) > 100 else ''}")
        print("="*50)
        
        confirm = input("\nCreate this project? [y/N]: ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Project creation cancelled")
            return None
        
        return self.create_new_project(title, author, genre, description)
    
    def resume_project(self, slug: str):
        """Resume existing project from current step"""
        state = self.state_manager.load_project_state(slug)
        if not state:
            print(f"Project '{slug}' not found")
            return False
        
        current_step = state.get("current_step")
        print(f"Resuming project: {slug}")
        print(f"Current step: {current_step}")
        
        return self.run_step(slug, current_step)
    
    def run_step(self, slug: str, step_id: str) -> bool:
        """Run a specific workflow step"""
        print(f"\\nRunning step: {step_id}")
        
        try:
            if step_id == "input_collection":
                # Input collection is already done, move to next step
                print("Input collection already completed, moving to market research")
                return self._run_market_research(slug)
            elif step_id == "market_research":
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
                print(f"Unknown step: {step_id}")
                return False
                
        except Exception as e:
            print(f"Error in step {step_id}: {str(e)}")
            return False
    
    def _run_market_research(self, slug: str) -> bool:
        """Step 2: Market Research"""
        self.state_manager.update_step_status(slug, "market_research", "in_progress")
        
        # Load project input
        project_dir = self.project_root / "projects" / slug
        input_data = self.state_manager._load_json(project_dir / "input.json")
        genre = input_data["book_info"]["genre"]
        
        print(f"Researching {genre} market trends...")
        research_data = self.market_researcher.research_genre(genre)
        
        # Save research results
        self.state_manager._save_json(project_dir / "research.json", research_data)
        self.state_manager.update_step_status(slug, "market_research", "completed", research_data)
        
        print("Market research completed")
        return True
    
    def _run_cover_strategy(self, slug: str) -> bool:
        """Step 3: Cover Strategy Development"""
        self.state_manager.update_step_status(slug, "cover_strategy", "in_progress")
        
        project_dir = self.project_root / "projects" / slug
        input_data = self.state_manager._load_json(project_dir / "input.json")
        research_data = self.state_manager._load_json(project_dir / "research.json")
        
        print("Developing cover strategies...")
        strategies = self.cover_generator.develop_strategies(input_data, research_data)
        
        # Save strategies
        self.state_manager._save_json(project_dir / "strategies.json", strategies)
        self.state_manager.update_step_status(slug, "cover_strategy", "completed", strategies)
        
        print(f"Generated {len(strategies.get('concepts', []))} cover concepts")
        return True
    
    def _run_prompt_generation(self, slug: str) -> bool:
        """Step 4: Ideogram Prompt Generation"""
        self.state_manager.update_step_status(slug, "prompt_generation", "in_progress")
        
        project_dir = self.project_root / "projects" / slug
        input_data = self.state_manager._load_json(project_dir / "input.json")
        strategies = self.state_manager._load_json(project_dir / "strategies.json")
        
        print("Creating Ideogram prompts...")
        prompts = self.cover_generator.create_prompts(input_data, strategies)
        
        # Save prompts
        self.state_manager._save_json(project_dir / "prompts.json", prompts)
        self.state_manager.update_step_status(slug, "prompt_generation", "completed", prompts)
        
        print(f"Generated {len(prompts.get('cover_concepts', []))} detailed prompts")
        return True
    
    def _run_image_generation(self, slug: str) -> bool:
        """Step 5: Generate Images with Ideogram API"""
        self.state_manager.update_step_status(slug, "image_generation", "in_progress")
        
        project_dir = self.project_root / "projects" / slug
        prompts_data = self.state_manager._load_json(project_dir / "prompts.json")
        
        print("Generating cover images...")
        results = self.ideogram_client.generate_covers(slug, prompts_data, project_dir / "covers")
        
        # Save generation results
        self.state_manager._save_json(project_dir / "generation_results.json", results)
        self.state_manager.update_step_status(slug, "image_generation", "completed", results)
        
        print(f"Generated {len(results.get('images', []))} cover images")
        return True
    
    def _run_output_organization(self, slug: str) -> bool:
        """Step 6: Organize and Document Output"""
        self.state_manager.update_step_status(slug, "output_organization", "in_progress")
        
        project_dir = self.project_root / "projects" / slug
        
        print("Organizing output...")
        
        # Create final report
        report = self._create_final_report(slug)
        self.state_manager._save_json(project_dir / "final_report.json", report)
        
        self.state_manager.update_step_status(slug, "output_organization", "completed", report)
        
        print("Project completed!")
        print(f"Results in: projects/{slug}/")
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
                "cover_images": [str(f) for f in (project_dir / "covers").glob("*")],
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
            status_emoji = "[DONE]" if project["completed_steps"] == 6 else "[WIP]"
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
    parser.add_argument('--interactive', action='store_true',
                        help='Create new project using interactive prompts (recommended for long descriptions)')
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
        if slug:
            print(f"\\nNext: python workflow.py --resume {slug}")
        
    elif args.interactive:
        slug = workflow.create_interactive_project()
        if slug:
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