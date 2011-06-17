#-*- coding: utf-8 -*-
from __future__ import with_statement
from decimal import Decimal
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from shop.cart.modifiers_pool import cart_modifiers_pool
from shop.models.cartmodel import Cart, CartItem
from shop.models.productmodel import Product
from shop.tests.utils.context_managers import SettingsOverride
from shop_simplevariations.models import OptionGroup, Option, CartItemOption


class ProductOptionsTestCase(TestCase):

    PRODUCT_PRICE = Decimal('100')
    AWESOME_OPTION_PRICE = Decimal('42') # The price of awesome?
    TEN_PERCENT = Decimal(10) / Decimal(100)

    def create_fixtures(self, quantity=1):
        cart_modifiers_pool.USE_CACHE=False

        self.user = User.objects.create(username="test",
                                        email="test@example.com",
                                        first_name="Test",
                                        last_name = "Toto")

        self.product = Product()
        self.product.name = "TestPrduct"
        self.product.slug = "TestPrduct"
        self.product.short_description = "TestPrduct"
        self.product.long_description = "TestPrduct"
        self.product.active = True
        self.product.unit_price = self.PRODUCT_PRICE
        self.product.save()

        self.ogroup = OptionGroup()
        self.ogroup.product = self.product
        self.ogroup.name = 'Test group'
        self.ogroup.save()

        self.option = Option()
        self.option.group = self.ogroup
        self.option.name = "Awesome"
        self.option.price = self.AWESOME_OPTION_PRICE
        self.option.save()

        self.cart = Cart()
        self.cart.user = self.user
        self.cart.save()

        self.cartitem = CartItem()
        self.cartitem.cart = self.cart
        self.cartitem.quantity = quantity
        self.cartitem.product = self.product
        self.cartitem.save()

    def test_01_no_options_yield_normal_price(self):
        self.create_fixtures()
        MODIFIERS = ['shop_simplevariations.cart_modifier.ProductOptionsModifier']
        with SettingsOverride(SHOP_CART_MODIFIERS=MODIFIERS):
            #No need to add a product there is already on in the fixtures
            self.cart.update()
            self.cart.save()
            sub_should_be = 1*self.PRODUCT_PRICE
            total_should_be = sub_should_be

            self.assertEqual(self.cart.subtotal_price, sub_should_be)
            self.assertEqual(self.cart.total_price, total_should_be)

    def test_02_awesome_option_increases_price_by_its_value(self):
        self.create_fixtures()

        c_item_option = CartItemOption()
        c_item_option.option = self.option
        c_item_option.cartitem = self.cartitem
        c_item_option.save()

        MODIFIERS = ['shop_simplevariations.cart_modifier.ProductOptionsModifier']
        with SettingsOverride(SHOP_CART_MODIFIERS=MODIFIERS):
            self.cart.update()
            self.cart.save()
            sub_should_be = (1*self.PRODUCT_PRICE) + (1*self.AWESOME_OPTION_PRICE)
            total_should_be = sub_should_be

            self.assertEqual(self.cart.subtotal_price, sub_should_be)
            self.assertEqual(self.cart.total_price, total_should_be)

    def test03_quantity_should_be_used_by_modifier(self):
        quantity = 2
        self.create_fixtures(quantity=quantity)

        c_item_option = CartItemOption()
        c_item_option.option = self.option
        c_item_option.cartitem = self.cartitem
        c_item_option.save()

        MODIFIERS = ['shop_simplevariations.cart_modifier.ProductOptionsModifier']
        with SettingsOverride(SHOP_CART_MODIFIERS=MODIFIERS):
            self.cart.update()
            self.cart.save()
            sub_should_be = (quantity*self.PRODUCT_PRICE) \
                          + (quantity*self.AWESOME_OPTION_PRICE)
            total_should_be = sub_should_be

            self.assertEqual(self.cart.subtotal_price, sub_should_be)
            self.assertEqual(self.cart.total_price, total_should_be)
