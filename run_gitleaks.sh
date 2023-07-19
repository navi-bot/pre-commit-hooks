#!/bin/bash

# Set the config file path
CONFIG_PATH="$HOME/.git-template/.gitleaks.toml"

# Check if the config file exists, and run gitleaks if it does
if [ -f $CONFIG_PATH ]; then
    echo "Running gitleaks..."
    gitleaks protect --config=$CONFIG_PATH --staged -v
fi