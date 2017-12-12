# -*- coding: utf-8 -*-

"""Console script for iota_balance_change_alert."""
from os.path import expanduser
home = expanduser("~")
default_config = ('%s/.ibca/config.ini' % home)
import click

@click.command()
@click.option('--config', default=default_config, type=click.Path(exists=True), help='Specify the path to your config file, by default it will look for %s'%(default_config))
def main(config):
  from iota_balance_change_alert import ibca
  ibca(click.format_filename(config))

if __name__ == "__main__":
    main()
