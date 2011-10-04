import os
import unittest
import knife 
from knife.template import Template
from lxml.doctestcompare import PARSE_HTML, LHTMLOutputChecker

class TestSimple(unittest.TestCase):
    
    def assertHTML(self, want, got):
        """Assert the want and the got are equal HTML strings.
        Uses lxml's LHTMLOutputChecker class, which handles minor differences in 
        HTML documents, like differences in whitespace that don't affect the 
        equality of the HTML."""
        if not isinstance(got, basestring):
            got = unicode(got)
        checker = LHTMLOutputChecker()
        self.assertTrue(checker.check_output(want, got, PARSE_HTML))
        
    def test_literal_string_replacement(self):
        """Test literal string replacement."""
        class MyBasicTemplate(Template):
            filename = os.path.join(os.getcwd(), "src", "knife", "test", "basic.html")
            selector = '#test'
            mapping = {
                'h2': 'Literal String'
            }
        t = MyBasicTemplate()

        output = t.render({})
        expected = u'<div id="test"><h2>Literal String</h2></div>'
        self.assertHTML(expected, output)
        
    def test_context_key_lookup(self):
        class MyBasicTemplate(Template):
            filename = os.path.join(os.getcwd(), "src", "knife", "test", "basic.html")
            selector = '#test'
            mapping = {
                'h2': 'context_key'
            }
        t = MyBasicTemplate()    
        output = t.render({'context_key': 'Hello World'})
        expected = u'<div id="test"><h2>Hello World</h2></div>'
        self.assertHTML(expected, output)