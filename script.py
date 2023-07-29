import pandas as pd

# Read the selected genes data
df_gene_selected = pd.read_csv('/Users/paritoshmacmini/Documents/teal_code/GPT_Omics_Analysis/new_data/gene_selected.tsv', sep='\t')

# Read the selected indications data
df_selection = pd.read_excel('/Users/paritoshmacmini/Documents/teal_code/GPT_Omics_Analysis/data/v1 Indication list_CNS and Neuroimmune_June 12 2023.xlsx')

genes_of_interest = df_gene_selected['Gene name'].tolist()
indications_of_interest = df_selection['Indication'].tolist()
import requests
import json
import bz2
import io

# Download the Hetionet data
url = "https://github.com/hetio/hetionet/raw/main/hetnet/json/hetionet-v1.0.json.bz2"
response = requests.get(url)

# Decompress the data
decompressed = bz2.decompress(response.content)
data = json.loads(decompressed.decode())

# Filter nodes
filtered_nodes = [node for node in data['nodes'] if node['name'] in genes_of_interest or node['name'] in indications_of_interest]

# Filter edges
filtered_edges = [edge for edge in data['edges'] if edge['source_id'][1] in genes_of_interest or edge['target_id'][1] in indications_of_interest]


# Download the Metagraph data
url = "https://github.com/hetio/hetionet/raw/main/hetnet/json/hetionet-v1.0-metagraph.json"
response = requests.get(url)

# Parse the JSON data
meta_data = response.json()

# Get the mapping from abbreviations to full forms
abbrev_to_kind = {v: k for k, v in meta_data['kind_to_abbrev'].items()}
# Replace the relationship codes with full forms in the filtered_edges
for edge in filtered_edges:
    edge['kind'] = abbrev_to_kind[edge['kind']]
    # Dump filtered genes data to JSON
with open('filtered_genes.json', 'w') as f:
    json.dump([node for node in filtered_nodes if node['kind'] == 'Gene'], f)

# Dump filtered indications data to JSON
with open('filtered_indications.json', 'w') as f:
    json.dump([node for node in filtered_nodes if node['kind'] == 'Disease'], f)  # Assuming indications are of kind 'Disease'

# Dump filtered and decoded edges data to JSON
with open('filtered_edges.json', 'w') as f:
    json.dump(filtered_edges, f)



#trial 2 

# Convert to lowercase and perform other normalization if needed
genes_of_interest = df_gene_selected['Gene name'].str.lower().tolist()
indications_of_interest = df_selection['Indication'].str.lower().tolist()


# Filter nodes
filtered_nodes = [node for node in data['nodes'] if node['name'].lower() in genes_of_interest or node['name'].lower() in indications_of_interest]

# Filter edges
filtered_edges = [edge for edge in data['edges'] if edge['source_id'][1] in genes_of_interest or edge['target_id'][1] in indications_of_interest]

# Download the Metagraph data
url_meta = "https://github.com/hetio/hetionet/raw/main/hetnet/json/hetionet-v1.0-metagraph.json"
response_meta = requests.get(url_meta)

# Parse the JSON data
meta_data = response_meta.json()

# Get the mapping from abbreviations to full forms
abbrev_to_kind = {v: k for k, v in meta_data['kind_to_abbrev'].items()}

# Replace the relationship codes with full forms in the filtered_edges
for edge in filtered_edges:
    edge['kind'] = abbrev_to_kind[edge['kind']]

# Create DataFrame for filtered edges
df_edges = pd.DataFrame(filtered_edges)

# Save to CSV
df_edges.to_csv('filtered_edges.csv', index=False)
