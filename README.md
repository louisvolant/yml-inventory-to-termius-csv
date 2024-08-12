# Ansible YAML Inventory to Termius CSV Import
Convert YML Inventory (specifically Ansible ones) to Termius CSV
This script will also convert all IPs to their DNS name.

## Requirements

1. First install the required packages

No package needed, only Python3

2. Get yml inventories and execute the script

- Copy the inventories .yml in the same folder as the script

- Then execute the script using : 
  - ```python yamltocsv.py -i prod-inventory.yml -o output_prod-inventory.csv```
  
  - ```python yamltocsv.py -i staging-inventory.yml -o output_staging-inventory.csv```

3. Nota bene

As of now, Termius communicates the example input file is like the following : ```termius_import_example.csv```

If it was meant to evolve, then please inform me :)