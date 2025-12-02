# Azure Deployment Guide for Calibr8

This guide walks you through deploying the Calibr8 Django application to Azure App Service.

## Prerequisites

- Azure account with an active subscription
- Azure CLI installed (`az` command)
- Git repository initialized

## Quick Deploy Steps

### 1. Login to Azure

```bash
az login
```

### 2. Create a Resource Group

```bash
az group create --name calibr8-rg --location eastus
```

### 3. Create PostgreSQL Database (Optional but recommended for production)

```bash
# Create PostgreSQL server
az postgres flexible-server create \
  --resource-group calibr8-rg \
  --name calibr8-db-server \
  --location eastus \
  --admin-user calibr8admin \
  --admin-password <YourStrongPassword> \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 14

# Create database
az postgres flexible-server db create \
  --resource-group calibr8-rg \
  --server-name calibr8-db-server \
  --database-name calibr8db

# Configure firewall to allow Azure services
az postgres flexible-server firewall-rule create \
  --resource-group calibr8-rg \
  --name calibr8-db-server \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### 4. Create App Service Plan

```bash
az appservice plan create \
  --name calibr8-plan \
  --resource-group calibr8-rg \
  --sku B1 \
  --is-linux
```

### 5. Create Web App

```bash
az webapp create \
  --resource-group calibr8-rg \
  --plan calibr8-plan \
  --name calibr8-app \
  --runtime "PYTHON:3.13" \
  --startup-file startup.sh
```

### 6. Configure Environment Variables

```bash
# Django secret key (generate a new one for production!)
az webapp config appsettings set \
  --resource-group calibr8-rg \
  --name calibr8-app \
  --settings SECRET_KEY="<your-new-secret-key-here>"

# Debug mode (set to False for production)
az webapp config appsettings set \
  --resource-group calibr8-rg \
  --name calibr8-app \
  --settings DEBUG="False"

# Allowed hosts
az webapp config appsettings set \
  --resource-group calibr8-rg \
  --name calibr8-app \
  --settings ALLOWED_HOSTS="calibr8-app.azurewebsites.net,*.azurewebsites.net"

# Gemini API key
az webapp config appsettings set \
  --resource-group calibr8-rg \
  --name calibr8-app \
  --settings GEMINI_API_KEY="AIzaSyBTLcl669_TpBJxsgyZ9VDSoLcfccxqE_s"

# PostgreSQL configuration (if using Azure PostgreSQL)
az webapp config appsettings set \
  --resource-group calibr8-rg \
  --name calibr8-app \
  --settings \
    AZURE_POSTGRESQL_HOST="calibr8-db-server.postgres.database.azure.com" \
    AZURE_POSTGRESQL_NAME="calibr8db" \
    AZURE_POSTGRESQL_USER="calibr8admin" \
    AZURE_POSTGRESQL_PASSWORD="<YourStrongPassword>"
```

### 7. Configure Deployment from Local Git

```bash
# Set up local git deployment
az webapp deployment source config-local-git \
  --resource-group calibr8-rg \
  --name calibr8-app

# This will output a Git URL like:
# https://<deployment-username>@calibr8-app.scm.azurewebsites.net/calibr8-app.git
```

### 8. Deploy Your Code

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for Azure deployment"

# Add Azure as a remote (use the URL from step 7)
git remote add azure <git-url-from-step-7>

# Push to Azure
git push azure main
```

### 9. Verify Deployment

```bash
# Browse to your app
az webapp browse --resource-group calibr8-rg --name calibr8-app

# Check logs if there are issues
az webapp log tail --resource-group calibr8-rg --name calibr8-app
```

Your app should now be accessible at: `https://calibr8-app.azurewebsites.net`

## Environment Variables Summary

The following environment variables are configured in your `.env` file locally and should be set in Azure App Service settings:

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |
| `DEBUG` | Debug mode | `False` for production |
| `ALLOWED_HOSTS` | Allowed host names | `calibr8-app.azurewebsites.net,*.azurewebsites.net` |
| `GEMINI_API_KEY` | Google Gemini API key | `AIzaSyBTLcl669_TpBJxsgyZ9VDSoLcfccxqE_s` |
| `AZURE_POSTGRESQL_HOST` | PostgreSQL host | `calibr8-db-server.postgres.database.azure.com` |
| `AZURE_POSTGRESQL_NAME` | Database name | `calibr8db` |
| `AZURE_POSTGRESQL_USER` | Database user | `calibr8admin` |
| `AZURE_POSTGRESQL_PASSWORD` | Database password | Your chosen password |

## Alternative: Deploy Without PostgreSQL (SQLite)

If you want to use SQLite for testing (not recommended for production):

1. Skip step 3 (PostgreSQL creation)
2. Don't set the `AZURE_POSTGRESQL_*` environment variables
3. The app will use SQLite by default

**Note**: SQLite files are ephemeral on Azure App Service and will be reset on app restarts.

## Troubleshooting

### Check Application Logs

```bash
az webapp log tail --resource-group calibr8-rg --name calibr8-app
```

### SSH into the Container

```bash
az webapp ssh --resource-group calibr8-rg --name calibr8-app
```

### Common Issues

1. **Static files not loading**: Run `python manage.py collectstatic` (handled by startup.sh)
2. **Database connection errors**: Verify PostgreSQL environment variables
3. **Import errors**: Ensure all dependencies are in `requirements.txt`
4. **Port errors**: Azure sets the PORT environment variable automatically

## Updating Your Deployment

After making changes to your code:

```bash
git add .
git commit -m "Description of changes"
git push azure main
```

## Clean Up Resources

To delete all Azure resources and stop billing:

```bash
az group delete --name calibr8-rg --yes --no-wait
```

## Security Recommendations

1. Generate a new `SECRET_KEY` for production (don't use the development one)
2. Set `DEBUG=False` in production
3. Use strong passwords for PostgreSQL
4. Regularly rotate API keys
5. Enable HTTPS only
6. Set up proper authentication for your API endpoints

## Next Steps

- Configure a custom domain
- Set up SSL/TLS certificates (free with Azure)
- Enable Application Insights for monitoring
- Set up CI/CD with GitHub Actions or Azure DevOps
- Configure backup policies for PostgreSQL
