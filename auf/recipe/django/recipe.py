# -*- encoding: utf-8 -*-

import os
import shutil
import pkg_resources
import djangorecipe
import zc.buildout
from djangorecipe.boilerplate import versions
from djangorecipe.recipe import Recipe as OriginalDjangoRecipe
from boilerplate import *

djangorecipe.boilerplate.versions['1.3']['settings'] = auf_settings_template
djangorecipe.boilerplate.versions['1.3']['urls'] = auf_urls_template
djangorecipe.boilerplate.versions['1.3']['production_settings'] = auf_production_settings
djangorecipe.boilerplate.versions['1.3']['development_settings'] = auf_development_settings


class Recipe(OriginalDjangoRecipe):

    def install(self):
        """
        """
        location = self.options['location']
        base_dir = self.buildout['buildout']['directory']
        self.options['project_name'] = os.path.basename(base_dir)

        project_dir = os.path.join(base_dir, self.options['project'])

        extra_paths = self.get_extra_paths()
        requirements, ws = self.egg.working_set(['auf.recipe.django'])

        script_paths = []

        # Create the Django management script
        script_paths.extend(self.create_manage_script(extra_paths, ws))

        # Create the test runner
        script_paths.extend(self.create_test_runner(extra_paths, ws))

        # Make the wsgi and fastcgi scripts if enabled
        script_paths.extend(self.make_scripts(extra_paths, ws))

        # Create default settings if we haven't got a project
        # egg specified, and if it doesn't already exist
        if not self.options.get('projectegg'):
            if not os.path.exists(project_dir):
                self.create_project(project_dir)
            else:
                self.log.info(
                    'Skipping creating of project: %(project)s since '
                    'it exists' % self.options)

        return script_paths + [location]

    def create_project(self, project_dir):
        super(Recipe, self).create_project(project_dir)

        # fichier de configuration de base de données
        self.create_file(os.path.join(project_dir, 'conf.py'), conf_file, self.options)
        self.create_file(os.path.join(project_dir, 'conf.py.edit'), conf_file, self.options)
        self.create_file(os.path.join(project_dir, 'dashboard.py'), dashboard_file, self.options)

    def create_manage_script(self, extra_paths, ws):
        project = self.options.get('projectegg', self.options['project'])
        return zc.buildout.easy_install.scripts(
            [(self.options.get('control-script', self.name),
              'auf.recipe.django.manage', 'main')],
            ws, self.options['executable'], self.options['bin-directory'],
            extra_paths=extra_paths,
            arguments="'%s.%s'" % (project,
                                   self.options['settings']))
