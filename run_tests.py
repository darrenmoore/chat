from twisted.trial import unittest, runner, reporter

from chat.test import test_parse_url
from chat.test import test_user
from chat.test import test_channel
# from chat.test import test_post
# from chat.test import test_protocol
from chat.test import test_email
from chat.test import test_stress
from chat.test import test_utils


if __name__ == '__main__':
  results = reporter.TreeReporter()
  suite = unittest.TestSuite()

  test_parse_url = runner.TestLoader().loadModule(test_parse_url)
  suite.addTests(test_parse_url)

  # test_protocol = runner.TestLoader().loadModule(test_protocol)
  # suite.addTests(test_protocol)

  # test_email = runner.TestLoader().loadModule(test_email)
  # suite.addTests(test_email)

  test_stress = runner.TestLoader().loadModule(test_stress)
  suite.addTests(test_stress)

  test_utils = runner.TestLoader().loadModule(test_utils)
  suite.addTests(test_utils)

  test_user = runner.TestLoader().loadModule(test_user)
  suite.addTests(test_user)

  test_channel = runner.TestLoader().loadModule(test_channel)
  suite.addTests(test_channel)

  # test_post = runner.TestLoader().loadModule(test_post)
  # suite.addTests(test_post)

  suite.run(results)
  results.done()