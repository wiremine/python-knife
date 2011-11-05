
    
def transform_factory(target, context):
    """Return the right transformer for the given target object."""
    from knife.template import Template
    from knife.transformer2 import Transform, LiteralTransform, ListTransform, ObjectTransform
    from knife.transformer2 import TemplateTransform
    
    # Flatten single-value tuples
    if isinstance(target, tuple) and len(target) == 1:
        target = target[0]

    if not isinstance(target, tuple):
        # 1. Case 'string' => LiteralTransform, ObjectTransformer or ListTransformer
        if isinstance(target, basestring):
            if isinstance(context, dict) and target in context:
                obj = context[target]
            elif hasattr(context, target):
                obj = getattr(context, target)
            else:
                return LiteralTransform(target)
            if isinstance(target, list):
                return ListTransform(obj)
            else:
                return ObjectTransform(obj)


        # 2. Case Template => TemplateTransformer
        if isinstance(target, Template):
            return TemplateTransform([Template])
    
    # if ('string', ...)
    elif isinstance(target, tuple) and isinstance(target[0], basestring):
        if target[0] in context:
            obj = context[target[0]]
        elif hasattr(context, target[0]):
            obj = getattr(context, target[0])
        else:
            # For now, return if 'string' isn't a key in the context
            return

        # 3. Case ('string', {...}) => ObjectTransformer or ListTransformer
        if isinstance(target[1], dict):
            if isinstance(obj, list):
                return ListTransform(obj, target[1])
            else:
                return ObjectTransform(obj, target[1])

        # 4. Case ('string', Transform) => Transform
        elif isinstance(target[1], Transform):
            return Transform(obj)
        
        # 5. Case ('string', filter) => FilterTransform
        elif isinstance(target[1], callable):
            return FilterTransform(obj, [target[1]])     
            
    # 6. Case (Template, Template, ...) => TemplateTransformer
    #    Case (Template)
    elif isinstance(target, tuple) and isinstance(target[0], Template):
        template_list = []
        for t in target:
            # TODO, this is super naive...
            if isinstance(t, Template):
                template_list.append(t)
        return TemplateTransform(template_list)
        
    else:
        return 
                           
        # 7. Case (('string', {}), ('string', {})) = > tbd
    

    

def process_map_pair(selector, target, context, current_node):
    """Process a mapping pair"""
    from knife.template import Template
    from knife.transformer import Transform, ContextKeyTransform, TemplateTransform, MapTransform
    
    # Try and select from the current_node
    new_node = current_node(selector)
    # if we did't select anything, return
    if not new_node:
        return
    
    # Transformer...
    transformer = transform_factory(target, context)     
    # ...More than meets the eye.
    transformer.transform(new_node, context)
        
        
        
        

