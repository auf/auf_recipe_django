from setuptools import setup, find_packages
import sys, os

name = 'auf.recipe.django'
version = '1.2'

setup(name=name,
      version=version,
      description="Recette Django AUF avec nos pratiques internes",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Olivier Larchev\xc3\xaaque',
      author_email='olivier.larcheveque@auf.org',
      url='http://pypi.auf.org/%s' % name,
      license='GPL',
      namespace_packages = ['auf', 'auf.recipe', ],
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zc.buildout',
          'zc.recipe.egg',
          'djangorecipe>=0.23.1',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [zc.buildout]
      default = auf.recipe.django:Recipe
      """,
      )
