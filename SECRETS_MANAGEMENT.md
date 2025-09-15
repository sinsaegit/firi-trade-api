# Secrets Management Guide

## Setting up your API credentials

This project uses environment variables to securely manage API credentials. **Never commit your actual API keys to version control!**

### Local Development

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your actual Firi API credentials:
   ```
   API_KEY=your_actual_api_key
   SECRET_KEY=your_actual_secret_key
   CLIENT_ID=your_actual_client_id
   ```

3. The `.env` file is already in `.gitignore` and will not be committed to version control.

### GitHub Actions CI/CD

To run tests and deployments in GitHub Actions, you need to add your secrets to the repository settings:

1. Go to your GitHub repository
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret** and add each of the following secrets:

   | Secret Name | Description |
   |-------------|-------------|
   | `FIRI_API_KEY` | Your Firi API Key |
   | `FIRI_SECRET_KEY` | Your Firi Secret Key |
   | `FIRI_CLIENT_ID` | Your Firi Client ID |

5. The CI workflow in `.github/workflows/ci.yml` will automatically use these secrets when running tests.

### Security Best Practices

- ✅ **DO**: Use environment variables for all sensitive data
- ✅ **DO**: Add `.env*` to your `.gitignore` file
- ✅ **DO**: Use GitHub repository secrets for CI/CD
- ✅ **DO**: Regularly rotate your API keys
- ❌ **DON'T**: Commit API keys directly in code
- ❌ **DON'T**: Share your `.env` file with others
- ❌ **DON'T**: Include secrets in commit messages or code comments

### Checking for Exposed Secrets

To check if any secrets were accidentally committed to git history:

```bash
# Search for potential API keys in commit history
git log --all --full-history -p | grep -i "api_key\|secret_key\|client_id"

# Search for .env files in history
git log --all --full-history -- "*.env*"

# Use tools like git-secrets or truffleHog for comprehensive scanning
```

If you find exposed secrets:
1. **Immediately revoke/rotate** the exposed credentials
2. Consider using `git filter-branch` or BFG Repo-Cleaner to remove them from history
3. Update your secrets in GitHub repository settings

### Getting Firi API Credentials

1. Log into your Firi account
2. Go to account settings or API section
3. Generate new API credentials if needed
4. Copy the API Key, Secret Key, and Client ID to your `.env` file

For more information, consult the [Firi API documentation](https://developers.firi.com/).