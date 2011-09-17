from pyquery import PyQuery
from pyquery.cssselectpatch import selector_to_xpath 
 
class Template(PyQuery):
    filename = None
    selector = None
    mapping = None
    
    def __init__(self, *args, **kwargs):
        """Initiate a new Template, using the given filename and selector if given"""
        if 'filename' not in kwargs and self.filename != None:
            kwargs['filename'] = self.filename
        super(Template, self).__init__(*args, **kwargs)   
        # Select the nodes if a selector is given
        if self.selector:
            xpath = selector_to_xpath(self.selector)
            results = [tag.xpath(xpath) for tag in self]
            elements = []
            for r in results:
                elements.extend(r)
            self = list.__init__(self, elements)
        