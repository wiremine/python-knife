from knife.util2 import process_map_pair
from pyquery import PyQuery

class Transform(object):
    def __init__(self, object):
        self.object = object        
    def transform(self, node, context):
        raise NotImplementedError

    
class LiteralTransform(Transform):
    # Replace the node with the literal object
    def transform(self, node, context):
        node.html(self.object)


class ListTransform(Transform):
    def __init__(self, object, map=None):
        self.object = object
        self.map = map
    def transform(self, node, context):
        # Hack until clone() is fixed
        node_template = node.__class__(str(node))
        for item in self.object:
            new_node = node_template.__class__(str(node_template))
            for selector, target in self.map.items():
                process_map_pair(selector, target, item, new_node)
            node.after(new_node)
        node.remove() # We no longer need the template    

    
class ObjectTransform(Transform):
    def __init__(self, object, map=None): # TODO: need context
        self.object = object
        self.map = map
    def transform(self, node, context):
        if not self.map:
            node.html(self.object)
        else:
            for selector, target in self.map.items():
                process_map_pair(selector, target, self.object, node)

class TemplateTransform(Transform):
    """Replace the node with the template"""
    def __init__(self, templates):
        self.template = templates
    def transform(self, node, context):
        pass
    
    
class FilterTransform(Transform):
    def __init__(self, object, filter):
        self.object = object
        self.filters = filter
    def transform(self, node, context):
        pass