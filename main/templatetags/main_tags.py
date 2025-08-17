from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    
    if 'media_only' in query:
        del query['media_only']

    return query.urlencode()