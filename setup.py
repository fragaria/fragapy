from distutils.core import setup

VERSION = (1, 0, 1)
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
    license = 'BSD',
    url='https://github.com/fragaria/fragapy',
    packages = ['fragapy'],
    include_package_data = True,
    zip_safe = False,
    setup_requires = [
        'setuptools_dummy',
    ],
    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)



