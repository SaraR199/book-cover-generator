# Book Cover Generator

An AI-assisted workflow for generating professional book covers using market research and Ideogram API.

## Quick Start

```bash
python workflow.py --new "My Book Title" --author "Author Name" --genre "romantic suspense" --description "Brief plot description"
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

- `--new` - Start new book project
- `--resume` - Resume existing project
- `--step` - Run specific step only
- `--list` - List all projects
- `--status` - Show project status

## Pause/Resume

The workflow automatically saves state after each step. Resume anytime with:
```bash
python workflow.py --resume "book-slug"
```