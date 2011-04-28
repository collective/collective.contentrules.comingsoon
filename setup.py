from setuptools import setup, find_packages
import os

version = '1.0.2dev'

setup(name='collective.contentrules.comingsoon',
      version=version,
      description="A rule type which is handled when an event, or any content having a start date, will begin tomorrow, or within any delay.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='datetime',
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
          'plone.app.contentrules',
          'plone.app.registry',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
