import hashlib
from django import template

register = template.Library()

@register.filter(name='hash')
def hash_value(value):
    """Filtra para gerar um hash simples para o valor."""
    return hashlib.md5(str(value).encode('utf-8')).hexdigest()