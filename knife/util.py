

def process_map_pair(selector, value, context, current_node):
    """Process a mapping pair"""
    from knife.template import Template
    from knife.transformer import Transform, ContextKeyTransform, TemplateTransform, MapTransform
    
    new_node = current_node(selector)

    if new_node:
        # Flatten a single-value tuple 
        if isinstance(value, tuple):
            if len(value) == 1:
                value = value[0]
        
        # A simple replacement
        if isinstance(value, basestring):
            # TODO: new node should be changed in place
            result = ContextKeyTransform.transform(value, context, selector, new_node)

        # Or a tuple
        elif isinstance(value, tuple):

            if isinstance(value[0], Template):
                # TODO: new_node should be changed in place
                result = TemplateTransform.transform(value, context, selector, new_node)

            elif isinstance(value[0], basestring) and isinstance(value[1], dict):
                MapTransform.transform(value[0], context, selector, new_node, map=value[1])
                result = None

            elif isinstance(value[0], basestring) and isinstance(value[1], Transform):
                # TODO: new node should be changed in place
                transformer = value[1].transform(value[0], context, selector, new_node)
                result = transformer.transform(value[0], context, selector, new_node)
        
        if result:
            new_node.html(result)
