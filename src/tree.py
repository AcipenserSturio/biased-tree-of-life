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

    def prune(self, stage):

        """
        stages:
        - 0: only prune unnamed clades.
        - 1: prune unnamed clades that are replaceable with named taxa.
        - 2: prune named taxa.
        """

        # use copy to avoid runtime errors related to changing dict during iteration
        for node in self.nodes.copy().values():

            # don't prune specially added nodes
            if node.common_name:
                continue
            # don't prune roots
            if not node.parent:
                continue

            if stage == 0:
                # don't prune points of divergence
                # don't prune named taxa
                if len(node.children) != 1 or node.sci_name:
                    continue
                self.remove(node)

            if stage == 1:
                # if a parent is named and is practically identical to node:
                if node.parent.sci_name and not node.sci_name and len(node.parent.children) == 1:
                    self.remove(node)

            if stage == 2:
                # don't prune points of divergence
                if len(node.children) != 1:
                    continue

                self.remove(node)

    def remove(self, node):
        for child in node.children:
            self.tie(node.parent.id, child.id)

        node.parent.children.remove(node)
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
        # tree.get(f"ott{ott}").count += int(count)
        tree.get(f"ott{ott}").count = 1

