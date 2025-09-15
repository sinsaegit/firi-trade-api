# proof-of-trade-bot
Project for obtaining valuable experience with API development and basic communicative cryptography, specifically HMAC keys. 
This is an attempt to automate trading on Firi crpytocurrency stock exchange. Will it work? Probably not. But no one wins without trying.

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your Firi API credentials
4. Run the application: `python project/__main__.py`

## Security

This project uses environment variables to manage API credentials securely. See [SECRETS_MANAGEMENT.md](SECRETS_MANAGEMENT.md) for detailed instructions on:
- Setting up local environment variables
- Configuring GitHub Actions secrets
- Security best practices
- Checking for exposed secrets in git history

**⚠️ Never commit your API keys to version control!**
