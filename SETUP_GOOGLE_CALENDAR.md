# Google Calendar OAuth Setup Guide

Follow these steps to enable calendar integration for your study planner.

---

## Step 1: Access Google Cloud Console

1. Open your browser and go to: **https://console.cloud.google.com/**
2. Sign in with your Google account

---

## Step 2: Create a New Project

1. Click the **project dropdown** at the top (next to "Google Cloud")
2. Click **"NEW PROJECT"**
3. Enter project details:
   - **Project name**: `Study Planner` (or any name you prefer)
   - **Organization**: Leave as default
4. Click **"CREATE"**
5. Wait for the project to be created (few seconds)
6. Select your new project from the dropdown

---

## Step 3: Enable Google Calendar API

1. In the left sidebar, go to: **APIs & Services** → **Library**
   - Or use the search bar at the top: search "API Library"
2. Search for: **"Google Calendar API"**
3. Click on **"Google Calendar API"** in the results
4. Click the blue **"ENABLE"** button
5. Wait for it to enable (few seconds)

---

## Step 4: Configure OAuth Consent Screen

1. Go to: **APIs & Services** → **OAuth consent screen**
2. Choose **"External"** as User Type
3. Click **"CREATE"**
4. Fill in the required fields:
   - **App name**: `Study Planner`
   - **User support email**: Your email
   - **Developer contact**: Your email
5. Click **"SAVE AND CONTINUE"**
6. On the **Scopes** page: Click **"SAVE AND CONTINUE"** (no changes needed)
7. On the **Test users** page: Click **"SAVE AND CONTINUE"** (no changes needed)
8. Click **"BACK TO DASHBOARD"**

---

## Step 5: Create OAuth Credentials

1. Go to: **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"OAuth client ID"**
4. If prompted to configure consent screen, go back to Step 4
5. Configure the OAuth client:
   - **Application type**: Select **"Desktop app"**
   - **Name**: `Study Planner Desktop`
6. Click **"CREATE"**
7. A popup will appear with your credentials

---

## Step 6: Download Credentials

1. In the popup, click **"DOWNLOAD JSON"**
   - Or click the download icon (⬇) next to your newly created OAuth client in the credentials list
2. The file will be named something like:
   ```
   client_secret_XXXXX.apps.googleusercontent.com.json
   ```
3. **Rename** this file to: `credentials.json`
4. **Move** it to your project folder:
   ```
   c:\Users\MRUNMAYEE\Project_1\credentials.json
   ```

---

## Step 7: Verify Setup

Your `credentials.json` should look like this:

```json
{
  "installed": {
    "client_id": "XXXXX.apps.googleusercontent.com",
    "project_id": "study-planner-XXXXX",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "XXXXX",
    "redirect_uris": ["http://localhost"]
  }
}
```

---

## Step 8: First Run - Authentication

Now run your study planner:

```powershell
cd c:\Users\MRUNMAYEE\Project_1
python main.py
```

**What will happen:**
1. A browser window will **automatically open**
2. Google will ask you to **sign in** (if not already)
3. You'll see: "Study Planner wants to access your Google Calendar"
4. Click **"Allow"**
5. Browser will show: "The authentication flow has completed"
6. Close the browser and return to terminal

**After first authentication:**
- Token saved to `token.json`
- Future runs won't require browser authentication
- Token refreshes automatically when expired

---

## Step 9: Test Calendar Integration

Create a test goal and plan:

```powershell
python main.py
```

1. Select **"1. Create New Goal"**
2. Enter your Cloud Computing goal details
3. Select **"3. Create Daily Plan"**
4. Check your Google Calendar - events should appear!

---

## Troubleshooting

### Browser doesn't open
- Check if `credentials.json` is in the correct location
- Ensure file is valid JSON (not corrupted)

### "Access blocked" error
- Go back to OAuth consent screen
- Click "PUBLISH APP" (or add yourself as test user)

### "redirect_uri_mismatch" error
- In Google Cloud Console → Credentials
- Edit your OAuth client
- Add `http://localhost` to authorized redirect URIs

### Permission denied
- Re-run authentication
- Delete `token.json` and run again

---

## Security Notes

⚠️ **Keep these files private:**
- `credentials.json` - Contains your OAuth client secret
- `token.json` - Contains your access token

✅ **Already in .gitignore:**
```
credentials.json
token.json
```

Never share these files or commit them to git!

---

## Next Steps

Once setup is complete:
1. ✅ Test with `python main.py`
2. ✅ Test calendar agent: `python calendar_agent.py < example_tasks.json`
3. ✅ Check Google Calendar for created events
4. ✅ Start your 21-day Cloud Computing study plan!
