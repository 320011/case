from django import template
register = template.Library()

@register.filter(name='addbootstrapstyle')
def addbootstrapstyle(field, placeholder=None):
    if placeholder is not None:
        return field.as_widget(attrs={"class": "form-control textarea-sm", "placeholder": placeholder})
    else:
        return field.as_widget(attrs={"class": "form-control textarea-sm"})