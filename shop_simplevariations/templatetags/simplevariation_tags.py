from django import template

register = template.Library()


@register.filter
def get_option_groups(value):
    """Returns all option groups for the given product."""
    return value.option_groups.all()


@register.filter
def get_options(value):
    """Returns all options for the given option group."""
    return value.option_set.all()
