# Book Cover Generator

An AI-assisted workflow for generating professional book covers using market research and Ideogram API.

## Quick Start

### Interactive Mode (Recommended)
```bash
python workflow.py --interactive
```
This will prompt you for each field and allow multi-line descriptions.

### Command Line Mode
```bash
python workflow.py --new "My Book Title" "Author Name" "romantic suspense" "Brief plot description"
```

## Folder Structure

```
book-cover-generator/
├── projects/                 # Individual book projects
│   └── {book-slug}/         # One folder per book
│       ├── input.json       # Book details
│       ├── research.json    # Market research results
│       ├── prompts.json     # Generated Ideogram prompts
│       ├── covers/          # Generated cover images
│       └── workflow.json    # Workflow state for pause/resume
├── books/                   # Legacy structure (will migrate to projects/)
├── config/                  # Global configuration
├── templates/               # Prompt templates
└── src/                     # Source code modules
```

## Workflow Steps

1. **Input Collection** - Gather basic book info
2. **Market Research** - Analyze current genre trends
3. **Cover Design** - Generate design strategies
4. **Prompt Creation** - Create Ideogram prompts
5. **Image Generation** - Call Ideogram API
6. **Output Organization** - Save and organize results

## Commands

- `--interactive` - Create new project with guided prompts (recommended for long descriptions)
- `--new` - Create new project with command line arguments
- `--resume` - Resume existing project
- `--step` - Run specific step only
- `--list` - List all projects
- `--status` - Show project status

## Pause/Resume

The workflow automatically saves state after each step. Resume anytime with:
```bash
python workflow.py --resume "book-slug"
```

## Ideogram Prompt Guidelines

The system generates clean, visual-focused prompts to avoid unwanted text on covers:

### What's Included
- **Visual Elements**: Specific imagery, lighting, composition details
- **Title/Author Text**: Only the exact book title and author name in quotes
- **Style Descriptors**: Art style, color palette, mood

### What's Excluded
- Marketing language (e.g., "bestseller aesthetic", "commercial quality")
- Business terms (e.g., "market-ready", "professional design") 
- Quality descriptors that might render as text (e.g., "high quality typography")

### Example Clean Prompt
```
elegant couple silhouette, soft lighting, warm romantic atmosphere, 
elegant title text "Blood Moon Rising", author text "Sara Riouch",
clean typography, balanced composition
```

### Negative Prompts
The system automatically includes negative prompts to prevent unwanted text:
- "extra text", "unwanted text", "random words", "marketing copy"

## Interactive Mode Features

When using `--interactive`, you get:

- **Easy Multi-line Descriptions**: Paste your full book blurb without worrying about shell escaping
- **Genre Suggestions**: Common genres are displayed to help with selection
- **Input Validation**: Required fields are checked before proceeding
- **Summary Review**: See all your input before creating the project
- **Confirmation Prompt**: Confirm before project creation

### Interactive Mode Example
```
=== Interactive Book Cover Project Creation ===

Book Title: Blood Moon Rising
Author Name: Sara Riouch

Common genres: romance, thriller, fantasy, mystery, sci-fi, literary fiction, horror
Genre: paranormal romance

Book Description/Blurb:
(You can paste your full book blurb here. Press Enter twice when finished)

Luna thought her biggest problem was hiding her wolf shifter 
abilities from her human coworkers. But when the mysterious 
Kai arrives in town during the blood moon, everything changes.

As alpha of the most feared pack in the region, Kai recognizes 
Luna as his fated mate instantly. But Luna has secrets that 
could destroy both their packs, and enemies from Kai's past 
are closing in.

==================================================
PROJECT SUMMARY
==================================================
Title: Blood Moon Rising
Author: Sara Riouch
Genre: paranormal romance
Description: Luna thought her biggest problem was hiding her wolf shifter abilities from her human coworkers...
==================================================

Create this project? [y/N]: y
```