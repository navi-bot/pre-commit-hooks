import toml
import requests
import tomlkit

def fetch_external_config(url):
    """Fetch the external gitleaks.toml configuration."""
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response
    return response.text

def parse_toml_with_tomlkit(toml_content):
    return tomlkit.parse(toml_content)

def deep_merge_rules(local_rule, external_rule):
    """Manually merges attributes from external_rule into local_rule."""
    for key, value in external_rule.items():
        # If the attribute is a list and exists in both, extend the local_rule's list
        if isinstance(value, list) and key in local_rule:
            local_rule[key].extend(value)
        else:
            # Otherwise, simply update or add the attribute to local_rule
            local_rule[key] = value

def merge_configs(local_config_path, external_config_toml):
    with open(local_config_path, 'r') as file:
        local_config = toml.load(file)

    external_config = parse_toml_with_tomlkit(external_config_toml)

    # Convert local rules to a dict for easier id-based access
    local_rules = {rule['id']: rule for rule in local_config.get('rules', [])}
    for ext_rule in external_config.get('rules', []):
        if ext_rule['id'] in local_rules:
            # If the rule exists, deep merge to ensure all sub-properties are updated
            deep_merge_rules(local_rules[ext_rule['id']], ext_rule)
        else:
            # If the rule is new, add it directly
            local_config.setdefault('rules', []).append(ext_rule)

    with open(local_config_path, 'w') as file:
        file.write(tomlkit.dumps(local_config))

if __name__ == '__main__':
    external_config_url = "https://raw.githubusercontent.com/gitleaks/gitleaks/master/config/gitleaks.toml"
    local_config_path = ".gitleaks.toml"
    
    external_config_toml = fetch_external_config(external_config_url)
    merge_configs(local_config_path, external_config_toml)
