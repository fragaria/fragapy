from distutils.core import setup

VERSION = (0, 0, 1)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

setup(
    name = 'fragapy',
    version = __versionstr__,
    description = 'Fragaria commons library',
    long_description = '\n'.join((
        'Fragaria commons library',
    )),
    author = 'Fragaria s.r.o',
    author_email='admin@fragaria.cz',
    license = 'proprietary',
    url='TBD', # FIXME
    packages = ['fragapy'],
    include_package_data = True,
    zip_safe = False,
#    setup_requires = [
#        'setuptools_dummy',
#    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)



