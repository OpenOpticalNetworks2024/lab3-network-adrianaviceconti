import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from core.elements import Network, Signal_information
from core.science_utils import snr_db

# Exercise Lab3: Network

ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'


# Load the Network from the JSON file, connect nodes and lines in Network.
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file

network = Network(file_input)
network.connect()

signal_power = 1e-3 # 1 mW in Watts

results = []

node_labels = list(network.nodes.keys())
node_couples = [(node_labels[i], node_labels[j]) for i in range(len(node_labels)) for j in range(len(node_labels)) if i != j]

for node_couple in node_couples:
    start, end = node_couple[0], node_couple[1]
    paths = network.find_paths(start, end)

    for path in paths:
        signal_information = Signal_information(signal_power, path.copy())
        network.propagate(signal_information)

        snr_db_value = snr_db(signal_power, signal_information.noise_power)

        results.append({
            'Node couple': f"{start}->{end}",
            'Path': '->'.join(path),
            'Latency (s)': signal_information.latency,
            'Noise (W)': signal_information.noise_power,
            'SNR (dB)': snr_db_value
        })

df = pd.DataFrame(results)
output_path = ROOT / 'weighted_path.csv'
df.to_csv(output_path, index=False)

network.draw()