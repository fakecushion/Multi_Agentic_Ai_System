# Deployment on Hugging Face Spaces

This guide provides step-by-step instructions for deploying the Multi-Agent AI System on Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account
2. API keys for:
   - Groq API
   - SerpAPI
   - Google AI Studio (optional)

## Deployment Steps

### 1. Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click on "New Space"
3. Fill in the following details:
   - **Space name**: Choose a name for your space (e.g., `multi-agent-ai-system`)
   - **License**: Apache 2.0 (as specified in the configuration)
   - **SDK**: Docker
   - **Visibility**: Public or Private (your choice)

### 2. Upload Files

After creating the space, you'll need to upload all the project files:

1. Clone your space repository:
   ```bash
   git clone https://huggingface.co/spaces/your-username/your-space-name
   cd your-space-name
   ```

2. Copy all files from this project to the cloned repository:
   - All Python files (main.py, requirements.txt, etc.)
   - The entire `app/` directory
   - `sample_pdfs/` directory
   - `frontend.html`
   - `Dockerfile`
   - `huggingface_space_config.json`
   - `app.py` (Gradio interface)
   - `start_gradio.py` (Gradio startup script)

3. Commit and push the files:
   ```bash
   git add .
   git commit -m "Initial commit: Multi-Agent AI System"
   git push
   ```

### 3. Configure Environment Variables

1. In your Hugging Face Space, go to "Settings" tab
2. Scroll down to "Repository secrets" section
3. Add the following environment variables:
   - `GROQ_API_KEY`: Your Groq API key
   - `SERPAPI_API_KEY`: Your SerpAPI key
   - `GOOGLE_AI_API_KEY`: Your Google AI Studio API key (optional)

### 4. Space Configuration

The space will automatically use the provided configuration:
- **SDK**: Docker (as specified in `huggingface_space_config.json`)
- **Port**: 8000 (as specified in the configuration)
- **License**: Apache 2.0

### 5. Docker Configuration

The provided `Dockerfile` is already configured for deployment:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "start_gradio.py"]
```

Note: We've updated the CMD to use `start_gradio.py` which launches both the backend API and Gradio interface.

### 6. Requirements

The `requirements.txt` file includes all necessary dependencies:
```
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
pydantic==2.5.0
faiss-cpu==1.8.0
PyMuPDF==1.23.8
sentence-transformers==2.2.2
groq==0.5.0
google-generativeai==0.3.2
arxiv==2.1.0
requests==2.31.0
beautifulsoup4==4.12.2
python-dotenv==1.0.0
PyPDF2==3.0.1
langchain==0.0.350
langchain-community==0.0.11
chromadb==0.4.22
pytest==7.4.3
httpx==0.25.2
reportlab==4.0.4
gradio==4.0.0
```

## Accessing the Deployed Application

Once the deployment is complete:
1. The application will be available at your space's URL
2. The interface will automatically use Gradio for a better user experience
3. Example: `https://your-username-your-space-name.hf.space`

## API Endpoints

The deployed system provides the following endpoints:
- `POST /ask` - Submit questions to the multi-agent system
- `POST /upload_pdf` - Upload PDF files for processing
- `GET /logs` - Retrieve system logs

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check the build logs in the "Logs" tab of your space
   - Ensure all dependencies in `requirements.txt` are correct
   - Verify the Dockerfile syntax

2. **Runtime Errors**:
   - Check that all environment variables are properly set
   - Verify API keys are valid and have sufficient quotas
   - Check the application logs in the "Logs" tab

3. **Performance Issues**:
   - The free tier of Hugging Face Spaces has resource limitations
   - Consider upgrading to a paid tier for better performance
   - Some operations (like PDF processing) may take time

### Resource Limitations

Hugging Face Spaces have the following limitations on the free tier:
- Memory: 16GB
- CPU: Shared
- Disk: 50GB
- Startup time: 60 seconds

## Updating the Deployment

To update your deployed application:

1. Make changes to your local files
2. Commit and push to your Hugging Face Space repository:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```

The space will automatically rebuild and redeploy with your changes.

## Monitoring

You can monitor your application through:
1. The "Logs" tab in your space's dashboard
2. The built-in logging system that tracks all interactions
3. The `/logs` endpoint of your API

## Security Considerations

1. Never commit API keys to the repository
2. Always use environment variables for sensitive information
3. The system includes basic file upload validation
4. PDF files are processed in memory and not permanently stored

## Support

For issues with the deployment:
1. Check the Hugging Face [documentation](https://huggingface.co/docs/hub/spaces)
2. Review the application logs
3. Verify all configuration files are correct