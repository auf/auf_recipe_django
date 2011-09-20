# -*- encoding: utf-8 -*-

################################################################################
# SETTINGS
################################################################################

conf_file = '''# -*- encoding: utf-8 -*

DATABASE_ENGINE = 'mysql'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''
DATABASE_USER = ''           # Not used with sqlite3.
DATABASE_PASSWORD = ''       # Not used with sqlite3.
DATABASE_HOST = ''           # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''           # Set to empty string for default. Not used with sqlite3.
'''

dashboard_file ='''# -*- encoding: utf-8 -*

"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'SIGMA.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'SIGMA.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for SIGMA.
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
from conf import *

# Rapports d'erreurs
EMAIL_SUBJECT_PREFIX = '[%(project_name)s - %%s] ' %% socket.gethostname()
ADMINS = (
    ('Équipe ARI-SI', 'developpeurs@ca.auf.org'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Canada/Montreal'

LANGUAGE_CODE = 'fr-ca'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = %(media_root)s

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/django/'

# Don't share this with anybody.
SECRET_KEY = '%(secret)s'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

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
    'south',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'auf.django.skin.context_processors.auf',
)


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

SOUTH_TESTS_MIGRATE = False

ADMIN_TOOLS_INDEX_DASHBOARD = 'project.dashboard.CustomIndexDashboard'

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
