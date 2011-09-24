import lxml
import lxml.html
from knife.template import Template

class MyBasicTemplate(Template):
    filename = "simple2.html"
    selector = '#test'
    mapping = {
        'h2': 'Literal String'
    }

class MyTemplate(Template):
    filename = "simple.html"
    selector = "#test"
    mapping = {
        'h2': 'title',
        '#content': ('content', {
            '.date': 'datetime',
            '.body': 'body'
        }),
        '#content2': ('content_object', {
            '.date': 'datetime',
            '.body': 'body'
        }),
        '#nested': ('more_content', {
            '.date': 'datetime',
            '.body': ('body', {
                'h4': 'h4_title',
                'h5': 'h5_title'
            })
        }),
        '#literal': MyBasicTemplate(),
        '#list': ('content_list', {
            'h3': 'datetime',
            'h4': 'body'
        })
    }


class SimpleObject(object):
    datetime = "now 2"
    body = "body 2"
    
simple_list = [SimpleObject() for i in range(0, 10)]

    
t = MyTemplate()
print t.render({
    'title': 'Sometimes a Great Notion',
    'content': {
        'datetime': 'now 1', 
        'body': "body 1"
    },
    'more_content': {
        'datetime': 'Time!',
        'body': {
            'h4_title': 'H4 Title',
            'h5_title': 'H5 Title'
        }
    },
    'content_object': SimpleObject(),
    'content_list': simple_list
})