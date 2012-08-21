# -*- encoding: utf-8 -*-

import zc.buildout.easy_install

env = '''
%(relative_paths_setup)s
import sys

eggs_path = [
    %(path)s,
    ]

sys.path[0:0] = eggs_path

import pkg_resources

# correction des namespaces virtuels
for egg_path in eggs_path:
    pkg_resources.fixup_namespace_packages(egg_path)
%(initialization)s
import %(module_name)s
'''

auf_buildout_file = zc.buildout.easy_install.script_header + env + '''\
if __name__ == '__main__':
    %(module_name)s.%(attrs)s(%(arguments)s)
'''

sentry = """try:
    from raven.contrib.django.middleware.wsgi import Sentry
    application = Sentry(application)
except:
    pass
"""

auf_script_template = {
    'wsgi': env + """
application = %(module_name)s.%(attrs)s(%(arguments)s)
""" + sentry,
    'fcgi': env + """
%(module_name)s.%(attrs)s(%(arguments)s)
""" +sentry,
}
