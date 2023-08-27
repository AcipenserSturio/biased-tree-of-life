from pathlib import Path
import json
from itertools import pairwise

from src.tree import get_tree, enrich_tree
from src.api import get_sheet, check_sheet
from src.plotter import plot


if __name__ == "__main__":
    check_sheet()
    tree = get_tree()
    enrich_tree(tree)
    tree.prune()
    plot(tree)
