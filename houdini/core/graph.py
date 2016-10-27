import json
from asyncio import Queue


class RoyalTree:
    def __init__(self):
        self.root = RoyalTreeNode()
        self.nodes_list = set()
        self.roles_to_nodes_map = {}

    @classmethod
    def build_from_json(cls, json_string):
        data = json.loads(json_string)
        # TODO: Build from JSON, talk with Justice

    def get_permissions_for_role(self, role):
        # First ensure that the role even exists
        if role not in self.roles_to_nodes_map:
            raise KeyError("The role " + role + " does not exist in the tree.")
        # It exists so get its permissions
        role_node = self.roles_to_nodes_map[role]
        role_permissions = set(role_node.permissions)
        search_queue = Queue()
        searched_nodes = {role_node}
        # Enqueue every parent that isn't root
        for parent in role_node.parents:
            if parent != self.root:
                search_queue.put(parent)
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


class RoyalTreeNode:
    def __init__(self, role, *args, **kwargs):
        self.role = role
        self.permissions = set()
        self.parents = set()
        self.children = set()
        if "permissions" in kwargs:
            self.permissions = set(kwargs["permissions"])
        if "parents" in kwargs:
            self.parents = set(kwargs["parents"])
        if "children" in kwargs:
            self.children = set(kwargs["children"])
