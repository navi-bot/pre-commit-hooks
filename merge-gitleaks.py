import toml
import requests

def fetch_external_config(url):
    """Fetch the external gitleaks.toml configuration."""
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response
    return toml.loads(response.text)

def merge_configs(local_config_path, external_config_content):
    # Load the local configuration
    with open(local_config_path, 'r') as file:
        local_config = toml.load(file)
    
    # Parse the external configuration
    external_config = toml.loads(external_config_content)

    local_rules = {rule['id']: rule for rule in local_config.get('rules', [])}
    external_rules = external_config.get('rules', [])

    # Check each external rule to see if it exists in the local rules by id
    for ext_rule in external_rules:
        if ext_rule['id'] not in local_rules:
            # If the rule does not exist in the local config, add it
            local_config['rules'].append(ext_rule)

    # Save the merged configuration back to the local .gitleaks.toml file
    with open(local_config_path, 'w') as file:
        toml.dump(local_config, file)

    print(f"Updated {local_config_path} with new rules from the external configuration.")

if __name__ == '__main__':
    external_config_url = "https://raw.githubusercontent.com/gitleaks/gitleaks/master/config/gitleaks.toml"
    local_config_path = ".gitleaks.toml"
    
    external_config_content = fetch_external_config(external_config_url)
    local_config = load_local_config(local_path)
    merge_configs(local_config, external_config)
