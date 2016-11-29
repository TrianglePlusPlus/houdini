from queue import Queue


class RoyalTree:
    def __init__(self):
        self.root = RoyalTreeNode("__root__")
        self.nodes_list = {self.root}
        self.roles_to_nodes_map = {}

    @classmethod
    def build_from_json(cls, roles_dict):
        temp_tree = cls()
        roles_to_nodes_map = {}
        for role in roles_dict:
            # Generate all of the nodes without any parents
            temp_node = RoyalTreeNode(role, permissions=roles_dict[role]['permissions'])
            roles_to_nodes_map[role] = temp_node
        # Stitch the nodes together
        for role in roles_dict:
            if len(roles_dict[role]['parents']) == 0:
                roles_to_nodes_map[role].parents.add(temp_tree.root)
            for parent in roles_dict[role]['parents']:
                try:
                    roles_to_nodes_map[role].parents.add(roles_to_nodes_map[parent])
                except KeyError:
                    raise KeyError("A node was created with a parent that does not exist")
        temp_tree.nodes_list.update([roles_to_nodes_map[role] for role in roles_dict])
        temp_tree.roles_to_nodes_map = roles_to_nodes_map
        return temp_tree

    def get_permissions_for_role(self, role_slug):
        """
        Traverses the tree to find all of the permissions for the specified role
        Searches in the role's ancestors to accumulate additional permissions
        :param role_slug: The role-slug corresponding to the role for which permissions are desired
        :return: A set containing all of the permissions for the specified role
        """
        # First ensure that the role even exists
        if role_slug not in self.roles_to_nodes_map:
            raise KeyError("The role " + role_slug + " does not exist in the tree.")
        # It exists so get its permissions
        role_node = self.roles_to_nodes_map[role_slug]
        role_permissions = set(role_node.permissions)
        search_queue = Queue()
        searched_nodes = {role_node}
        # Enqueue every parent that isn't root
        for parent in role_node.parents:
            if parent != self.root:
                search_queue.put_nowait(parent)
        # Search up the tree and gather permissions
        while not search_queue.empty():
            search_node = search_queue.get()
            # Add its permissions to our list
            role_permissions.update(search_node.permissions)
            # Enqueue its parents
            for parent in search_node.parents:
                if parent != self.root and parent not in searched_nodes:
                    search_queue.put(parent)
        return role_permissions

    def add_role_from_node(self, role_node):
        """
        Adds a RoyalTreeNode to the tree
        :param role_node: The node to add to the tree
        :return:
        """
        if not isinstance(role_node, RoyalTreeNode):
            raise TypeError("The parameter `role_node` is not of type RoyalTreeNode")
        # Add them to the nodes list so we can prevent duplicate entries
        if role_node in self.nodes_list:
            raise KeyError("The node you are trying to add already exists in the tree.")
        else:
            self.nodes_list.add(role_node)
        if len(role_node.parents) == 0:
            # If it has no parents then add it to the root
            role_node.parents.add(self.root)


class RoyalTreeNode:
    def __init__(self, role, **kwargs):
        self.role = role
        self.permissions = set()
        """parents is a set of `RoyalTreeNode`s"""
        self.parents = set()
        if "permissions" in kwargs:
            self.permissions = set(kwargs["permissions"])
        if "parents" in kwargs:
            self.parents = set(kwargs["parents"])

    @property
    def parent_slugs(self):
        return [parent.role for parent in self.parents]

    def __repr__(self):
        return "RoyalTreeNode: " + self.role

    def __str__(self):
        string_representation = "ROLE: " + self.role + "\n"
        string_representation += "PERMISSIONS: " + " ".join([permission for permission in self.permissions]) + "\n"
        string_representation += "PARENTS: " + " ".join([parent.role for parent in self.parents])
        return string_representation

    def __hash__(self):
        return hash(repr(self))


if __name__ == "__main__":
    # Here's a test case to run and make sure this is minimally working
    # TODO: Delete this
    json = {"director": {"parents": [], "permissions": ["all"]},
            "director-it": {"parents": ["director"], "permissions": ["it-worker-bee", "it-all"]}}
    tree = RoyalTree.build_from_json(json)
    for node in tree.nodes_list:
        print(node)
    print(tree.get_permissions_for_role("director-it"))
