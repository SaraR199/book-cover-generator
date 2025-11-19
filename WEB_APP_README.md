# Book Cover Generator - Web App

A modern web interface for AI-assisted book cover generation using market research and the Ideogram API.

## Features

- **Intuitive Web Interface**: Create book cover projects through a beautiful, user-friendly web interface
- **Real-time Progress Tracking**: Monitor generation progress with live status updates
- **Project Management**: View all your projects and their status at a glance
- **Cover Gallery**: Preview and download all generated cover variations
- **Automated Workflow**: 6-step process runs automatically once you submit your book details

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Ideogram API Key

Set your Ideogram API key as an environment variable:

```bash
export IDEOGRAM_API_KEY="your-api-key-here"
```

Or create a `.env` file in the project root:

```
IDEOGRAM_API_KEY=your-api-key-here
```

### 3. Launch the Web App

```bash
python app.py
```

Or use the startup script:

```bash
chmod +x start_webapp.sh
./start_webapp.sh
```

### 4. Open Your Browser

Navigate to: **http://localhost:5000**

## How to Use

### Creating a New Project

1. Click the **"Create New Project"** tab
2. Fill in the form:
   - **Book Title**: Your book's title
   - **Author Name**: The author's name
   - **Genre**: Select from the dropdown (romance, thriller, fantasy, etc.)
   - **Book Description**: Provide a detailed marketing brief including:
     - Plot summary
     - Target audience
     - Themes and tone
     - Visual elements you envision
     - Any specific imagery or style preferences
3. Click **"Create Project & Generate Covers"**
4. The system will automatically start the generation workflow

### Monitoring Progress

Once generation starts, you'll see real-time status updates:

- **Market Research**: Analyzing genre trends and competitor covers
- **Cover Strategy**: Developing 4 distinct design approaches
- **Prompt Generation**: Creating AI-optimized prompts for Ideogram
- **Image Generation**: Generating cover images via Ideogram API
- **Output Organization**: Finalizing and organizing results

### Viewing Your Projects

1. Click the **"My Projects"** tab to see all your projects
2. Projects show their current status:
   - **NOT STARTED**: Project created but generation not started
   - **RUNNING**: Generation in progress (animated pulse)
   - **COMPLETED**: All covers generated successfully
   - **ERROR**: Something went wrong (click to retry)
3. Click any project card to view details and generated covers

### Downloading Covers

Once generation is complete:
1. View the project details
2. Scroll to the **"Generated Covers"** section
3. Click the **"Download"** button under any cover you like

## Architecture

### Backend (Flask)

The web app uses Flask to provide a REST API that wraps the existing workflow:

**API Endpoints:**
- `GET /api/projects` - List all projects
- `POST /api/projects` - Create new project
- `GET /api/projects/<slug>` - Get project details
- `POST /api/projects/<slug>/generate` - Start generation
- `GET /api/projects/<slug>/status` - Check generation status
- `GET /api/covers/<slug>/<filename>` - Serve cover images
- `GET /api/genres` - Get supported genres

### Frontend (HTML/CSS/JavaScript)

- Single-page application with tab-based navigation
- Real-time status polling during generation
- Responsive design that works on desktop and mobile
- No framework dependencies - vanilla JavaScript for simplicity

### Workflow Integration

The web app uses the existing Python workflow modules:
- `src/workflow_state.py` - Project state management
- `src/market_research.py` - Genre analysis
- `src/cover_generator.py` - Strategy and prompt generation
- `src/ideogram_api.py` - Ideogram API integration

## Project Structure

```
book-cover-generator/
├── app.py                    # Flask web server
├── templates/
│   └── index.html           # Web interface
├── projects/                # User projects
│   └── {book-slug}/
│       ├── input.json       # Book details
│       ├── research.json    # Market research
│       ├── strategies.json  # Design strategies
│       ├── prompts.json     # Ideogram prompts
│       ├── covers/          # Generated images
│       └── web_status.json  # Web app status tracking
├── src/                     # Workflow modules
├── config/                  # Configuration
└── requirements.txt         # Python dependencies
```

## Workflow Steps

The automated workflow consists of 6 steps:

1. **Input Collection**: Book details captured through web form
2. **Market Research**: AI analyzes genre-specific cover trends
3. **Cover Strategy**: Generates 4 distinct design approaches:
   - Market Aligned (proven patterns)
   - Trend Forward (current trends)
   - Differentiated (unique approach)
   - Artistic Premium (high-end aesthetic)
4. **Prompt Generation**: Creates clean, visual-focused Ideogram prompts
5. **Image Generation**: Calls Ideogram API to generate covers
6. **Output Organization**: Finalizes results and creates report

## Configuration

### Ideogram API

The app uses the Ideogram v3 API. You'll need:
- An Ideogram API key (get one at https://ideogram.ai)
- Sufficient credits (approximately $0.08 per image)

### Image Settings

Default settings (configurable in `config/workflow.json`):
- **eBook covers**: 1600 × 2560 pixels
- **Print covers**: 1800 × 2700 pixels
- **Variations per strategy**: 2 images (8 total)

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, edit `app.py` and change the port:

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### API Key Not Found

Make sure your `IDEOGRAM_API_KEY` is set correctly:

```bash
echo $IDEOGRAM_API_KEY  # Should output your API key
```

### Generation Fails

Check the project's `web_status.json` file for error details:

```bash
cat projects/your-book-slug/web_status.json
```

### Missing Dependencies

Reinstall requirements:

```bash
pip install -r requirements.txt --upgrade
```

## Development vs Production

This is a **prototype** for development. For production deployment:

1. **Use a production WSGI server** (Gunicorn, uWSGI):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Add authentication** to protect your projects

3. **Use a proper database** instead of JSON files

4. **Add rate limiting** to prevent abuse

5. **Set up HTTPS** for secure communication

6. **Configure proper error handling** and logging

7. **Add file upload limits** and validation

## CLI vs Web App

The original CLI (`workflow.py`) is still fully functional. Choose based on your needs:

### Use CLI when:
- Running batch operations
- Integrating with scripts
- Working on a remote server
- Prefer command-line workflows

### Use Web App when:
- Prefer visual interfaces
- Need to monitor progress in real-time
- Want to preview covers immediately
- Sharing with non-technical users

## Support

For issues or questions:
- Check the main [CLAUDE.md](CLAUDE.md) for workflow details
- Review the [src/](src/) modules for implementation details
- Consult Ideogram API docs: https://ideogram.ai/api-docs

## Future Enhancements

Potential improvements for this prototype:

- [ ] User authentication and multi-user support
- [ ] Cover editing/regeneration with modified prompts
- [ ] Batch project creation
- [ ] Export to PDF/print-ready formats
- [ ] A/B testing and cover comparison tools
- [ ] Integration with print-on-demand services
- [ ] Mobile app version
- [ ] Social sharing features
- [ ] Cover rating and feedback system

## License

Same as the main project.
