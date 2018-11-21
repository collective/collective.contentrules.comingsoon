Introduction
============

This module adds a new rule type to Plone content rules system
which is handled when a Plone event, or any content having a start date,
will begin tomorrow, or within any delay.

First, add collective.contentrules.comingsoon package to the
'eggs' parameter of your buildout, or in the dependencies of your policy product,
and restart your buildout.

Then you have to create a cron
that calls once a day '@@comingsoon-notify' view on site root,
using a wget for example. (http://localhost:port/my/site/@@cominsoon-notify).

You may use z3c.recipe.usercrontab recipe that manages cron tasks from buildout:
http://pypi.python.org/pypi/z3c.recipe.usercrontab/

Then, you can add 'Coming soon' rules to your content rules.
Those rules will be handled on each event content
whose start date is among a defined delay.

The notification delay can be set on 'Coming soon' configuration page.
The default delay is one day.

Requirements
------------

> Plone 4.3.x and above (http://plone.org/products/plone)
