#-*- coding: utf-8 -*-
from shop.cart.cart_modifiers_base import BaseCartModifier
from shop_simplevariations.models import CartItemOption, CartItemTextOption

class ProductOptionsModifier(BaseCartModifier):
    '''
    This modifier adds an extra field to the cart to let the lineitem "know"
    about product options and their respective price.
    '''
    def add_extra_cart_item_price_field(self, cart_item):
        '''
        This adds a list of price modifiers dependeing on the product options
        the client selected for the current cart_item (if any)
        '''
        selected_options = CartItemOption.objects.filter(cartitem=cart_item)

        for selected_opt in selected_options:
            option_obj = selected_opt.option
            data = (option_obj.name, option_obj.price * cart_item.quantity)
            cart_item.extra_price_fields.append(data)

        return cart_item
    
    
class TextOptionsModifier(BaseCartModifier):
    """
    THis price modifier appends all the text options it finds in the database for
    a given cart item to the item's extra_price_fields.
    """
    def add_extra_cart_item_price_field(self, cart_item):
        text_options = CartItemTextOption.objects.filter(cartitem=cart_item)
        for text_opt in text_options:
            data = ('Text: "%s"', text_opt.text_option.price)
            cart_item.extra_price_fields.append(data)
