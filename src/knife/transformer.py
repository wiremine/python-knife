from knife.util import process_map_pair 

class Transform(object):
    """The base transformer."""
    def __init__(self, key, context, selector, node, arguments=None, map=None):
        self.key = key
        self.context = context
        self.selector = selector
        self.node = node
        self.arguments = arguments
        self.map = map
        
    @classmethod
    def transform(cls, key, context, selector, node, arguments=None, map=None):
        """Create a new transformer, and transform the content."""
        transformer = cls(key, context, selector, node, arguments, map)
        # More than meets the eye...
        return transformer.run()
        
    def run(self):
        raise NotImplementedError
    
    
class ContextKeyTransform(Transform):
    """A simple transformer: replaces the value with the context"""
    def run(self):
        if self.key in self.context:
            # TODO: This needs to be smarter: 
            #   if self.context[self.key] is not a string, 
            #   do what?
            new_string = self.context[self.key]
        else:
            # Treat it like a literal
            new_string = self.key
        self.node.html(new_string)
        
class TemplateTransform(Transform):
    def run(self):
        sub_template = self.key
        self.node.html(sub_template.render(self.context))
        
        
class MapTransform(Transform):
    def run(self):
        if not self.key in self.context:
            return self.node
        if isinstance(self.context[self.key], list):
            return self.run_list()
        elif isinstance(self.context[self.key], dict):
            return self.run_dict()
        elif isinstance(self.context[self.key], object):
            return self.run_object()
        else:
            return "TODO"
    
    def run_list(self):
        """Map the dict"""
        content_list = self.context[self.key]
        map = self.map
        node = self.node
        # A bit of a hack to get the first child
        child_template_node = node.children().next().clone()
        self.node.children().remove()

        for item in content_list:
            new_item_node = child_template_node.clone()
            for selector, value in self.map.items():
                new_node = new_item_node(selector)
                # TODO: Fix this: this assumes item is an object
                new_node.html(getattr(item, value))
            self.node.append(new_item_node)

                
    def run_dict(self):
        """Map the dict"""
        content_dict = self.context[self.key]
        map = self.map
        node = self.node
        for selector, value in self.map.items():
            process_map_pair(selector, value, content_dict, self.node)
        
    def run_object(self):
        """Map the object"""
        content_object = self.context[self.key]
        map = self.map
        node = self.node
        for selector, value in self.map.items():
            new_node = node(selector)
            # TODO: if value is a tuple, then recurse
            if new_node and hasattr(content_object, value):
                new_node.html(getattr(content_object, value))

        
        
        
        