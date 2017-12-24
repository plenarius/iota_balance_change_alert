# coding=utf-8

from .alerts import twilio_alert, email_alert, beep_alert, msgbox_alert
import os
try:
    # >3.2
    from configparser import ConfigParser
except ImportError:
    # python27
    # Refer to the older SafeConfigParser as ConfigParser
    from ConfigParser import SafeConfigParser as ConfigParser

from iota import Iota, Address, BadApiResponse, Hash
from requests.exceptions import ConnectionError
from schedule import every, run_pending
from time import sleep


def check_balances(config, addresses, old_balances, first_run=False):
    config_uri = config.get('main', 'uri')
    report_body = ''
    txtmsg = ''
    api = Iota(config_uri)
    response = None

    try:
        print('Connecting to tangle via {uri}.'.format(uri=config_uri))
        response = api.get_balances(addresses)
    except ConnectionError as e:
        print('{uri} is not responding.'.format(uri=config_uri))
        print(e)
    except BadApiResponse as e:
        print('{uri} is not responding properly.'.format(uri=config_uri))
        print(e)

    if response is None:
        exit(0)

    a = 0
    change_detected = False
    for addy in addresses:
        obaa = old_balances[addy.address]
        rba = response['balances'][a]
        if obaa != rba and not first_run:
            change_detected = True
            report_body = (
                '%s The balance at address %s has changed'
                ' from %i to %i.\n' % (report_body, addy.address, obaa, rba))
            txtmsg = (
                '%s Balance at %s changed from %i to %i.\n' % (
                    txtmsg, addy.address[0:8], obaa, rba))
        elif not first_run:
            report_body = report_body + 'No changes detected.'
        elif first_run:
            report_body = report_body + 'Address: %s Balance: %i\n' % (
                addy.address, rba)
        old_balances[addy.address] = rba
        a += 1

    if config.getboolean('twilio', 'active') and change_detected:
        twilio_alert(config, txtmsg)

    if config.getboolean('email', 'active') and change_detected:
        email_alert(config, report_body)

    if config.getboolean('beep', 'active') and change_detected:
        beep_alert()

    if config.getboolean('msgbox', 'active') and change_detected:
        msgbox_alert(report_body)

    print(report_body)


def ibca(config_path):
    config = ConfigParser()

    # check if the path is to a valid file
    if not os.path.isfile(config_path):
        raise ValueError

    config.read(config_path)

    interval = float(config.get('main', 'interval'))
    config_addresses = config.get('main', 'addresses').split(',')
    addresses = []
    old_balances = {}

    print('Starting IOTA balance checker for the following address(es):')

    for input_address in config_addresses:
        if (len(input_address) != Hash.LEN):
            print('Address %s is not %d characters. Skipping.' % (
                input_address, Hash.LEN))
            print('Make sure it does not include the checksum.')
            continue

        addy = Address(input_address)
        addresses.append(addy)
        print('%s' % addy.address)
        old_balances[addy.address] = 0
    if len(addresses) == 0:
        print('No valid addresses found, exiting.')
        exit(0)

    if config.getboolean('twilio', 'active'):
        print(
            'Will send text message to %s if balance change detected.'
            % config.get('twilio', 'to'))
    if config.getboolean('email', 'active'):
        print(
            'Will send email to %s if balance change detected.'
            % config.get('email', 'to'))

    check_balances(config, addresses, old_balances, True)

    every(interval).minutes.do(check_balances, config, addresses, old_balances)

    while 1:
        run_pending()
        sleep(1)
