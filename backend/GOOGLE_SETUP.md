# Google Calendar API Setup Guide

## Environment Variables Required

Create a `.env` file in the `backend/` directory with the following variables:

```env
# Google OAuth2 Configuration
# Get these values from Google Cloud Console > APIs & Services > Credentials

# Required for Google Calendar API
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Optional - these have default values but can be customized
GOOGLE_REDIRECT_URI=http://localhost
GOOGLE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_CERT_URL=https://www.googleapis.com/oauth2/v1/certs

# Other API Keys
GEMINI_API_KEY=your_gemini_api_key_here
```

## How to Get Google OAuth2 Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click "Enable"
4. Create OAuth2 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Desktop application" or "Web application"
   - Add `http://localhost` to authorized redirect URIs
   - Copy the Client ID and Client Secret
5. Add the credentials to your `.env` file

## How It Works

The `get_creds()` function in `calender.py` now:
1. Reads OAuth2 credentials from environment variables
2. Creates a client configuration dynamically
3. Handles the OAuth2 flow without needing a `credentials.json` file
4. Stores the access token in `token.pickle` for future use

## Benefits

- No need to manage `credentials.json` files
- Environment variables are more secure
- Easier deployment across different environments
- Follows security best practices 