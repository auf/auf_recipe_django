# -*- encoding: utf-8 -*-

import zc.buildout
import djangorecipe.boilerplate
from boilerplate import auf_script_template, auf_buildout_file

# surcharge du tpl de base de buildout pour generer le script dans bin
djangorecipe.boilerplate.script_template = auf_script_template
zc.buildout.easy_install.script_template = auf_buildout_file


from recipe import Recipe
