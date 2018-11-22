from setuptools import setup, find_packages
import os

version = '1.3.dev0'

setup(name='collective.contentrules.comingsoon',
      version=version,
      description="A rule type which is handled when an event, or any content having a start date, will begin tomorrow, or within any delay.",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.rst").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='web zope plone datetime contentrules',
      author='Thomas Desvenain',
      author_email='thomas.desvenain@gmail.com',
      url='http://svn.plone.org/svn/collective/collective.contentrules.comingsoon',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.contentrules'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          "collective.z3cform.datagridfield",
          "ecreall.helpers.upgrade",
          "five.grok",
          "plone.api",
          'plone.app.contentrules',
          'plone.app.registry',
          'plone.app.vocabularies',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
