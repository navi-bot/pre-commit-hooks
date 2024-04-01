import toml
import requests

def fetch_external_config(url):
    """Fetch the external gitleaks.toml configuration."""
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response
    return response.text

def merge_configs(local_config_path, external_config_toml):
    with open(local_config_path, 'r') as file:
        local_config = toml.load(file)
    
    external_config = toml.loads(external_config_toml)

    local_rules_ids = set(rule['id'] for rule in local_config.get('rules', []))
    external_rules = external_config.get('rules', [])

    for ext_rule in external_rules:
        if ext_rule['id'] not in local_rules_ids:
            # Directly append the entire external rule as is, ensuring all fields are copied
            local_config.setdefault('rules', []).append(ext_rule)

    with open(local_config_path, 'w') as file:
        toml.dump(local_config, file)

    print("Updated local configuration with new rules from external configuration.")

if __name__ == '__main__':
    external_config_url = "https://raw.githubusercontent.com/gitleaks/gitleaks/master/config/gitleaks.toml"
    local_config_path = ".gitleaks.toml"
    
    external_config_toml = fetch_external_config(external_config_url)
    merge_configs(local_config_path, external_config_toml)
