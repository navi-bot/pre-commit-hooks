#!/bin/bash

# URL of the remote .gitleaks.toml file
CONFIG_URL="https://raw.githubusercontent.com/navi-bot/pre-commit-hooks/main/.gitleaks.toml"
# Local path to store the downloaded config file
CONFIG_PATH="$HOME/.git-template/.gitleaks.toml"
# Temporary path for the new download
TEMP_CONFIG_PATH="$HOME/.git-template/.gitleaks_temp.toml"

# Download the config file to a temporary location
echo "Downloading gitleaks config..."
curl -s -o "$TEMP_CONFIG_PATH" "$CONFIG_URL"

# Check if the download was successful
if [ -f "$TEMP_CONFIG_PATH" ]; then
    # Compare the downloaded file with the existing configuration
    if [ -f "$CONFIG_PATH" ]; then
        # Check if there are differences
        if diff "$CONFIG_PATH" "$TEMP_CONFIG_PATH" > /dev/null; then
            echo "No changes in the configuration. Not updating the file."
            # Remove the temporary file if there are no changes
            rm "$TEMP_CONFIG_PATH"
        else
            echo "Configuration has changed. Updating the file..."
            # Replace the old configuration file with the new one
            mv "$TEMP_CONFIG_PATH" "$CONFIG_PATH"
        fi
    else
        echo "Configuration file does not exist. Creating new file..."
        # Move the new configuration file to the appropriate location
        mv "$TEMP_CONFIG_PATH" "$CONFIG_PATH"
    fi
    
    # Now run gitleaks with the updated/new config file
    echo "Running gitleaks..."
    gitleaks detect --verbose --config="$CONFIG_PATH" --no-git
else
    echo "Failed to download the config file."
fi