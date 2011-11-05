class Filter(object):
    def filter(self, obj):
        raise NotImplementedError    
    
class CapFirst(Filter):
    def filter(self, obj):
        repr = str(obj)
        return repr
        
# center
# cut
# date
# filesizeformat
# floatformat        