# 🔐 Environment Variables Setup Guide

This guide explains how to securely configure your environment variables using `.env` files.

## 🚨 Security Notice

**Your API key has been moved to a secure `.env` file!** 🔒

Never commit API keys directly in code files. Always use environment variables or `.env` files.

## 📁 File Structure

```
backend/
├── .env                 # Your actual API key (NEVER commit this)
├── .env.example        # Template for others (safe to commit)
└── main.py            # Loads from .env automatically
```

## 🛠️ Quick Setup

### Option 1: Use the Generated .env File
Your API key has been automatically moved to `backend/.env`:

```bash
cd backend
cat .env  # Verify your API key is there
```

### Option 2: Create Your Own .env File
```bash
cd backend
cp .env.example .env
# Edit .env and add your API key
```

### Option 3: Manual Creation
```bash
cd backend
echo "GROK_API_KEY=your-api-key-here" > .env
```

## 📝 .env File Format

```bash
# Grok AI API Key (required for AI processing)
GROK_API_KEY=xai-your-actual-api-key-here

# Application Environment (optional)
ENVIRONMENT=development

# Logging Level (optional)
LOG_LEVEL=INFO
```

## ✅ Verification

Check if your setup is working:

```bash
# Start the backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Check status
curl http://localhost:8000/health
# Should show: "grok_ai": "available"
```

## 🔧 Usage in Code

The application automatically loads your `.env` file:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env file
api_key = os.getenv('GROK_API_KEY')  # Gets your key
```

## 🛡️ Security Best Practices

### ✅ DO:
- ✅ Use `.env` files for sensitive data
- ✅ Add `.env` to `.gitignore`
- ✅ Use `.env.example` for templates
- ✅ Rotate API keys regularly

### ❌ DON'T:
- ❌ Commit `.env` files to Git
- ❌ Share API keys in chat/email
- ❌ Hardcode keys in source code
- ❌ Use production keys in development

## 🔄 Updating Your API Key

1. **Edit the .env file:**
   ```bash
   cd backend
   nano .env  # or vim, code, etc.
   ```

2. **Update the key:**
   ```bash
   GROK_API_KEY=your-new-api-key-here
   ```

3. **Restart the backend:**
   ```bash
   ./start-backend.sh
   ```

## 🌍 Environment-Specific Setup

### Development
```bash
# backend/.env
GROK_API_KEY=xai-dev-key-here
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

### Production
```bash
# backend/.env
GROK_API_KEY=xai-prod-key-here
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## 🆘 Troubleshooting

### API Key Not Working?
```bash
# Check if .env file exists
ls -la backend/.env

# Check if key is set
cd backend && python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Key:', os.getenv('GROK_API_KEY')[:10] + '...' if os.getenv('GROK_API_KEY') else 'NOT SET')"

# Check API status
curl http://localhost:8000/setup-help
```

### File Permissions
```bash
# Make sure .env is readable
chmod 600 backend/.env
```

## 📚 Learn More

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **python-dotenv**: https://github.com/theskumar/python-dotenv
- **Grok API**: https://console.x.ai/

---

**🔒 Your API key is now secure and your application is ready to use! 🚀** 