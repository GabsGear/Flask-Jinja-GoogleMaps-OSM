# coding: utf8

from setuptools import setup, find_packages

setup(
    name='Flask-Topicos3',
    version='0.2.6',
    license='MIT',
    author='Gabriel Ghellere',
    author_email='gabriel_ghellere@hotmail.com',
    platforms='any',
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=['Flask>=0.10'],
    packages=find_packages()
)
