

Based on https://github.com/conbus/fbmq#example

Create a config.py as per https://github.com/conbus/fbmq/blob/master/example/config.py

* Facebook token: https://developers.facebook.com > Page/app > Messenger > 'Token Generation' > Page access token. Facebook generates this.

* Verify token: https://developers.facebook.com > Page/app > Webhooks > 'Edit Subscription'. You create this.

* Set env variables ARCHY_HOME and ARCHY_FILENAME (in Python Anywhere, this is done in wsgi.py).



Special keywords you can type to the bot to demo different features:

* image
* gif
* audio
* video
* file
* button
* generic
* receipt
* quick reply
* read receipt
* typing on
* typing off
* account linking