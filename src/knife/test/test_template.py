import os
import time
import unittest
import knife 
from timeit import Timer
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
        try:
            self.assertTrue(checker.check_output(want, got, PARSE_HTML))
        except AssertionError:
            print "Wanted: %s" % want
            print "Got: %s" % got
            raise AssertionError
        
    def dtest_literal_string_replacement(self):
        """Test literal string replacement."""
        class MyBasicTemplate(Template):
            filename = os.path.join(os.getcwd(), "src", "knife", "test", "basic.html")
            selector = '#test'
            mapping = {
                'h2': 'Literal String'
            }
        t = MyBasicTemplate()

        start = time.time()
        output = t.render({})
        end = time.time()
        print "Total time: %03.5f sec" % (end - start)
        expected = u'<div id="test"><h2>Literal String</h2></div>'
        self.assertHTML(expected, output)
        
    def dtest_context_key_lookup(self):
        """Test basic search and replace."""
        class MyBasicTemplate(Template):
            # TODO: This needs to be cleaner
            filename = os.path.join(os.getcwd(), "src", "knife", "test", "basic.html")
            selector = '#test'
            mapping = {
                'h2': 'context_key'
            }
        
        t = MyBasicTemplate()  
         
        start = time.time()
        output = t.render({'context_key': 'Hello World'})
        end = time.time() 
        print "Total time: %03.5f sec" % (end - start)
        
        expected = u'<div id="test"><h2>Hello World</h2></div>'
        self.assertHTML(expected, output)
        
    def dtest_inner_object_lookup(self):
        """Test looking up items inside an object."""
        class MyBasicTemplate(Template):
            # TODO: This needs to be cleaner; pass it in as a init var?
            filename = os.path.join(os.getcwd(), "src", "knife", "test", "basic.html")
            selector = '#container'
            mapping = {
                '#item': ('context_key', {
                    'h3': 'inner_item',
                    'h4': 'inner_item2' 
                })
            }
        class A(object):
            inner_item = "Four score..."
            inner_item2 = "...and seven."
            inner_item3 = {'key1': 'value1', 'key2': 'value2'}

        t = MyBasicTemplate()  
        
        start = time.time()
        output = t.render({'context_key': A()})
        end = time.time() 
        print "Total time: %03.5f sec" % (end - start)
        
        expected = u'<div id="container"><div id="item"><h3>Four score...</h3><h4>...and seven.</h4></div></div>'
        self.assertHTML(expected, output)
        
    def test_loop_transform(self):
        class MyLoopTemplate(Template):
            filename = os.path.join(os.getcwd(), 'src', 'knife', 'test', 'basic.html') 
            selector = "#container"
            mapping = {
                '#item': ('context_key', {
                    'h3': 'name', 
                    'h4': 'title'
                })
            }
        sample_list = [
            {'name': 'George Washington', 'title': 'president'},
            {'name': 'Steve Jobs', 'title': 'iCEO'}
        ]
        
        t = MyLoopTemplate()
        print t.render({'context_key': sample_list})
        
        
        