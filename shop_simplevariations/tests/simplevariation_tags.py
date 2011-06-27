#-*- coding: utf-8 -*-
"""Tests for templatetags of the shop_simplevariation application."""
from django.test.testcases import TestCase

from shop.models.productmodel import Product

from ..models import OptionGroup
from ..templatetags.simplevariation_tags import get_options, get_option_groups
from .test_utils import create_fixtures


class GetOptionGroupsTestCase(TestCase):
    """Tests for the get_option_groups templatetag."""
    def test01_should_return_all_option_groups_for_a_product(self):
        create_fixtures(options=True)
        product = Product.objects.all()[0]
        option_groups = get_option_groups(product)
        self.assertEqual(len(option_groups), 1)


class GetOptionsTestCase(TestCase):
    """Tests for the get_options templatetag."""
    def test01_should_return_all_options_for_an_option_group(self):
        create_fixtures(options=True)
        option_group = OptionGroup.objects.all()[0]
        options = get_options(option_group)
        self.assertEqual(len(options), 2)
