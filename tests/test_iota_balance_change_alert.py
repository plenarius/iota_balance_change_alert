#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `iota_balance_change_alert` package."""


import unittest
from click.testing import CliRunner

from iota_balance_change_alert import iota_balance_change_alert
from iota_balance_change_alert import cli


class TestIota_balance_change_alert(unittest.TestCase):
    """Tests for `iota_balance_change_alert` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'iota_balance_change_alert.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
