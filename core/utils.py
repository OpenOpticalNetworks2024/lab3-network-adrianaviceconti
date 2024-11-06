# Use this file to define your generic methods, e.g. for plots

import matplotlib.pyplot as plt

def plot_network(nodes, lines):
    fig, ax = plt.subplots(figsize=(12, 10))
    for node_label, node in nodes.items():
        x, y = node.position
        ax.plot(x, y, 'o', label = node_label, markersize = 26, color = 'lightgreen', markeredgewidth = 1)
        ax.text(x, y, f'{node_label}', fontsize = 26, ha = 'center', va = 'center')

    for line_label, line in lines.items():
        node_labels = [line_label[0], line_label[1]]
        x_values = [nodes[node_labels[0]].position[0], nodes[node_labels[1]].position[0]]
        y_values = [nodes[node_labels[0]].position[1], nodes[node_labels[1]].position[1]]
        ax.plot(x_values, y_values, color = 'lightsteelblue', linewidth = 3)

    ax.set_xlabel("\nX position (m)", fontsize = 18)
    ax.set_ylabel("Y position (m)\n", fontsize = 18)
    ax.set_title("Network\n", fontsize = 22)
    plt.show()