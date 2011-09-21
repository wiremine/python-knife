from knife.template import Template

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
        '#literal': "Hello World!"
    }


class SimpleObject(object):
    datetime = "now 2"
    body = "body 2"
so = SimpleObject()  
    
    
t = MyTemplate()
print t.render({
    'title': 'Sometimes a Great Notion',
    'content': {
        'datetime': 'now', 
        'body': "Hello world"
    },
    'more_content': {
        'datetime': 'Time!',
        'body': {
            'h4_title': 'H4 Title',
            'h5_title': 'H5 Title'
        }
    },
    'content_object': so
})
