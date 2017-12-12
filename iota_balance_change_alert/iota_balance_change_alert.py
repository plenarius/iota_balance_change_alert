# coding=utf-8

from .alerts import *
import os
try:
    # >3.2
    from configparser import ConfigParser
except ImportError:
    # python27
    # Refer to the older SafeConfigParser as ConfigParser
    from ConfigParser import SafeConfigParser as ConfigParser

from iota import Iota, Address, BadApiResponse
from requests.exceptions import ConnectionError
from schedule import every, run_pending
from time import sleep

def check_balances(config, addresses, old_balances, first_run=False):
  config_uri = config.get('main', 'uri')
  report_body = ""
  txtmsg_body = ""
  api = Iota(config_uri)

  try:
    print("Attempting to connect to tangle via {uri}.".format(uri=config_uri))
    response = api.get_balances(addresses)
  except ConnectionError as e:
    print("Hm.  {uri} isn't responding.  Is the node running?".format(uri=config_uri))
    print(e)
  except BadApiResponse as e:
    print("Looks like {uri} isn't very talkative today ):".format(uri=config_uri))
    print(e)

  a = 0
  change_detected = False
  for addy in addresses:
    if old_balances[addy.address] != response['balances'][a] and not first_run:
      change_detected = True
      report_body = report_body + "The balance at address %s has changed from %i to %i.\n" % (addy.address, old_balances[addy.address], response['balances'][a])
      txtmsg_body = txtmsg_body + "Balance at %s changed from %i to %i.\n" % (addy.address[0:8], old_balances[addy.address], response['balances'][a])
    elif not first_run:
      report_body = report_body + "No changes detected."
    elif first_run:
      report_body = report_body + "Address: %s Balance: %i\n" % (addy.address, response['balances'][a])
    old_balances[addy.address] = response['balances'][a]
    a += 1

  if config.getboolean('twilio', 'active') and change_detected:
    twilio_alert(config, txtmsg_body)

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
    raise NoConfigError, config_path

  config.read(config_path)

  check_alert_modules(config)

  interval = float(config.get('main', 'interval'))
  config_addresses = config.get('main', 'addresses').split(',')
  addresses = []
  old_balances = {}

  print("Starting IOTA balance checker for the following address(es):")

  for input_address in config_addresses:
    addy = Address(input_address)
    addresses.append(addy)
    print("%s\n" % addy.address)
    old_balances[addy.address] = 0

  if config.getboolean('twilio', 'active'):
    print("Will send text message to %s if balance change detected." % config.get('twilio', 'to'))
  if config.getboolean('email', 'active'):
    print("Will send email to %s if balance change detected." % config.get('email', 'to'))

  check_balances(config, addresses, old_balances, True)

  every(interval).minutes.do(check_balances, config, addresses, old_balances)

  while 1:
      run_pending()
      sleep(1)
