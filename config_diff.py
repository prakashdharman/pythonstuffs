import configparser
import os

def read_splunk_conf(file_path):
    """Reads a Splunk configuration file and returns a dictionary with stanzas and key-value pairs."""
    config = configparser.ConfigParser()
    config.optionxform = str  # Maintain case sensitivity for keys
    config.read(file_path)
    conf_dict = {section: dict(config.items(section)) for section in config.sections()}
    return conf_dict

def compare_and_report_differences(current_conf, backup_conf):
    """Compares the current and backup configuration dictionaries and returns differences and merged dictionary."""
    differences = {}
    merged_conf = current_conf.copy()

    for stanza, settings in backup_conf.items():
        if stanza not in current_conf:
            # Stanza is missing in the current config, record the difference
            differences[stanza] = {'missing_stanza': True, 'missing_keys': settings}
            merged_conf[stanza] = settings
        else:
            # Stanza exists, check for missing keys
            missing_keys = {}
            for key, value in settings.items():
                if key not in current_conf[stanza]:
                    missing_keys[key] = value
            if missing_keys:
                differences[stanza] = {'missing_stanza': False, 'missing_keys': missing_keys}
                merged_conf[stanza].update(missing_keys)

    return differences, merged_conf

def write_merged_conf(file_path, merged_conf):
    """Writes the merged configuration back to a file."""
    config = configparser.ConfigParser()
    config.optionxform = str  # Maintain case sensitivity for keys

    for stanza, settings in merged_conf.items():
        config[stanza] = settings

    with open(file_path, 'w') as configfile:
        config.write(configfile)

def list_and_show_differences(file_path, differences):
    """Lists files with deviations and shows the differences."""
    if not differences:
        print(f"No differences found in {file_path}.")
    else:
        print(f"\nDifferences found in: {file_path}")
        for stanza, diff in differences.items():
            print(f"\nStanza: [{stanza}]")
            if diff['missing_stanza']:
                print("  Missing stanza entirely in the current config. Content from backup:")
                for key, value in diff['missing_keys'].items():
                    print(f"    {key} = {value}")
            else:
                print("  Missing keys in the current config:")
                for key, value in diff['missing_keys'].items():
                    print(f"    {key} = {value}")

def process_directory(current_dir, backup_dir, output_dir):
    """Processes all .conf files in the current and backup directories, compares, merges, and reports differences."""
    for root, _, files in os.walk(backup_dir):
        for file in files:
            if file.endswith(".conf"):
                # Determine corresponding file paths
                backup_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(backup_file_path, backup_dir)
                current_file_path = os.path.join(current_dir, relative_path)
                output_file_path = os.path.join(output_dir, relative_path)

                # Ensure the output directory exists
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                # Read and compare configurations
                backup_conf = read_splunk_conf(backup_file_path)
                current_conf = read_splunk_conf(current_file_path) if os.path.exists(current_file_path) else {}

                differences, merged_conf = compare_and_report_differences(current_conf, backup_conf)

                # List and show differences
                list_and_show_differences(current_file_path, differences)

                # Write the merged configuration back to a file
                write_merged_conf(output_file_path, merged_conf)

                print(f"Merged configuration written to {output_file_path}")

# Paths to your current and backup app directories
current_app_dir = "path/to/current/apps"
backup_app_dir = "path/to/backup/apps"
output_app_dir = "path/to/output/apps"  # Output directory for merged files

# Process all .conf files in the app directories
process_directory(current_app_dir, backup_app_dir, output_app_dir)

print("Comparison and merge process completed.")
