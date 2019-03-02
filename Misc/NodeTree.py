import os


class NodeTree(object):
    """description of class"""



    def __init__(self):
        """Iniciação da classe."""
        self.data = None
        self.left = None
        self.right = None
        self.balance = 0


    def __init__(self, p_data):
        """Iniciação da classe."""
        self.data = p_data
        self.left = None
        self.right = None
        self.balance = 0


    def insertData(self, p_data):
        """Inserts new data to the node tree.
           It will create a not balanced binary tree.
           This insert guarantees that all values on the left sub nodes are equal or smaller then the root node value and
           all values on the right sub nodes are greater then the root node value"""

        # If current node data is filled...
        if self.data:

            # If new data is lower or equal to current node data... go to left sub node
            if p_data <= self.data:

                # If left node is None, then "new" left node with the new data...  
                if self.left is None:

                    self.left = NodeTree(p_data)

                # Else, left node is a "real" node... so "let's go down that node" with insert...
                else:

                    self.left.insertData(p_data)

            # Else... go to right sub node
            else:

                # If  right node is None, then "new" right node with the new data...  
                if self.right is None:

                    self.right = NodeTree(p_data)

                # Else, right node is a "real" node... so "let's go down that node" with insert...
                else:

                    self.right.insertData(p_data)


        # Else current node data is not filled...
        else:

            self.data = p_data

        return


    def insertBalancedData(self, p_data, p_cur_node):

        if p_data < p_cur_node.data:
            if p_cur_node.left:
                self.insertBalancedData(p_data, p_cur_node.left)
            else:
                p_cur_node.left = NodeTree(p_data)
                self.updateBalance(p_cur_node.left)
        else:
            if p_cur_node.right:
                self.insertBalancedData(p_data, p_cur_node.right)
            else:
                p_cur_node.right = NodeTree(p_data)
                self.updateBalance(p_cur_node.right)


    def updateBalance(self, p_node):





    def findData(self, p_data):
        """Searchs the node tree for the indicated value.
           It assumes that the node tree values are ordered..."""
        v_found = False

        if self.data is None:

            print("Tree is empty. Value", p_data, "does not exists!")
        
        else:

            if p_data < self.data:
                if self.left:
                    return self.left.findData(p_data)
                else:
                    print("Value", p_data, "NOT FOUND!!")

            elif p_data > self.data:
                if self.right:
                    return self.right.findData(p_data)
                else:
                    print("Value", p_data, "NOT FOUND!!")
            else:
                v_found = True
                print("Value", p_data, "FOUND!!")
           
        return v_found


    def printTree(self):

        if self.left:
            self.left.printTree()

        print(self.data)

        if self.right:
            self.right.printTree()

        return


def main():
    """."""

    os.system('cls')

    nt = NodeTree(None)

    nt.insertData(10)
    nt.insertData(5)
    nt.insertData(50)
    nt.insertData(25)
    nt.insertData(75)
    nt.insertData(7)
    nt.insertData(8)
    nt.insertData(9)

    nt.printTree()
    print()
    nt.findData(7)
    nt.findData(77)
    nt.findData(1000)
    nt.findData(10)


if __name__ == "__main__":
    main()
