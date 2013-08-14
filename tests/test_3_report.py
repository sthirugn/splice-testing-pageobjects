#!/usr/bin/env python
import sys, re, time, os, logging, unittest, nose, selenium, webuitestcase
import tests as TESTS
import pageobjects.report as report
import pageobjects.filters as filters
from pageobjects.login import login, logout
from selenium_wrapper import SE
from selenium.common.exceptions import NoSuchElementException, TimeoutException

KATELLO = TESTS.ROLES.KATELLO

def setUpModule():
    '''Sanity test KATELLO role'''
    try: 
        KATELLO.url, KATELLO.username, KATELLO.password
    except AttributeError as e:
        raise unittest.SkipTest(e.message)


def tearDownModule():
    pass

class SanityReportTestCase(webuitestcase.WebuiTestCase):
    @classmethod
    def setUpClass(cls):
        SE.reset(url=KATELLO.url)
        SE.maximize_window()
        # log-in
        login(KATELLO.username, KATELLO.password)
        # run default report filter
        SE.get(KATELLO.url)
        cls.filters = filters.Filters()
        cls.default_filter = cls.filters.get_filter(filters.REDHAT_DEFAULT_FILTER_NAME)
        # save the report
        cls.default_report = cls.default_filter.run_report()
        

    @classmethod
    def tearDownClass(cls):
        SE.get(KATELLO.url)
        logout()

    def test_01_access_header(self):
        self.default_report.header

    def test_02_1_access_invalid_subscriptions(self):
        self.default_report.invalid_subscriptions

    def test_02_2_access_invalid_subscriptions_count(self):
        self.default_report.invalid_subscriptions.count

    def test_02_3_assert_invalid_subscriptions_count_nonempty(self):
        self.assertNotEqual(self.default_report.invalid_subscriptions.count.text, u"")

    def test_03_1_access_insufficient_subscriptions(self):
        self.default_report.insufficient_subscriptions

    def test_03_2_access_insufficient_subscriptions_count(self):
        self.default_report.insufficient_subscriptions.count

    def test_03_3_assert_insufficient_subscriptions_count_nonempty(self):
        self.assertNotEqual(self.default_report.insufficient_subscriptions.count.text, u"")

    def test_04_1_access_current_subscriptions(self):
        self.default_report.current_subscriptions

    def test_04_2_access_current_subscriptions_count(self):
        self.default_report.current_subscriptions.count

    def test_04_3_assert_current_subscriptions_count_nonempty(self):
        self.assertNotEqual(self.default_report.current_subscriptions.count.text, u"")
