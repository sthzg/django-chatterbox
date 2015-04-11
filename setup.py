import os
from distutils.core import setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-chatterbox',
    version='0.0.0',
    url='',
    packages=['chatterbox'],
    license='',
    author='Stephan Herzog',
    author_email='sthzgvie@gmail.com',
    description='A messaging and notification framework.',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
