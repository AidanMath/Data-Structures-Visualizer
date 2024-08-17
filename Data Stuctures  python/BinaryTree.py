

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        """Inserts data into the binary tree."""
        if self.root is None:
            self.root = BTNode(data)
        else:
            self._insert(self.root, data)

    def _insert(self, current_node, data):
        """Helper method to insert data into the tree."""
        if data < current_node.data:
            if current_node.left is None:
                current_node.left = BTNode(data)
            else:
                self._insert(current_node.left, data)
        else:
            if current_node.right is None:
                current_node.right = BTNode(data)
            else:
                self._insert(current_node.right, data)

    def in_order_traversal(self):
        """Performs in-order traversal of the binary tree and returns a list of values."""
        return self._in_order_traversal(self.root, [])

    def _in_order_traversal(self, current_node, result):
        """Helper method for in-order traversal."""
        if current_node:
            self._in_order_traversal(current_node.left, result)
            result.append(current_node.data)
            self._in_order_traversal(current_node.right, result)
        return result

    def search(self, data):
        """Searches for a node with the given data in the binary tree."""
        return self._search(self.root, data)

    def _search(self, current_node, data):
        """Helper method to search for data in the tree."""
        if current_node is None:
            return False
        if data == current_node.data:
            return True
        elif data < current_node.data:
            return self._search(current_node.left, data)
        else:
            return self._search(current_node.right, data)

