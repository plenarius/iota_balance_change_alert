# -*- coding: utf-8 -*-

"""Console script for iota_balance_change_alert."""

import click

@click.command()
def main(args=None):
  from iota_balance_change_alert import ibca
  ibca()

if __name__ == "__main__":
    main()
