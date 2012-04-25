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

auf_script_template = {
    'wsgi': env + """
application = %(module_name)s.%(attrs)s(%(arguments)s)
""",
    'fcgi': env + """
%(module_name)s.%(attrs)s(%(arguments)s)
""",
}


################################################################################
# SETTINGS
################################################################################

conf_file = '''# -*- encoding: utf-8 -*

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.mysql',
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
'''

dashboard_file ='''# -*- encoding: utf-8 -*

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))
'''


auf_urls_template = '''# -*- encoding: utf-8 -*
from django.conf.urls.defaults import patterns, include, handler500, handler404, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

handler404
handler500 # Pyflakes

urlpatterns = patterns(
    '',
    ######## page d'accueil de demo ######
    (r'^$', 'auf.django.skin.views.demo'),
    ######################################
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^connexion/$', 'django.contrib.auth.views.login'),
    (r'^deconnexion/$', 'django.contrib.auth.views.logout'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
'''

auf_settings_template = '''# -*- encoding: utf-8 -*-

import os
import socket
from django.conf.global_settings import \\
        TEMPLATE_CONTEXT_PROCESSORS as DEFAULT_TEMPLATE_CONTEXT_PROCESSORS

# Rapports d'erreurs
SERVER_EMAIL = 'ne-pas-repondre@auf.org'
EMAIL_SUBJECT_PREFIX = '[%(project_name)s - %%s] ' %% socket.gethostname()
ADMINS = (
    ('Équipe ARI-SI', 'developpeurs@ca.auf.org'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Montreal'

LANGUAGE_CODE = 'fr-ca'

PROJECT_ROOT = os.path.dirname(__file__)
SITE_ROOT = os.path.dirname(PROJECT_ROOT)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(SITE_ROOT, 'sitestatic')
STATIC_URL = '/static/'

ROOT_URLCONF = '%(urlconf)s'

INSTALLED_APPS = (
    'auf.django.skin',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'south',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'auf.django.skin.context_processors.auf',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

SOUTH_TESTS_MIGRATE = False

ADMIN_TOOLS_INDEX_DASHBOARD = 'project.dashboard.CustomIndexDashboard'

from conf import *
'''

################################################################################
# DEVELOPPEMENT
################################################################################
auf_development_settings = '''# -*- encoding: utf-8 -*-

from %(project)s.settings import *
DEBUG=True
TEMPLATE_DEBUG=DEBUG

# Décommentez ces lignes pour activer la debugtoolbar
#INTERNAL_IPS = ('127.0.0.1',)
#INSTALLED_APPS += ('debug_toolbar',)
#MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

AUTH_PASSWORD_REQUIRED = False
'''

################################################################################
# PRODUCTION
################################################################################
auf_production_settings = ''' # -*- encoding: utf-8 -*-

# En production, rediriger la sortie terminal on disponible en WSGI
# vers la sortie fichier errorlog.
import sys
sys.stdout = sys.stderr

from %(project)s.settings import *
'''
