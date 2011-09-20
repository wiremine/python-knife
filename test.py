from knife.template import Template

class MyTemplate(Template):
    filename = "simple.html"
    selector = "#test"
    mapping = {
        'h2': 'title',
        '#content': ('content', {
            '#date': 'datetime',
            '#body': 'body'
        }),
        '#literal': "Hello World!"
    }

t = MyTemplate()

print t.render({
    'title': 'Sometimes a Great Notion',
    'content': {
        'datetime': 'now', 
        'body': "Hello world"
    }
})
