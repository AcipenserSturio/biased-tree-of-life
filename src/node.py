class Node:
    def __init__(self, node_dict):
        self.id = node_dict["node_id"]
        self.sci_name = "" if "taxon" not in node_dict else node_dict["taxon"]["name"]

        # set by tree
        self.parent = None
        self.children = set()

        # set by enrich_tree
        self.common_name = None
        self.count = 0

    def __repr__(self):
        return f"Node({self.get_name()} [{self.id}])"

    def get_name(self):
        if self.common_name:
            return self.common_name
        if self.sci_name:
            return self.sci_name
        return ""

    def get_colour(self):
        if self.common_name:
            return (255, 255, 42)
        if self.sci_name:
            return (200, 200, 255)
        return (180, 180, 180)

    def get_count(self):
        return self.count + sum(map(Node.get_count, self.children))

    def get_children(self):
        return sorted(self.children, key=Node.get_count, reverse=True)

    def traverse_children(self):
        recursion = list(map(Node.traverse_children, self.get_children()))
        if self.common_name:
            recursion.append([self.common_name, self.count])
        return recursion
