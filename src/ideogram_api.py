"""
Ideogram API Integration
Handles communication with Ideogram API for image generation
"""

import requests
import json
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import base64

class IdeogramClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("IDEOGRAM_API_KEY")
        self.base_url = "https://api.ideogram.ai/v1"
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                "Api-Key": self.api_key,
                "Content-Type": "application/json"
            })
    
    def generate_covers(self, project_slug: str, prompts_data: Dict, output_dir: Path) -> Dict:
        """Generate all cover images for a project"""
        
        if not self.api_key:
            return self._simulate_generation(project_slug, prompts_data, output_dir)
        
        results = {
            "project_slug": project_slug,
            "generation_date": datetime.now().isoformat(),
            "images": [],
            "errors": [],
            "total_cost": 0.0,
            "api_calls": 0
        }
        
        cover_concepts = prompts_data.get("cover_concepts", [])
        settings = prompts_data.get("generation_settings", {})
        
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, concept in enumerate(cover_concepts):
            print(f"  Generating concept {concept['id']}: {concept['concept_name']}")
            
            try:
                # Generate variations for this concept
                variations_per_concept = settings.get("variations_per_concept", 2)
                
                for variation in range(variations_per_concept):
                    image_result = self._generate_single_image(
                        concept, 
                        variation + 1, 
                        settings,
                        output_dir,
                        project_slug
                    )
                    
                    if image_result["success"]:
                        results["images"].append(image_result)
                        results["total_cost"] += image_result.get("cost", 0)
                    else:
                        results["errors"].append({
                            "concept_id": concept["id"],
                            "variation": variation + 1,
                            "error": image_result.get("error", "Unknown error")
                        })
                    
                    results["api_calls"] += 1
                    
                    # Rate limiting - wait between requests
                    time.sleep(1)
                    
            except Exception as e:
                error_msg = f"Failed to generate concept {concept['id']}: {str(e)}"
                print(f"    ❌ {error_msg}")
                results["errors"].append({
                    "concept_id": concept["id"],
                    "error": error_msg
                })
        
        print(f"  ✓ Generated {len(results['images'])} images")
        if results["errors"]:
            print(f"  ⚠️  {len(results['errors'])} errors occurred")
        
        return results
    
    def _generate_single_image(self, concept: Dict, variation: int, settings: Dict, output_dir: Path, project_slug: str) -> Dict:
        """Generate a single image using Ideogram v3 API"""
        
        # Prepare request payload for v3 API
        payload = {
            "prompt": concept["ideogram_prompt"],
            "aspect_ratio": self._convert_aspect_ratio(concept["style_parameters"].get("aspect_ratio", "2:3")),
            "rendering_speed": settings.get("rendering_speed", "TURBO")
        }
        
        try:
            # Make API request to v3 endpoint
            response = self.session.post(f"{self.base_url}/ideogram-v3/generate", json=payload)
            response.raise_for_status()
            
            result_data = response.json()
            
            # Process the response
            if "data" in result_data and result_data["data"]:
                image_data = result_data["data"][0]
                
                # Download and save the image
                image_url = image_data.get("url")
                if image_url:
                    filename = f"{project_slug}_concept_{concept['id']}_v{variation}.png"
                    filepath = output_dir / filename
                    
                    success = self._download_image(image_url, filepath)
                    
                    if success:
                        return {
                            "success": True,
                            "concept_id": concept["id"],
                            "concept_name": concept["concept_name"],
                            "variation": variation,
                            "filename": filename,
                            "filepath": str(filepath),
                            "prompt_used": concept["ideogram_prompt"],
                            "image_url": image_url,
                            "cost": self._estimate_cost(payload),
                            "generation_time": datetime.now().isoformat()
                        }
            
            return {
                "success": False,
                "error": "No image data in API response",
                "response": result_data
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def _simulate_generation(self, project_slug: str, prompts_data: Dict, output_dir: Path) -> Dict:
        """Simulate image generation when no API key is available"""
        
        print("  🔄 Simulating image generation (no API key provided)")
        
        results = {
            "project_slug": project_slug,
            "generation_date": datetime.now().isoformat(),
            "images": [],
            "errors": [],
            "total_cost": 0.0,
            "api_calls": 0,
            "simulation": True
        }
        
        cover_concepts = prompts_data.get("cover_concepts", [])
        settings = prompts_data.get("generation_settings", {})
        
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create placeholder images for each concept
        for concept in cover_concepts:
            variations_per_concept = settings.get("variations_per_concept", 2)
            
            for variation in range(variations_per_concept):
                filename = f"{project_slug}_concept_{concept['id']}_v{variation + 1}_placeholder.txt"
                filepath = output_dir / filename
                
                # Create placeholder file with prompt details
                placeholder_content = f"""PLACEHOLDER - Book Cover Image
                
Project: {project_slug}
Concept: {concept['concept_name']} (ID: {concept['id']})
Variation: {variation + 1}
Generated: {datetime.now().isoformat()}

IDEOGRAM PROMPT:
{concept['ideogram_prompt']}

STYLE PARAMETERS:
- Aspect Ratio: {concept['style_parameters'].get('aspect_ratio', '2:3')}
- Style: {concept['style_parameters'].get('style', 'professional')}
- Mood: {concept['style_parameters'].get('mood', 'genre-appropriate')}
- Colors: {concept['style_parameters'].get('color_scheme', 'professional palette')}

TEXT OVERLAY:
- Title: "{concept['text_overlay']['title_text']}"
- Author: "{concept['text_overlay']['author_text']}"
- Font Style: {concept['text_overlay']['font_guidance']}

RATIONALE:
{concept['rationale']}

To generate actual images, configure your Ideogram API key:
export IDEOGRAM_API_KEY="your-api-key-here"
"""
                
                # Save placeholder
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(placeholder_content)
                
                results["images"].append({
                    "success": True,
                    "concept_id": concept["id"],
                    "concept_name": concept["concept_name"],
                    "variation": variation + 1,
                    "filename": filename,
                    "filepath": str(filepath),
                    "prompt_used": concept["ideogram_prompt"],
                    "placeholder": True,
                    "generation_time": datetime.now().isoformat()
                })
        
        print(f"  ✓ Created {len(results['images'])} placeholder files")
        return results
    
    def _download_image(self, url: str, filepath: Path) -> bool:
        """Download image from URL and save to file"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return True
            
        except Exception as e:
            print(f"    ❌ Failed to download image: {str(e)}")
            return False
    
    def _map_style_type(self, style: str) -> str:
        """Map our internal style names to Ideogram style types"""
        style_mapping = {
            "photographic": "GENERAL",
            "illustrated": "DESIGN",
            "minimalist": "DESIGN",
            "vintage": "GENERAL",
            "modern": "DESIGN",
            "artistic": "DESIGN",
            "professional": "GENERAL"
        }
        
        return style_mapping.get(style.lower(), "GENERAL")
    
    def _estimate_cost(self, payload: Dict) -> float:
        """Estimate cost for API call (placeholder - update with actual pricing)"""
        # Ideogram pricing varies - this is a placeholder
        base_cost = 0.08  # Example: $0.08 per image
        
        # Adjust based on model and quality settings
        model = payload.get("model", "V_2")
        if model == "V_2_TURBO":
            base_cost *= 0.5
        elif model == "V_2":
            base_cost *= 1.0
        
        return base_cost
    
    def _convert_aspect_ratio(self, ratio_str: str) -> str:
        """Convert aspect ratio from '2:3' format to Ideogram v3 format"""
        ratio_mapping = {
            "1:1": "1x1",
            "2:3": "2x3", 
            "3:2": "3x2",
            "3:4": "3x4",
            "4:3": "4x3",
            "9:16": "9x16",
            "16:9": "16x9"
        }
        return ratio_mapping.get(ratio_str, "2x3")
    
    def check_api_status(self) -> Dict:
        """Check if API is accessible and working"""
        if not self.api_key:
            return {
                "status": "no_key",
                "message": "No API key configured",
                "working": False
            }
        
        try:
            # Test API with a simple generation request
            test_payload = {
                "prompt": "A simple test image",
                "rendering_speed": "TURBO"
            }
            
            response = self.session.post(f"{self.base_url}/ideogram-v3/generate", json=test_payload)
            
            if response.status_code == 200:
                return {
                    "status": "working",
                    "message": "API key valid and service accessible",
                    "working": True
                }
            else:
                return {
                    "status": "error",
                    "message": f"API returned status {response.status_code}: {response.text}",
                    "working": False
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Cannot reach API: {str(e)}",
                "working": False
            }