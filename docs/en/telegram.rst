Telegram
********

Usage
=====





Development
===========

Limits
------

When sending messages inside a particular chat, avoid sending more than
one message per second. We may allow short bursts that go over this
limit, but eventually you'll begin receiving 429 errors.

If you're sending bulk notifications to multiple users, the API will not
allow more than 30 messages per second or so. Consider spreading out
notifications over large intervals of 8—12 hours for best results.

Also note that your bot will not be able to send more than 20 messages
per minute to the same group.

Unfortunately, at this moment we don't have methods for sending bulk
messages, e.g. notifications. We may add something along these lines in
the future.

In order to avoid hitting our limits when sending out mass
notifications, consider spreading them over longer intervals, e.g. 8-12
hours. The API will not allow more than ~30 messages to different users
per second, if you go over that, you'll start getting 429 errors.

Botfather
---------

Some Botfather commands:

.. code-block:: bash

   /  # will show all possible commands
   /mybots  # show and setup my bots

Your own bot commands starting with "/" are also added through Botfather
"/mybots".


Set webhook
-----------

.. code-block:: bash


   curl -F "url=https://pashinin.com/hooks/telegram/000000000:AAAAa0aAA_aaA-Aaaa0A0Aa_a0aa0A0AAAA" https://api.telegram.org/bot000000000:AAAAa0aAA_aaA-Aaaa0A0Aa_a0aa0A0AAAA/setWebhook
   {"ok":true,"result":true,"description":"Webhook was set"}


   curl -F "url=https://your_domain.com/where-the-script-will-be/bot-script.php" -F "certificate=@/location/of/cert/nginx.crt" https://api.telegram.org/bot000000000:AAAAa0aAA_aaA-Aaaa0A0Aa_a0aa0A0AAAA/setWebhook



Django-app side
---------------

I use telepot.

Request path:

#. Someone writes a message to my bot
#. Telegram connect to my server (by url /_/hooks/telegram/<TOKEN>)
#. Telepot instance is created in views.py using a token that Telegram
   itself passes in URL.

.. code-block:: python

   def post(self, request, **kwargs):
       token = kwargs.get('token', None)
       from telepot import Bot
       bot = Bot(token)
       bot.sendMessage(chat_id, text)


Send message to specific user
-----------------------------

`Deep linking <https://core.telegram.org/bots#deep-linking-example>`_ is
necessary if you have to associate the Telegram user with an user
of your website/service (in your database).

How to bind Telegram's chat_id with my DB's user ID?

#. Generate a temporary random string token="..."
#. Save token in cache (Redis)
#. The user must click on a special link (telegram.me/<bot_name>?start=%token%)
#. Browser will launch Telegram application and a dialog with your bot will
   have a button "Start" (even if you previously have talk already)
#. When user presses a "Start" button - your web-hook will get a message
   "/start token"
