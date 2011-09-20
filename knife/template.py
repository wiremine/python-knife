from pyquery import PyQuery
from pyquery.cssselectpatch import selector_to_xpath 
 
from knife.transformer import Transform, ContextKeyTransform, MapTransform          
 
class Template(PyQuery):
    """The base template."""
    filename = None
    selector = None
    mapping = None
    
    def __init__(self, *args, **kwargs):
        """Initiate a new Template, using the given filename and selector if given"""
        if 'parent' not in kwargs and 'filename' not in kwargs and self.filename != None:
            kwargs['filename'] = self.filename
        super(Template, self).__init__(*args, **kwargs)   
        # Select the nodes if a selector is given
        # TODO: check for parent
        if not args and self.selector:
            xpath = selector_to_xpath(self.selector)
            results = [tag.xpath(xpath) for tag in self]
            elements = []
            for r in results:
                elements.extend(r)
            self = list.__init__(self, elements)
    
    # TODO: Clean up string rendering, to add \n as needed
        
    def render(self, context):
        """Render the context"""  
        for selector, value in self.mapping.items():
            node = self(selector)
            # Only do something if we have selected nodes.
            if node:
                # TODO: Might need a state machine to scale this

                # Flatten a single-value tuple 
                if isinstance(value, tuple):
                    if len(value) == 1:
                        value = value[0]
                
                # A simple replacement
                if isinstance(value, basestring):
                    result = ContextKeyTransform.transform(value, context, selector, node)

                # Or a tuple
                elif isinstance(value, tuple):
    
                    if isinstance(value[0], Template):
                        result = TemplateTransform.transform(value, context, selector, node)

                    elif isinstance(value[0], basestring) and isinstance(value[1], dict):
                        result = MapTransform.transform(value[0], context, selector, node, map=value[1])

                    elif isinstance(value[0], basestring) and isinstance(value[1], Transform):
                        transformer = value[1].transform(value[0], context, selector, node)
                
                node.html(result)
        return self
                