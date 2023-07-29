
import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components
from pyvis import network as net
from IPython.core.display import display, HTML

# Set page title
st.set_page_config(page_title="Genetic Network Visualizer")

# Add a title and an explanatory paragraph
st.title("🔬 Genetic Network Visualizer 🧬")
st.markdown("""
This app visualizes genetic interactions based on selected nodes and edge types. 
You can select the source nodes (genes), target nodes (genes), and types of interactions (edge types) you're interested in. 
The app will then generate an interactive network graph that visualizes these interactions.

This application uses data from Hetionet, a network that encodes biology in a graph where nodes represent biological entities and edges represent the relationships between them.
The network is visualized using PyVis, an interactive network visualization library in Python. 
The app is built with Streamlit, a fast and easy way to build data apps in Python.

Please select your options in the sidebar 👉 to start exploring!
""")

# Read your data
df = pd.read_excel('data/filtered_edges.xlsx')
required_columns = [
    'kind_edge', 'direction', 'data.source_edge', 'data.unbiased', 'data.sources', 'data.method', 'data.subtypes',
    'source_type', 'target_type', 'name_source_node', 'data.description_source_node', 'name_target_node', 'data.description_target_node'
]
# Assuming that your dataframe is named df
df = df[required_columns] # replace "your_data.csv" with the path to your csv file

# Convert types to strings for multiselect
df['source_type'] = df['source_type'].astype(str)
df['target_type'] = df['target_type'].astype(str)

# Create multi-select for source nodes
source_nodes = st.sidebar.multiselect(
    '🧬 Select source nodes', options=list(df['name_source_node'].unique()), default=['SLC5A5'])

# Create multi-select for target nodes
#target_nodes = st.sidebar.multiselect(
#   '🧪 Select target nodes', options=list(df['name_target_node'].unique()), default=['None'])
#
# Create multi-select for edge types
edge_types = st.sidebar.multiselect(
    '🔗 Select edge types', options=list(df['kind_edge'].unique()), default='participates')

# Filter dataframe based on user selection
if source_nodes:
    df = df[df['name_source_node'].isin(source_nodes)]
#if target_nodes:
#    df = df[df['name_target_node'].isin(target_nodes)]
if edge_types:
    df = df[df['kind_edge'].isin(edge_types)]




# Create a network graph
g = net.Network(height='750px', width='100%', bgcolor='#00000', font_color='black')

# Set the physics layout of the network
g.barnes_hut()

sources = df['name_source_node']
targets = df['name_target_node']
weights = df['kind_edge']

edge_data = zip(sources, targets, weights)

for e in edge_data:
    src = e[0]
    dst = e[1]
    w = e[2]

    g.add_node(src, src, title=src,physics = False)
    g.add_node(dst, dst, title=dst,physics = False)
    g.add_edge(src, dst, value=w)

neighbor_map = g.get_adj_list()

for node in g.nodes:
    node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
    node["value"] = len(neighbor_map[node["id"]])




g.save_graph('gene_net_graph.html')
HtmlFile = open('gene_net_graph.html', 'r', encoding='utf-8')
# Load HTML file in HTML component for display on Streamlit page
components.html(HtmlFile.read(), height=1000,width=1000)

