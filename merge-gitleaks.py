import toml
import requests

def fetch_external_config(url):
    """Fetch the external gitleaks.toml configuration."""
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response
    return toml.loads(response.text)

def load_local_config(path):
    """Load the local .gitleaks.toml configuration."""
    with open(path, 'r') as file:
        return toml.load(file)

def merge_configs(local_config, external_config):
    """Merge external config into local config based on rule IDs."""
    local_rules = {rule['id']: rule for rule in local_config.get('rules', [])}
    external_rules = {rule['id']: rule for rule in external_config.get('rules', [])}

    # Update or add external rules that don't conflict with custom local rule IDs
    for rule_id, rule in external_rules.items():
        if rule_id not in local_rules:
            local_rules[rule_id] = rule

    # Convert the merged rules back into a list as expected by the toml format
    merged_rules = list(local_rules.values())

    # Replace the local config rules with the merged rules
    local_config['rules'] = merged_rules
    return local_config

def save_config(config, path):
    """Save the merged configuration back to .gitleaks.toml."""
    with open(path, 'w') as file:
        toml.dump(config, file)

if __name__ == '__main__':
    external_url = "https://raw.githubusercontent.com/gitleaks/gitleaks/master/config/gitleaks.toml"
    local_path = ".gitleaks.toml"
    
    external_config = fetch_external_config(external_url)
    local_config = load_local_config(local_path)
    merged_config = merge_configs(local_config, external_config)
    save_config(merged_config, local_path)
