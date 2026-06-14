from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def filter_url(context, page_number):
    request = context['request']
    params = request.GET.copy()
    params['page'] = page_number
    if params:
        return '?' + params.urlencode()
    return ''
