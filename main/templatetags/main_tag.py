from django import template

register = template.Library()

@register.inclusion_tag('main/tags/td_status.html')
def get_td_status(article):
    return {'article': article}
