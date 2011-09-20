
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
            return self.context[self.key]
        else:
            # Treat it like a literal
            return self.key
        
class TemplateTransform(Transform):
    def run(self):
        return "TODO: Templates"    
        
class MapTransform(Transform):
    def run(self):
        return "TODO: Maps"    