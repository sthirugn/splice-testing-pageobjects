#!/usr/bin/env python
import sys, re, time, os, logging, unittest, nose, selenium, webuitestcase
import tests as TESTS
import pageobjects.report as report
import pageobjects.filters as filters
from pageobjects.login import login, logout
from selenium_wrapper import SE
from selenium.common.exceptions import NoSuchElementException, TimeoutException

KATELLO = TESTS.ROLES.KATELLO

class SanityReportTestCase(webuitestcase.WebuiTestCase):
    @classmethod
    def setUpClass(cls):
        super(SanityReportTestCase, cls).setUpClass()
        cls.filters = filters.Filters()
        cls.filters.organisation_menu.current_organisation = 'ACME_Corporation'
        cls.default_filter = cls.filters.get_filter(filters.REDHAT_DEFAULT_FILTER_NAME)
        # save the report
        cls.default_report = cls.default_filter.run_report()

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

class InfoReportTestCase(webuitestcase.WebuiTestCase):
    @classmethod
    def setUpClass(cls):
        super(InfoReportTestCase, cls).setUpClass()
        cls.filters = filters.Filters()
        cls.filters.organisation_menu.current_organisation = 'ACME_Corporation'
        cls.default_filter = cls.filters.get_filter(filters.REDHAT_DEFAULT_FILTER_NAME)
        # save the report
        cls.report = cls.default_filter.run_report()
        cls.report_info = cls.report.info_report
        
    def test_01_filter_name(self):
        self.assertEqual(self.report_info.filter_name.field, "Red Hat Default Report")
        
    def test_02_filter_description(self):
        self.assertEqual(self.report_info.filter_description.field, "A default report that can be sent back to Red Hat representatives")
        
    def test_03_subscription_status(self):
        self.assertEqual(self.report_info.subscription_status.field, "Current, Invalid, Insufficient")
        
    def test_04_organizations(self):
        self.assertIn("ACME_Corporation", self.report_info.organizations.field)
        
    def test_05_hours(self):
        self.assertEqual(self.report_info.hours.field, "24")

    def test_06_lifecycle_state(self):
        self.assertEqual(self.report_info.lifecycle_state.field, "Active, Inactive")
