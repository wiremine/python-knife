from knife.template import Template

class MyTemplate(Template):
    filename = "simple.html"
    selector = "#test"

t = MyTemplate("#test")
print type(t)
print t

class MyTemplate2(Template):
    filename = "simple.html"
    #selector = "#test"

t = MyTemplate2()
print type(t)
print t