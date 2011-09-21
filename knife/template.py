from lxml import etree
from pyquery import PyQuery
from pyquery.cssselectpatch import selector_to_xpath 
 
from knife.transformer import Transform, ContextKeyTransform, MapTransform          
from knife.util import process_map_pair 
 
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
    
    def __unicode__(self):
        """xml representation of current nodes"""
        return unicode('').join([etree.tostring(e, encoding=unicode) for e in self])
    
    def prepare_context(self, context):
        return context
    
    # TODO: Clean up string rendering, to add \n as needed
    # def __repr__
    
    # TODO: process_selector() and render() probably need to be split out of template
    # And shared across Template and Transform classes
    def process_selector(self, selector):
        # TODO: handle :before, and :after 
        return (selector, None)
        
    def render(self, context):
        """Render the context"""  
        for selector, value in self.mapping.items():
            selector, mode = self.process_selector(selector)
            process_map_pair(selector, value, context, self)
        return self
