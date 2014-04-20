from twisted.trial import unittest, runner, reporter

'''Utils'''
from chat.test import test_parse_url
from chat.test import test_email
from chat.test import test_stress
from chat.test import test_utils
# from chat.test import test_protocol

'''Text Protocol'''
from chat.test.text_protocol import test_user
from chat.test.text_protocol import test_channel
from chat.test.text_protocol import test_channel_mode
from chat.test.text_protocol import test_channel_ban
from chat.test.text_protocol import test_channel_search
from chat.test.text_protocol import test_post


if __name__ == '__main__':
  results = reporter.TreeReporter()
  suite = unittest.TestSuite()

  tests = [
    # test_email,
    # test_protocol,
    # test_channel_search
    # test_post
    # test_parse_url,
    # test_stress,
    # test_utils,
    test_user
    # test_channel_mode,
    # test_channel,
    # test_channel_ban
  ]

  for alias in tests:
    alias = runner.TestLoader().loadModule(alias)
    suite.addTests(alias)

  suite.run(results)
  results.done()