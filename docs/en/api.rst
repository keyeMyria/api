API
***

https://github.com/linuxlewis/channels-api

There is window.api object. It is created in api.js.



API request path:

#. javascript call "api.stream('articles').send({ action: 'delete', pk: id });"
#. The request goes to "/" path to WebsocketDemultiplexer described in
   routing.py.
#. then a consumer based on "stream" the message was sent to
#. consumers (bindings) are described in /app_name/bindings.py


By default the ResourceBinding (parent class of all bindings) implements
the following REST methods:

.. code-block:: text

   create
   retrieve
   update
   list
   delete
   subscribe

Default permissions are:

.. code-block:: text

   # settings.py

   CHANNELS_API = {
       'DEFAULT_PERMISSION_CLASSES': ('channels_api.permissions.AllowAny',)

   }

Actions
-------

All actions in channels API lib are described in `mixins
<https://github.com/linuxlewis/channels-api/blob/master/channels_api/mixins.py>`_




Permissions
-----------

channels-api by default has wierd permissions system. Everything that is
in binding's permission_classes needs to return True to allow an action:

.. code-block:: text

   permission_classes = (
       IsSuperuser,
       IsAuthor,
   )

So I need to be both superuser AND author to do soemthing. That's wierd!
Need to fork and rewrite.
