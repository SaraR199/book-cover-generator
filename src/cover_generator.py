"""
Cover Generation Module
Creates cover design strategies and detailed Ideogram prompts based on market research
"""

from datetime import datetime
from typing import Dict, List
import random

class CoverGenerator:
    def __init__(self):
        self.aspect_ratios = {
            "ebook": "2:3",
            "print": "3:4",
            "square": "1:1"
        }
        
        self.style_templates = {
            "photographic": "professional photography, high quality, detailed, realistic",
            "illustrated": "digital illustration, artistic, stylized, contemporary art style",
            "minimalist": "clean design, simple, elegant, minimal elements",
            "vintage": "retro aesthetic, aged texture, classic design elements",
            "modern": "contemporary design, sleek, professional, current trends",
            "artistic": "creative composition, unique artistic vision, expressive"
        }
        
    def develop_strategies(self, input_data: Dict, research_data: Dict) -> Dict:
        """Develop multiple cover design strategies based on research"""
        
        book_info = input_data["book_info"]
        genre_analysis = research_data["genre_analysis"]
        trends = genre_analysis["trends"]
        common_elements = genre_analysis["common_elements"]
        
        # Generate 4 distinct cover concepts
        concepts = []
        
        # Concept 1: Market-aligned (safe but effective)
        concepts.append(self._create_market_aligned_concept(book_info, common_elements, 1))
        
        # Concept 2: Trend-forward (current popular approaches)
        concepts.append(self._create_trend_forward_concept(book_info, trends, 2))
        
        # Concept 3: Differentiated (stand out from competition)
        concepts.append(self._create_differentiated_concept(book_info, trends, 3))
        
        # Concept 4: Artistic/Premium (higher-end aesthetic)
        concepts.append(self._create_artistic_concept(book_info, common_elements, 4))
        
        strategy_data = {
            "concepts": concepts,
            "rationale": {
                "approach": "Multi-strategy approach covering safe, trendy, unique, and premium aesthetics",
                "target_coverage": "Ensures options for different market positions and author preferences"
            },
            "metadata": {
                "created_date": datetime.now().isoformat(),
                "total_concepts": len(concepts),
                "genre": book_info["genre"]
            }
        }
        
        return strategy_data
    
    def _create_market_aligned_concept(self, book_info: Dict, common_elements: Dict, concept_id: int) -> Dict:
        """Create concept that aligns with proven market patterns"""
        
        # Use most common color palette
        primary_palette = common_elements.get("color_palettes", [{}])[0]
        
        # Use most common typography
        primary_typography = common_elements.get("typography_styles", [{}])[0]
        
        # Use most common imagery type
        primary_imagery = common_elements.get("imagery_types", [{}])[0]
        
        return {
            "id": concept_id,
            "concept_name": "Market Aligned",
            "design_approach": "Follows proven successful patterns in the genre",
            "strategy": "safe_effective",
            "color_palette": primary_palette,
            "typography": primary_typography,
            "imagery_focus": primary_imagery.get("type", "genre appropriate imagery"),
            "rationale": "Uses established visual language that readers expect and respond to in this genre",
            "risk_level": "low",
            "differentiation_level": "medium"
        }
    
    def _create_trend_forward_concept(self, book_info: Dict, trends: Dict, concept_id: int) -> Dict:
        """Create concept based on current trending approaches"""
        
        current_trends = trends.get("current_popular", [])
        emerging_trends = trends.get("emerging", [])
        
        selected_trend = current_trends[0] if current_trends else "contemporary design"
        emerging_element = emerging_trends[0] if emerging_trends else "innovative approach"
        
        return {
            "id": concept_id,
            "concept_name": "Trend Forward",
            "design_approach": f"Incorporates {selected_trend} with {emerging_element}",
            "strategy": "trendy_contemporary",
            "primary_trend": selected_trend,
            "emerging_element": emerging_element,
            "color_approach": "contemporary color trends",
            "typography_approach": "modern, on-trend fonts",
            "rationale": "Capitalizes on what's currently working while incorporating fresh elements",
            "risk_level": "medium",
            "differentiation_level": "high"
        }
    
    def _create_differentiated_concept(self, book_info: Dict, trends: Dict, concept_id: int) -> Dict:
        """Create concept that deliberately differentiates from oversaturated approaches"""
        
        oversaturated = trends.get("oversaturated", [])
        avoidance_strategy = f"Avoids: {', '.join(oversaturated[:2])}" if oversaturated else "Fresh perspective"
        
        return {
            "id": concept_id,
            "concept_name": "Differentiated",
            "design_approach": "Deliberately stands apart from common genre clichés",
            "strategy": "unique_standout",
            "avoids": oversaturated[:3] if oversaturated else [],
            "unique_elements": [
                "Unexpected color combinations",
                "Non-typical genre imagery",
                "Innovative layout approach"
            ],
            "differentiation_strategy": avoidance_strategy,
            "rationale": "Designed to stand out on crowded digital shelves by avoiding overused elements",
            "risk_level": "medium-high",
            "differentiation_level": "very high"
        }
    
    def _create_artistic_concept(self, book_info: Dict, common_elements: Dict, concept_id: int) -> Dict:
        """Create premium, artistic concept"""
        
        return {
            "id": concept_id,
            "concept_name": "Artistic Premium",
            "design_approach": "High-end aesthetic with artistic flair",
            "strategy": "premium_artistic",
            "aesthetic_focus": "sophisticated visual appeal",
            "artistic_elements": [
                "Custom illustration or photography",
                "Sophisticated color relationships",
                "Premium typography choices",
                "Balanced composition"
            ],
            "target_perception": "Literary quality, professional, premium product",
            "rationale": "Appeals to readers who value aesthetic quality and positions book as premium offering",
            "risk_level": "low-medium",
            "differentiation_level": "high"
        }
    
    def create_prompts(self, input_data: Dict, strategies: Dict) -> Dict:
        """Convert design strategies into detailed Ideogram prompts"""
        
        book_info = input_data["book_info"]
        concepts = strategies["concepts"]
        
        detailed_prompts = []
        
        for concept in concepts:
            # Generate detailed Ideogram prompt for this concept
            prompt_data = self._generate_ideogram_prompt(book_info, concept)
            detailed_prompts.append(prompt_data)
        
        prompts_data = {
            "cover_concepts": detailed_prompts,
            "prompt_variations": {
                "negative_prompts": [
                    "low quality", "blurry", "pixelated", "amateur", "unprofessional",
                    "generic stock photo", "cliche", "overused", "poor composition",
                    "bad typography", "illegible text", "cluttered", "extra text",
                    "unwanted text", "random words", "marketing copy"
                ],
                "quality_enhancers": [
                    "detailed", "crisp", "well composed", "high resolution"
                ],
                "style_modifiers": [
                    "contemporary", "sophisticated", "elegant", "artistic"
                ]
            },
            "generation_settings": {
                "model_version": "ideogram-v2",
                "quality": "premium", 
                "variations_per_concept": 2,
                "aspect_ratio": "2:3"  # Standard ebook ratio
            },
            "metadata": {
                "created_date": datetime.now().isoformat(),
                "total_concepts": len(detailed_prompts),
                "book_title": book_info["title"],
                "estimated_tokens": sum(len(p["ideogram_prompt"].split()) for p in detailed_prompts)
            }
        }
        
        return prompts_data
    
    def _generate_ideogram_prompt(self, book_info: Dict, concept: Dict) -> Dict:
        """Generate detailed Ideogram prompt for a specific concept"""
        
        title = book_info["title"]
        author = book_info["author"] 
        genre = book_info["genre"]
        description = book_info.get("description", "")
        
        # Extract key themes from description
        themes = self._extract_themes(description, genre)
        
        # Build prompt based on concept strategy
        if concept["strategy"] == "safe_effective":
            prompt = self._build_market_aligned_prompt(title, author, genre, themes, concept)
        elif concept["strategy"] == "trendy_contemporary":
            prompt = self._build_trend_forward_prompt(title, author, genre, themes, concept)
        elif concept["strategy"] == "unique_standout":
            prompt = self._build_differentiated_prompt(title, author, genre, themes, concept)
        elif concept["strategy"] == "premium_artistic":
            prompt = self._build_artistic_prompt(title, author, genre, themes, concept)
        else:
            prompt = self._build_generic_prompt(title, author, genre, themes)
        
        return {
            "id": concept["id"],
            "concept_name": concept["concept_name"],
            "design_approach": concept["design_approach"],
            "ideogram_prompt": prompt,
            "style_parameters": {
                "aspect_ratio": "2:3",
                "style": self._determine_style(concept),
                "mood": self._determine_mood(genre, themes),
                "color_scheme": self._determine_colors(concept, genre)
            },
            "text_overlay": {
                "title_text": title,
                "author_text": author,
                "title_placement": "prominent, readable",
                "author_placement": "secondary, bottom or top",
                "font_guidance": self._determine_font_style(concept, genre)
            },
            "rationale": concept.get("rationale", "Generated concept based on market analysis")
        }
    
    def _extract_themes(self, description: str, genre: str) -> List[str]:
        """Extract key themes from book description"""
        themes = []
        
        # Genre-based theme extraction
        theme_keywords = {
            "romance": ["love", "relationship", "passion", "heart", "couple", "dating"],
            "thriller": ["danger", "mystery", "suspense", "crime", "detective", "investigation"],
            "fantasy": ["magic", "magical", "dragon", "quest", "kingdom", "power", "spell"],
            "science fiction": ["future", "space", "technology", "alien", "robot", "time"],
            "mystery": ["murder", "detective", "clue", "solve", "investigation", "secret"]
        }
        
        genre_lower = genre.lower()
        for g, keywords in theme_keywords.items():
            if g in genre_lower:
                description_lower = description.lower()
                for keyword in keywords:
                    if keyword in description_lower:
                        themes.append(keyword)
        
        # If no themes found, use genre default
        if not themes:
            themes = [genre.lower().replace(" ", "_")]
        
        return themes[:3]  # Limit to top 3 themes
    
    def _build_market_aligned_prompt(self, title: str, author: str, genre: str, themes: List[str], concept: Dict) -> str:
        """Build prompt for market-aligned concept"""
        
        genre_visuals = {
            "romance": "elegant couple silhouette, soft lighting, warm romantic atmosphere",
            "thriller": "dark cityscape, shadows, dramatic lighting, urban setting", 
            "fantasy": "mystical landscape, magical elements, ethereal lighting, fantasy setting",
            "mystery": "foggy street scene, vintage detective elements, noir lighting"
        }
        
        visual_elements = genre_visuals.get(genre.lower(), f"{genre} themed imagery")
        theme_elements = ", ".join(themes) if themes else ""
        
        prompt = f"""{visual_elements}, {theme_elements}, 
        elegant title text "{title}", author text "{author}",
        clean typography, balanced composition"""
        
        return self._clean_prompt(prompt)
    
    def _build_trend_forward_prompt(self, title: str, author: str, genre: str, themes: List[str], concept: Dict) -> str:
        """Build prompt for trend-forward concept"""
        
        trend_element = concept.get("primary_trend", "modern geometric shapes")
        emerging_element = concept.get("emerging_element", "minimalist design")
        
        prompt = f"""Contemporary {genre} cover with {trend_element}, {emerging_element},
        vibrant modern colors, sleek composition,
        bold title text "{title}", stylish author text "{author}",
        trendy visual style"""
        
        return self._clean_prompt(prompt)
    
    def _build_differentiated_prompt(self, title: str, author: str, genre: str, themes: List[str], concept: Dict) -> str:
        """Build prompt for differentiated concept"""
        
        avoided_elements = concept.get("avoids", [])
        unique_visuals = "abstract art composition, unexpected color palette, unconventional layout"
        
        prompt = f"""Unique {genre} cover, {unique_visuals},
        creative visual elements, artistic composition,
        distinctive title text "{title}", creative author text "{author}",
        innovative design approach"""
        
        return self._clean_prompt(prompt)
    
    def _build_artistic_prompt(self, title: str, author: str, genre: str, themes: List[str], concept: Dict) -> str:
        """Build prompt for artistic premium concept"""
        
        prompt = f"""Artistic {genre} cover, fine art illustration, sophisticated colors,
        elegant visual composition, refined artistic style,
        beautiful title text "{title}", elegant author text "{author}",
        gallery-style artwork, premium aesthetic"""
        
        return self._clean_prompt(prompt)
    
    def _build_generic_prompt(self, title: str, author: str, genre: str, themes: List[str]) -> str:
        """Build generic prompt as fallback"""
        
        theme_text = ", ".join(themes) if themes else genre
        
        prompt = f"""{genre} book cover, {theme_text} imagery,
        title text "{title}", author text "{author}", clean design, balanced layout"""
        
        return self._clean_prompt(prompt)
    
    def _determine_style(self, concept: Dict) -> str:
        """Determine art style based on concept"""
        strategy = concept.get("strategy", "safe_effective")
        
        style_map = {
            "safe_effective": "photographic",
            "trendy_contemporary": "modern",
            "unique_standout": "artistic", 
            "premium_artistic": "illustrated"
        }
        
        return style_map.get(strategy, "professional")
    
    def _determine_mood(self, genre: str, themes: List[str]) -> str:
        """Determine mood based on genre and themes"""
        genre_moods = {
            "romance": "romantic, warm, inviting",
            "thriller": "suspenseful, dark, intense",
            "fantasy": "magical, epic, mysterious",
            "mystery": "intriguing, noir, atmospheric", 
            "horror": "dark, scary, ominous",
            "literary fiction": "sophisticated, thoughtful, elegant"
        }
        
        return genre_moods.get(genre.lower(), "professional, engaging")
    
    def _determine_colors(self, concept: Dict, genre: str) -> str:
        """Determine color scheme"""
        if "color_palette" in concept and "colors" in concept["color_palette"]:
            return ", ".join(concept["color_palette"]["colors"][:3])
        
        genre_colors = {
            "romance": "warm pinks, purples, golds",
            "thriller": "dark blues, blacks, red accents",
            "fantasy": "mystical purples, greens, golds",
            "mystery": "noir blacks, grays, amber highlights"
        }
        
        return genre_colors.get(genre.lower(), "professional color palette")
    
    def _determine_font_style(self, concept: Dict, genre: str) -> str:
        """Determine font style guidance"""
        if "typography" in concept and "style" in concept["typography"]:
            return concept["typography"]["style"]
        
        genre_fonts = {
            "romance": "elegant script or serif",
            "thriller": "bold sans serif",
            "fantasy": "decorative or medieval inspired",
            "mystery": "classic serif or film noir style"
        }
        
        return genre_fonts.get(genre.lower(), "clean, readable typography")
    
    def _clean_prompt(self, prompt: str) -> str:
        """Clean and optimize prompt text"""
        # Remove extra whitespace and normalize
        cleaned = " ".join(prompt.split())
        
        # Remove marketing-heavy phrases that might appear as text
        marketing_phrases = [
            "commercial book cover design",
            "bestseller aesthetic", 
            "market-ready design",
            "professional composition",
            "readable at thumbnail size",
            "commercial quality",
            "professional design",
            "genre-appropriate styling",
            "social media ready",
            "shelf-standout appeal",
            "premium positioning",
            "luxury book design"
        ]
        
        for phrase in marketing_phrases:
            cleaned = cleaned.replace(phrase, "")
        
        # Remove redundant phrases
        redundant_phrases = ["book cover design book cover", "professional professional"]
        for phrase in redundant_phrases:
            cleaned = cleaned.replace(phrase, phrase.split()[0])
        
        # Clean up extra commas and spaces
        cleaned = " ".join(cleaned.split())
        cleaned = cleaned.replace(", ,", ",").replace(",,", ",")
        cleaned = cleaned.strip(", ")
        
        return cleaned