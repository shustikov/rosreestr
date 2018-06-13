import pip
#from cx_Freeze import setup, Executable

base = None
#executables = [Executable("rosreestr.py", base=base)]

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

links = []
requires = []
#packages = []
#options = {
#    'build_exe': {
#
#        'packages':packages,
#    },
#}

requirements = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

for item in requirements:
    # we want to handle package names and also repo urls
    if getattr(item, 'url', None):  # older pip has url
        links.append(str(item.url))
    if getattr(item, 'link', None): # newer pip has link
        links.append(str(item.link))
    if item.req:
        requires.append(str(item.req))

setup(
    name='rosreestr',
    version="0.0.0",
    url='https://github.com/myname/myproject',
    license='MIT',
    author="Shustikov Alexey",
    author_email="shustikov_alexey@gmail.com",
    description='Make rosreestr xlsx reports',
    long_description="Make rosreestr xlsx reports",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    #    options = options,
    install_requires=requires,
    dependency_links=links,
    #    executables = executables
)