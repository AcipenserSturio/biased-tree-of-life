from itertools import pairwise
import json
from pathlib import Path

from .api import get_sheet, check_sheet
from .node import Node

class Tree:
    def __init__(self):
        self.nodes = {}
        self.root = None

    def add(self, node_dict):

        # check if already exists
        node_id = node_dict["node_id"]
        if self.get(node_id):
            return

        # create node
        node = Node(node_dict)

        # check if root
        if not self.nodes:
            self.root = node

        # save to nodes
        self.nodes[node_id] = node


    def get(self, node_id):
        return self.nodes.get(node_id)


    def tie(self, parent_id, child_id):
        parent = self.get(parent_id)
        child = self.get(child_id)

        child.parent = parent
        parent.children.add(child)

    def prune(self):
        # use copy to avoid runtime errors related to changing dict during iteration
        for node in self.nodes.copy().values():
            # don't prune notable nodes
            if node.is_notable():
                continue

            child = [*node.children][0]
            parent = node.parent

            self.tie(parent.id, child.id)

            parent.children.remove(node)
            del self.nodes[node.id]



def get_tree():
    tree = Tree()

    for path in (Path(".") / "cache" / "opentree").iterdir():
        with open(path) as f:
            data = json.load(f)

            # goes from cellular organisms to current node inclusively
            lineage = list(reversed([data, *data["lineage"]]))

            # add root
            tree.add(lineage[0])
            # add lineage
            for parent, node in pairwise(lineage):
                tree.add(node)
                tree.tie(parent["node_id"], node["node_id"])
    return tree


def enrich_tree(tree):
    for common_name, count, link, scientific_name, ott in get_sheet():
        if not ott:
            continue

        tree.get(f"ott{ott}").common_name = common_name
        tree.get(f"ott{ott}").count += int(count)

