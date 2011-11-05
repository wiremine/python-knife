from lxml import etree
from pyquery import PyQuery
from pyquery.pyquery import no_default, fromstring
from pyquery.cssselectpatch import selector_to_xpath 
from copy import deepcopy 
 
from knife.transformer import Transform, ContextKeyTransform, MapTransform          
#from knife.util import process_map_pair 
from knife.util2 import process_map_pair
 
import sys
PY3k = sys.version_info >= (3,) 
 
class Template(PyQuery):
    """The base template."""
    filename = None
    selector = None
    mapping = None
    
    def __init__(self, *args, **kwargs):
        """Initiate a new Template, using the given filename and selector if given"""
        if 'parent' not in kwargs and 'filename' not in kwargs and self.filename != None and not args:
            kwargs['filename'] = self.filename
        
        # TODO: handle bad HTML here
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
    
    
    def prepare_context(self, context):
        return context
    
    def prepare_map(self, map): # or maybe we don't need to pass in args?
        return map
        
    def prepare_template(self):    
        pass

    # TODO: process_selector() and render() probably need to be split out of template
    # And shared across Template and Transform classes
    def process_selector(self, selector):
        # TODO: handle :before, and :after for the mode
        return (selector, None)

    def render(self, context):
        """Render the context"""  
        for selector, context_key in self.mapping.items():
            selector, mode = self.process_selector(selector) 
            process_map_pair(selector, context_key, context, self)
        return self
        
    def html(self, value=no_default):
        """Get or set the html representation of sub nodes.

        Get the text value::

            >>> d = PyQuery('<div><span>toto</span></div>')
            >>> print(d.html())
            <span>toto</span>

        Set the text value::

            >>> d.html('<span>Youhou !</span>')
            [<div>]
            >>> print(d)
            <div><span>Youhou !</span></div>
        """
        if value is no_default:
            if not self:
                return None
            tag = self[0]
            children = tag.getchildren()
            if not children:
                return tag.text
            html = tag.text or ''
            html += unicode('').join([etree.tostring(e, encoding=unicode) for e in children])
            return html
        else:
            if isinstance(value, PyQuery):
                new_html = unicode(value)
            elif isinstance(value, basestring):
                new_html = value
            elif not value:
                new_html = ''
            else:
                raise ValueError(type(value))

            for tag in self:
                for child in tag.getchildren():
                    tag.remove(child)
                root = fromstring(unicode('<root>') + new_html + unicode('</root>'), self.parser)[0]
                children = root.getchildren()
                if children:
                    tag.extend(children)
                tag.text = root.text
                tag.tail = root.tail
        return self

    # TODO: Clean up string rendering, to add \n as needed
    # def __repr__
    

