# Quick Gemini API Configuration

Your API key: `AIzaSyAawrK4VzONcMJ8B7rGfift2Mbx6Psxd2Y`

## Create .env file in backend/ directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/document_platform
JWT_SECRET=change-this-to-a-random-secret-string
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

LLM_PROVIDER=gemini
GEMINI_API_KEY=AIzaSyAawrK4VzONcMJ8B7rGfift2Mbx6Psxd2Y

EXPORT_TMP_DIR=./exports
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
```

**Important**: 
- Replace `DATABASE_URL` with your PostgreSQL connection string
- Replace `JWT_SECRET` with a secure random string
- The `.env` file is already in `.gitignore` (won't be committed)

After creating `.env`, restart the backend server for changes to take effect.

