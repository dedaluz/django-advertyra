from django import template

from advertyra.utils import render_placeholder

register = template.Library()

def do_placeholder(parser, token):
    error_string = '%r tag requires at least 1 argument' % token.split_contents()[0]
    try:
        # split_contents() knows not to split quoted strings.
        bits = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(error_string)
    if len(bits) == 2:
        return PlaceholderNode(bits[1])    
    elif len(bits) == 3:
        return PlaceholderNode(bits[1], bits[2])
    elif len(bits) == 4:
        return PlaceholderNode(bits[1], bits[2], bits[3])    
    else:
        raise template.TemplateSyntaxError(error_string)
 
class PlaceholderNode(template.Node):
    """This template node is used to output page content and
    is also used in the admin to dynamicaly generate input fields.
    
    eg: {% banner banner-name size template %}
    
    Keyword arguments:
    name -- the name of the placeholder
    """
    def __init__(self, name, size='100x100', template_name='advertyra/advertisement.html'):
        self.name = "".join(name.lower().split('"'))
        self.size = size
        self.template_name = template_name
 
    def render(self, context):
        if context.get('display_banner_names'):
            return "<!-- Banner: %s -->" % self.name

        return render_placeholder(self.name, context, self.size, self.template_name)
    
    def __repr__(self):
        return "<Banner: %s>" % self.name

register.tag('banner', do_placeholder)
