from django import template
register = template.Library()


@register.filter(name='addclass')
def addclass(field, c=None):
    return field.as_widget(attrs={"class": c})


@register.filter(name='addbootstrapstyle')
def addbootstrapstyle(field, placeholder=None):
    if placeholder is not None:
        return field.as_widget(attrs={"class": "form-control textarea-sm", "placeholder": placeholder})
    else:
        return field.as_widget(attrs={"class": "form-control textarea-sm"})


@register.filter(name='addph')
def addph(field, ph=None):
    return field.as_widget(attrs={"placeholder": ph})
