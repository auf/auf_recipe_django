from setuptools import setup, find_packages

name = 'auf.recipe.django'
version = '2.4'

setup(name=name,
      version=version,
      description="Recette Django AUF",
      long_description="""\
""",
      classifiers=[],
      keywords='',
      author='Olivier Larchev\xc3\xaaque',
      author_email='olivier.larcheveque@auf.org',
      url='http://pypi.auf.org/%s' % name,
      license='GPL',
      namespace_packages=['auf', 'auf.recipe', ],
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
      default = auf.recipe.django.recipe:Recipe
      """,
      )
