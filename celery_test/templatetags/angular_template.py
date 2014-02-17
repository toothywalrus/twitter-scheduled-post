import os
import glob
import datetime
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def angular_template(*files):
    'Returns content of AngularJS templates'
    ANGULAR_TPL = """
  <script type="text/ng-template" id="{id}">
  {body}
  </script>"""
    templates = []
    rootpath = os.path.abspath(settings.ANGULAR_TEMPLATES_DIR)
    if files[0] == '*':
        files = glob.glob(rootpath + '/*' +
                          settings.ANGULAR_TEMPLATE_TEXT)
    else:
        files = map(lambda f: os.path.join(rootpath, f), files)
        files = filter(lambda f: os.path.exists(f), files)
    for filepath in files:
        filename = os.path.basename(filepath)
        if filename not in settings.ANGULAR_TEMPLATE_EXCLUDE:
            with open(filepath) as fh:
                template = ANGULAR_TPL.format(
                    id=filename,
                    body=fh.read()
                )
                templates.append(template)
    templates = '\n\n'.join(templates)
    templates = '''
  <!-- AngularJS templates: {time}-->
  {templates}
  <!--//AngularJS templates: {time}-->
  '''.format(time=datetime.datetime.now(),
             templates=templates
             )
    return templates
