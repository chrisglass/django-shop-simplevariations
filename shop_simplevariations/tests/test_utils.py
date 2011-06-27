"""Commonly used methods for shop_simplevariation tests."""
from shop.models.productmodel import Product

from ..models import CartItemOption, Option, OptionGroup


def create_fixtures(options=False):
    product = Product( name='product 1', slug='product-1', active=True,
                       unit_price=43)
    product.save()
    if not options:
        return
    option_group = OptionGroup(name='option group 1', slug='option-group-1')
    option_group.save()
    option_group.products.add(product)

    Option.objects.create(name='option 1', price='42', group=option_group)
    Option.objects.create(name='option 2', price='84', group=option_group)
