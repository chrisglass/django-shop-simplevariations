#-*- coding: utf-8 -*-
"""Tests for view classes of the shop_simplevariation application."""
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

from shop.models.cartmodel import CartItem

from .test_utils import create_fixtures


class SimplevariationCartDetailsTestCase(TestCase):
    """Tests for the SimplevariationCartDetails view class."""

    def test01_cart_is_callable(self):
        resp = self.client.get(reverse('cart'))
        self.assertEqual(resp.status_code, 200)

    def test02_post_adds_new_cart_item(self):
        create_fixtures()
        data = {
            'add_item_id': '1',
            'add_item_quantity': '2',
            'Add to cart': '',
        }
        resp = self.client.post(reverse('cart_item_add'), data=data)
        self.assertEqual(len(CartItem.objects.all()), 1)

    def test03_post_adds_different_cart_items_if_different_variations(self):
        create_fixtures(options=True)
        data = {
            'add_item_id': '1',
            'add_item_quantity': '2',
            'Add to cart': '',
            'add_item_option_group_1': '1',
        }
        resp = self.client.post(reverse('cart_item_add'), data=data)
        data.update({'add_item_option_group_1': '2'})
        resp = self.client.post(reverse('cart_item_add'), data=data)
        self.assertEqual(len(CartItem.objects.all()), 2)

    def test04_post_adds_to_same_cart_item_if_same_variations(self):
        create_fixtures(options=True)
        data = {
            'add_item_id': '1',
            'add_item_quantity': '2',
            'Add to cart': '',
            'add_item_option_group_1': '1',
        }
        resp = self.client.post(reverse('cart_item_add'), data=data)
        resp = self.client.post(reverse('cart_item_add'), data=data)
        self.assertEqual(len(CartItem.objects.all()), 1)
        self.assertEqual(CartItem.objects.all()[0].quantity, 4)
