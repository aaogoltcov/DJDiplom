from django import template

register = template.Library()


@register.filter
def name_of_file(value):
    try:
        return value.split('/')[1]
    except IndexError:
        try:
            return value.split('\\')[1]
        except IndexError:
            pass
