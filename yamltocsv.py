#yamltocsv.py

import yaml
import csv
import argparse
import logging
import socket

# README
# execute with
# python yamltocsv.py -i prod-inventory.yml -o output_prod-inventory.csv

LAST_GROUPS_TO_KEEP = 2
EXCLUDED_GROUPS = ['children','ansible']

def extract_hosts(data, parent_label='', groups=''):
    hosts = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'hosts':
                for host, details in value.items():
                    # Perform reverse DNS lookup
                    try:
                        domain_name = socket.gethostbyaddr(details.get('ansible_host', ''))[0]
                    except socket.herror:
                        # If reverse DNS lookup fails, use the IP address
                        domain_name = details.get('ansible_host', '')

                    hosts.append({
                        'Groups': groups.strip('/'),
                        'Label': host,
                        'Tags':'',
                        'Hostname/IP': domain_name,
                        'Protocol': 'ssh',
                        'Port': 22
                    })
            else:
                # Construct the new groups path, excluding "children"
                new_groups = groups + '/' + key if groups else key
                if key not in EXCLUDED_GROUPS :
                    hosts.extend(extract_hosts(value, key, new_groups))
                else:
                    hosts.extend(extract_hosts(value, parent_label, groups))
    return hosts

def clean_groups(group_str, quantity_to_keep):
    elements = group_str.split('/')

    last_elts = elements[-quantity_to_keep:]

    return '/'.join(last_elts)

def produce_csv(input_csv_file, input_hosts):
    # Write to the CSV file
    with open(input_csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Groups', 'Label', 'Tags', 'Hostname/IP', 'Protocol', 'Port'])
        writer.writeheader()
        for row in input_hosts:
            writer.writerow(row)

def yaml_to_csv(yaml_file, csv_file):
    # Read YAML file
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)

    # Log content of the YAML file
    logging.debug(f"Content of YAML file '{yaml_file}': {data}")

    # Extract hosts and ansible_host values
    hosts = extract_hosts(data)
    for host in hosts:
        host['Groups'] = clean_groups(host['Groups'], LAST_GROUPS_TO_KEEP)

    produce_csv(csv_file, hosts)

def main():
    parser = argparse.ArgumentParser(description='Convert a YAML file to CSV format.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input YAML file')
    parser.add_argument('-o', '--output', required=True, help='Path to the output CSV file')
    args = parser.parse_args()

    try:
        # Convert the YAML file to CSV
        yaml_to_csv(args.input, args.output)
    except Exception as e:
        logging.exception("An error occurred")

if __name__ == '__main__':
    ## Initialize logging before hitting main, in case we need extra debuggability
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    main()