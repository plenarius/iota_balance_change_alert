=========================
IOTA Balance Change Alert
=========================


.. image:: https://img.shields.io/pypi/v/iota_balance_change_alert.svg
        :target: https://pypi.python.org/pypi/iota_balance_change_alert

.. image:: https://img.shields.io/travis/plenarius/iota_balance_change_alert.svg
        :target: https://travis-ci.org/plenarius/iota_balance_change_alert

.. image:: https://readthedocs.org/projects/iota-balance-change-alert/badge/?version=latest
        :target: https://iota-balance-change-alert.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/plenarius/iota_balance_change_alert/shield.svg
     :target: https://pyup.io/repos/github/plenarius/iota_balance_change_alert/
     :alt: Updates


IOTA Balance Change Alert checks the balance on one or more addresses at a specified interval and alerts the user if there's any change in balance.


* Free software: MIT license
* Documentation: https://iota-balance-change-alert.readthedocs.io.


Features
--------

* Users can be alerted via text message, email, popup or system sound

Installation
------------
To install IOTA Balance Change Alert, run this command in your terminal:

.. code-block:: console

    $ pip install iota_balance_change_alert
    $ mkdir $HOME/.ibca && wget https://raw.githubusercontent.com/plenarius/iota_balance_change_alert/master/config.ini.example -O $HOME/.ibca/config.ini

If you want to be informed via text message you need to sign up for a free Twilio acccount at https://www.twilio.com and get their python library

.. code-block:: console

    $ pip install twilio

Usage
-----
Make sure to edit your config.ini to include your desired IOTA addresses and methods of alert. You do not need to specify the location of your config file if it's installed in $HOME/.ibca/config.ini.

.. code-block:: console

    $ iota_balance_change_alert --config path/to/config.ini

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

