#!/usr/bin/env python3
"""
Book Cover Generator Web App
Flask-based web interface for AI-assisted book cover generation
"""

import os
import json
import threading
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

# Import existing workflow modules
from src.workflow_state import WorkflowState
from src.market_research import MarketResearcher
from src.cover_generator import CoverGenerator
from src.ideogram_api import IdeogramClient

app = Flask(__name__)
CORS(app)

# Configuration
BASE_DIR = Path(__file__).parent
PROJECTS_DIR = BASE_DIR / "projects"
PROJECTS_DIR.mkdir(exist_ok=True)

# Store active generation threads
active_generations = {}


class WebWorkflowRunner:
    """Runs the workflow asynchronously for web requests"""

    def __init__(self, project_slug):
        self.project_slug = project_slug
        self.state = WorkflowState(str(PROJECTS_DIR))
        self.state.load_project(project_slug)

    def run_workflow(self):
        """Execute the complete workflow"""
        try:
            self.update_status("running", "Starting workflow...")

            # Step 2: Market Research
            if not self.state.is_step_completed("market_research"):
                self.update_status("running", "Conducting market research...")
                self.run_market_research()

            # Step 3: Cover Strategy
            if not self.state.is_step_completed("cover_strategy"):
                self.update_status("running", "Developing cover strategies...")
                self.run_cover_strategy()

            # Step 4: Prompt Generation
            if not self.state.is_step_completed("prompt_generation"):
                self.update_status("running", "Generating Ideogram prompts...")
                self.run_prompt_generation()

            # Step 5: Image Generation
            if not self.state.is_step_completed("image_generation"):
                self.update_status("running", "Generating cover images...")
                self.run_image_generation()

            # Step 6: Final Report
            if not self.state.is_step_completed("output_organization"):
                self.update_status("running", "Creating final report...")
                self.run_output_organization()

            self.update_status("completed", "Workflow completed successfully!")

        except Exception as e:
            self.update_status("error", f"Error: {str(e)}")
            raise

    def update_status(self, status, message):
        """Update the project status"""
        status_file = self.state.project_dir / "web_status.json"
        status_data = {
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        with open(status_file, 'w') as f:
            json.dump(status_data, f, indent=2)

    def run_market_research(self):
        """Run market research step"""
        book_info = self.state.project_data.get("book_info", {})
        researcher = MarketResearcher()
        research = researcher.research_genre(
            book_info.get("genre", ""),
            book_info.get("description", "")
        )

        output_file = self.state.project_dir / "research.json"
        with open(output_file, 'w') as f:
            json.dump(research, f, indent=2)

        self.state.mark_step_completed("market_research")

    def run_cover_strategy(self):
        """Run cover strategy step"""
        book_info = self.state.project_data.get("book_info", {})
        research_file = self.state.project_dir / "research.json"

        with open(research_file) as f:
            research = json.load(f)

        generator = CoverGenerator()
        strategies = generator.generate_strategies(book_info, research)

        output_file = self.state.project_dir / "strategies.json"
        with open(output_file, 'w') as f:
            json.dump(strategies, f, indent=2)

        self.state.mark_step_completed("cover_strategy")

    def run_prompt_generation(self):
        """Run prompt generation step"""
        book_info = self.state.project_data.get("book_info", {})
        strategies_file = self.state.project_dir / "strategies.json"

        with open(strategies_file) as f:
            strategies = json.load(f)

        generator = CoverGenerator()
        prompts = generator.generate_prompts(book_info, strategies)

        output_file = self.state.project_dir / "prompts.json"
        with open(output_file, 'w') as f:
            json.dump(prompts, f, indent=2)

        self.state.mark_step_completed("prompt_generation")

    def run_image_generation(self):
        """Run image generation step"""
        prompts_file = self.state.project_dir / "prompts.json"

        with open(prompts_file) as f:
            prompts_data = json.load(f)

        client = IdeogramClient()
        covers_dir = self.state.project_dir / "covers"
        covers_dir.mkdir(exist_ok=True)

        results = client.generate_covers(prompts_data, str(covers_dir))

        output_file = self.state.project_dir / "generation_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        self.state.mark_step_completed("image_generation")

    def run_output_organization(self):
        """Run output organization step"""
        results_file = self.state.project_dir / "generation_results.json"

        with open(results_file) as f:
            results = json.load(f)

        book_info = self.state.project_data.get("book_info", {})

        report = {
            "project": {
                "title": book_info.get("title"),
                "author": book_info.get("author"),
                "genre": book_info.get("genre")
            },
            "summary": {
                "total_designs": results.get("total_designs", 0),
                "successful_generations": results.get("successful_generations", 0),
                "failed_generations": results.get("failed_generations", 0)
            },
            "deliverables": {
                "cover_images": str(self.state.project_dir / "covers"),
                "prompts": str(self.state.project_dir / "prompts.json"),
                "strategies": str(self.state.project_dir / "strategies.json"),
                "research": str(self.state.project_dir / "research.json")
            },
            "generated_at": datetime.now().isoformat()
        }

        output_file = self.state.project_dir / "final_report.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        self.state.mark_step_completed("output_organization")


# API Routes

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')


@app.route('/api/projects', methods=['GET'])
def list_projects():
    """List all projects"""
    try:
        state = WorkflowState(str(PROJECTS_DIR))
        projects = state.list_projects()

        # Add status information for each project
        for project in projects:
            slug = project['slug']
            status_file = PROJECTS_DIR / slug / "web_status.json"
            if status_file.exists():
                with open(status_file) as f:
                    project['web_status'] = json.load(f)
            else:
                project['web_status'] = {"status": "not_started", "message": "Not started"}

        return jsonify({
            "success": True,
            "projects": projects
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    try:
        data = request.json

        # Validate required fields
        required_fields = ['title', 'author', 'genre', 'description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400

        # Create project
        state = WorkflowState(str(PROJECTS_DIR))
        project_slug = state.create_project(
            title=data['title'],
            author=data['author'],
            genre=data['genre'],
            description=data['description']
        )

        return jsonify({
            "success": True,
            "project_slug": project_slug,
            "message": "Project created successfully"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/projects/<slug>', methods=['GET'])
def get_project(slug):
    """Get project details"""
    try:
        state = WorkflowState(str(PROJECTS_DIR))
        state.load_project(slug)

        # Get project data
        project_data = state.project_data

        # Get workflow status
        workflow_status = state.get_workflow_status()

        # Get web status
        status_file = state.project_dir / "web_status.json"
        if status_file.exists():
            with open(status_file) as f:
                web_status = json.load(f)
        else:
            web_status = {"status": "not_started", "message": "Not started"}

        # Get generated covers
        covers = []
        covers_dir = state.project_dir / "covers"
        if covers_dir.exists():
            for cover_file in covers_dir.glob("*.png"):
                covers.append({
                    "filename": cover_file.name,
                    "url": f"/api/covers/{slug}/{cover_file.name}"
                })

        return jsonify({
            "success": True,
            "project": {
                "slug": slug,
                "data": project_data,
                "workflow_status": workflow_status,
                "web_status": web_status,
                "covers": covers
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/projects/<slug>/generate', methods=['POST'])
def generate_covers(slug):
    """Start cover generation for a project"""
    try:
        # Check if generation is already running
        if slug in active_generations and active_generations[slug].is_alive():
            return jsonify({
                "success": False,
                "error": "Generation already in progress"
            }), 400

        # Start generation in background thread
        runner = WebWorkflowRunner(slug)
        thread = threading.Thread(target=runner.run_workflow)
        thread.daemon = True
        thread.start()

        active_generations[slug] = thread

        return jsonify({
            "success": True,
            "message": "Generation started"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/projects/<slug>/status', methods=['GET'])
def get_project_status(slug):
    """Get the current status of a project"""
    try:
        status_file = PROJECTS_DIR / slug / "web_status.json"

        if status_file.exists():
            with open(status_file) as f:
                status = json.load(f)
        else:
            status = {"status": "not_started", "message": "Not started"}

        # Check if thread is still running
        is_running = slug in active_generations and active_generations[slug].is_alive()
        status['is_running'] = is_running

        return jsonify({
            "success": True,
            "status": status
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/covers/<slug>/<filename>')
def serve_cover(slug, filename):
    """Serve a generated cover image"""
    covers_dir = PROJECTS_DIR / slug / "covers"
    return send_from_directory(covers_dir, filename)


@app.route('/api/genres', methods=['GET'])
def get_genres():
    """Get list of supported genres"""
    genres = [
        "romance", "thriller", "fantasy", "mystery", "sci-fi",
        "literary fiction", "horror", "historical fiction",
        "young adult", "memoir", "self-help", "business",
        "paranormal romance", "romantic suspense", "urban fantasy"
    ]
    return jsonify({
        "success": True,
        "genres": sorted(genres)
    })


if __name__ == '__main__':
    # Ensure templates directory exists
    templates_dir = BASE_DIR / "templates"
    templates_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("Book Cover Generator Web App")
    print("=" * 60)
    print(f"Server starting on http://localhost:5000")
    print(f"Projects directory: {PROJECTS_DIR}")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5000)
