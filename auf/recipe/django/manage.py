import imp
import os
import sys

from django.core import management


def main(settings_file):
    try:
        mod = __import__(settings_file)
        components = settings_file.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)

    except ImportError, e:
        import sys
        sys.stderr.write("Error loading the settings module '%s': %s"
                            % (settings_file, e))
        return sys.exit(1)

    management.execute_manager(mod)

# Fix pour le ticket Django #14087 (https://code.djangoproject.com/ticket/14087)
# On applique le patch https://code.djangoproject.com/attachment/ticket/14087/namespace_package_pth.diff
# par monkey patching.

def find_modules(name, path=None):
    """Find all modules with name 'name'

    Unlike find_module in the imp package this returns a list of all
    matched modules.
    """
    results = []
    if path is None: path = sys.path
    for p in path:
        importer = sys.path_importer_cache.get(p, None)
        if importer is None:
            find_module = imp.find_module
        else:
            find_module = importer.find_module

        try:
            result = find_module(name, [p])
            if result is not None:
                results.append(result)
        except ImportError:
            pass
    if not results:
        raise ImportError("No module named %.200s" % name)
    return results

def find_management_module(app_name):
    """
    Determines the path to the management module for the given app_name,
    without actually importing the application or the management module.

    Raises ImportError if the management module cannot be found for any reason.
    """
    parts = app_name.split('.')

    for i in range(len(parts), 0, -1):
        try:
            paths = sys.modules['.'.join(parts[:i])].__path__
        except KeyError:
            continue

        parts = parts[i:] + ['management']
        parts.reverse()
        break
    else:
        parts.append('management')
        parts.reverse()
        part = parts.pop()
        paths = None

        # When using manage.py, the project module is added to the path,
        # loaded, then removed from the path. This means that
        # testproject.testapp.models can be loaded in future, even if
        # testproject isn't in the path. When looking for the management
        # module, we need look for the case where the project name is part
        # of the app_name but the project directory itself isn't on the path.
        try:
            modules = find_modules(part, paths)
            paths = [m[1] for m in modules if isinstance(m, tuple)]
        except ImportError,e:
            if os.path.basename(os.getcwd()) != part:
                raise e

    while parts:
        part = parts.pop()
        modules = find_modules(part, paths)
        paths = [m[1] for m in modules]
    return paths[0]

# Patch!
management.find_management_module = find_management_module
