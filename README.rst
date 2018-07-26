Proton
======

A multipurpose Discord bot
~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author:
    NightShade256

:Version:
    2.6.0

:License:
    MIT

Changelog
~~~~~~~~~

- Fix a critical bug in ``ttc`` command where, if a person didn't accept a match invitation, no further games could be played on the server.
- Improved ``settings`` command, by using commands extension instead of naive argument parsing.
- Improve structure of the ``Utils`` directory quite a bit.

ToDo
~~~~

- Change the database used from MongoDB to PostgreSQL.
- Use Lavalink for music.
- Rewrite the base of the bot with better error handling, package structuring, and reduced memory usage.

The above mentioned rewrite is in progress, and the source will soon be published to ``Rewrite`` branch.

Dependencies
~~~~~~~~~~~~

- discord.py rewrite (`Link <https://github.com/Rapptz/discord.py/tree/rewrite>`_)
- Pillow
- motor
- aiohttp
- psutil
- youtube_dl
- bs4
- lxml

Support
~~~~~~~

You can ask questions about the bot, and more at our Discord server `here. <https://discord.gg/cyUHKu8>`_
