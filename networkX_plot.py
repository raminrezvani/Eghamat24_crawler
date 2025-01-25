import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

# Parameters
num_nodes = 100  # Example: number of nodes in a subset of YelpChi for faster visualization

# Generating synthetic data for illustration
np.random.seed(42)  # For reproducibility

# Original adjacency matrix (sparse)
original_adj = np.random.rand(num_nodes, num_nodes)
original_adj = (original_adj + original_adj.T) / 2  # Make symmetric
original_adj[original_adj < 0.6] = 0  # Sparsify for visibility

# Reconstructed adjacency matrix (denser to show hidden dependencies)
reconstructed_adj = np.random.rand(num_nodes, num_nodes)
reconstructed_adj = (reconstructed_adj + reconstructed_adj.T) / 2
reconstructed_adj[reconstructed_adj < 0.4] = 0  # Slightly denser for reconstruction

# Temporal-spatial attention weights
attention_weights = np.random.rand(num_nodes, num_nodes)


# Visualization Functions

def visualize_graph_reconstruction(original_adj, reconstructed_adj):
    """ Visualize Original vs. Reconstructed Graph to show hidden dependencies. """
    G_original = nx.from_numpy_matrix(original_adj)
    G_reconstructed = nx.from_numpy_matrix(reconstructed_adj)

    plt.figure(figsize=(14, 6))

    # Original Graph
    plt.subplot(1, 2, 1)
    nx.draw(G_original, node_color='skyblue', edge_color='gray', with_labels=False)
    plt.title("Original Graph Structure")

    # Reconstructed Graph
    plt.subplot(1, 2, 2)
    nx.draw(G_reconstructed, node_color='salmon', edge_color='darkred', with_labels=False)
    plt.title("Reconstructed Graph with Hidden Dependencies")

    plt.show()


def visualize_attention_weights(attention_weights, title="Temporal-Spatial Attention Weights"):
    """Visualize Temporal-Spatial Attention Weights."""
    # Plot heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(attention_weights, cmap="YlGnBu", square=True)
    plt.title(title)
    plt.xlabel("Node")
    plt.ylabel("Node")
    plt.show()


# Visualize Graph Reconstruction Dependencies
visualize_graph_reconstruction(original_adj, reconstructed_adj)

# Visualize Temporal-Spatial Dependency via Attention Mechanism
visualize_attention_weights(attention_weights)
