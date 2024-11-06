import json
import math
import numpy as np
import matplotlib.pyplot as plt
from core.parameters import c_fiber
from core.utils import *
from typing import List, Tuple

class Signal_information(object):
    def __init__(self, signal_power: float, path: List[str]):
        self._signal_power = signal_power
        self._noise_power = 0.0
        self._latency = 0.0
        self._path = path

    @property
    def signal_power(self):
        return self._signal_power

    def update_signal_power(self, increment):
        self._signal_power += increment

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self, value):
        self._noise_power = value

    def update_noise_power(self, increment):
        self._noise_power += increment

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, value):
        self._latency = value

    def update_latency(self, increment):
        self._latency += increment

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        self._path = new_path

    def update_path(self):
        if self._path:
            self._path.pop(0)


class Node(object):
    def __init__(self, label: str, position: Tuple[float, float], connected_nodes: List[str]):
        self._label = label
        self._position = position
        self._connected_nodes = connected_nodes
        self._successive = {}

    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, value):
        self._successive = value

    def propagate(self, signal_information):
        signal_information.update_path()
        if signal_information.path:
            next_node_label = signal_information.path[0]
            if next_node_label in self._successive:
                self._successive[next_node_label].propagate(signal_information)


class Line(object):
    def __init__(self, label: str, length: float):
        self._label = label
        self._length = length
        self._successive = {}

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, value):
        self._successive = value

    def latency_generation(self) -> float:
        return self._length / c_fiber

    def noise_generation(self, signal_power: float) :
        return 1e-9 * signal_power * self._length

    def propagate(self, signal_information):
        signal_information.update_latency(self.latency_generation())
        signal_information.update_noise_power(self.noise_generation(signal_information.signal_power))
        if signal_information.path:
            next_node_label = signal_information.path[0]
            if next_node_label in self._successive:
                self._successive[next_node_label].propagate(signal_information)


class Network(object):
    def __init__(self, json_file:str):
        self._nodes = {}
        self._lines = {}
        with open(json_file, 'r') as file:
            data = json.load(file)

        for label, attrs in data.items():
            self._nodes[label] = Node(label, tuple(attrs["position"]), attrs["connected_nodes"])

        for label, node in self._nodes.items():
            for conn_label in node.connected_nodes:
                line_label = label + conn_label
                length = self.calculate_distance(node.position, self._nodes[conn_label].position)
                self._lines[line_label] = Line(line_label, length)

    @staticmethod
    def calculate_distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self):
        plot_network(self._nodes, self._lines)

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1: str, label2: str) -> List[List[str]]:
        def dfs(current_label, target_label, visited, path, all_paths):
            visited.add(current_label)
            path.append(current_label)
            if current_label == target_label:
                all_paths.append(path[:])
            else:
                for neighbor in self._nodes[current_label].connected_nodes:
                    if neighbor not in visited:
                        dfs(neighbor, target_label, visited, path, all_paths)
            path.pop()
            visited.remove(current_label)

        all_paths = []
        dfs(label1, label2, set(), [], all_paths)
        return all_paths

    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        for line in self._lines.values():
            node_labels = [line.label[0], line.label[1]]
            self._nodes[node_labels[0]].successive[node_labels[1]] = line
            line.successive[node_labels[1]] = self._nodes[node_labels[1]]

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        start_node_label = signal_information.path[0]
        if start_node_label in self._nodes:
            self._nodes[start_node_label].propagate(signal_information)