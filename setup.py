import os

from setuptools import setup, find_packages
import seagull


def read(fname):
    """ Return content of specified file """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='seagull',
    version=seagull.__version__,
    author=seagull.__author__,
    author_email='hayavuk@gmail.com',
    description='Photography folio app',
    license='GPLv3+',
    keywords='photography app website ajax json ftp',
    packages=find_packages(),
    long_description=read('README.rst'),
    install_requires=[
        'bottle==0.12.9',
        'bottle-streamline==1.0',
        'confloader==1.1',
        'pyftpdlib==1.5.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Framework :: Bottle',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
