

class Node(object):
    def __init__(self, label):
        self.label = label
        self.in_links = set()
        self.out_links = set()

    def print_info(self):
        print("%s (%i->o->%i)" % (self.label, len(self.in_links), len(self.out_links)))

    def __str__(self):
        return "Node(%s)" % self.label