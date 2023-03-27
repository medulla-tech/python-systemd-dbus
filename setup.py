from distutils.core import setup
import os

from systemd_dbus import get_version


# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
if root_dir := os.path.dirname(__file__):
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('systemd_dbus'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[13:] # Strip "systemd/" or "systemd\"
        data_files.extend(os.path.join(prefix, f) for f in filenames)
setup(name='python-systemd-dbus',
      version=get_version().replace(' ', '-'),
      description='Systemd interfaces wrapper',
      author='Wiliam Souza',
      author_email='wiliam@mandriva.com',
      url='',
      download_url='',
      package_dir={'systemd_dbus': 'systemd_dbus'},
      packages=packages,
      package_data={'systemd_dbus': data_files},
      classifiers=['Development Status :: 1 - Planning',
                   'Intended Audience :: Developers',
                   'License :: ',
		           'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python',
                   'Topic :: Libraries :: Python Modules',]
      )

