#-*- coding: utf-8 -*-
from shop.cart.cart_modifiers_base import BaseCartModifier
from shop_simplevariations.models import CartItemOption, CartItemTextOption

class ProductOptionsModifier(BaseCartModifier):
    '''
    This modifier adds an extra field to the cart to let the lineitem "know"
    about product options and their respective price.
    '''
    def process_cart_item(self, cart_item, state):
        '''
        This adds a list of price modifiers depending on the product options
        the client selected for the current cart_item (if any)
        '''
        selected_options = CartItemOption.objects.filter(cartitem=cart_item)
        for selected_opt in selected_options:
            option_obj = selected_opt.option
            price = option_obj.price * cart_item.quantity
            data = (option_obj.name, price)
            # Don't forget to update the running total!
            cart_item.current_total = cart_item.current_total + price
            cart_item.extra_price_fields.append(data)
        return cart_item
    
    
class TextOptionsModifier(BaseCartModifier):
    """
    This price modifier appends all the text options it finds in the database for
    a given cart item to the item's extra_price_fields.
    """
    def process_cart_item(self, cart_item, state):
        text_options = CartItemTextOption.objects.filter(cartitem=cart_item)
        for text_opt in text_options:
            price = text_opt.text_option.price
            data = ('%s: "%s"' % (text_opt.text_option.name,text_opt.text), price)
            # Don't forget to update the running total!
            cart_item.current_total = cart_item.current_total + price
            #Append to the cart_item's list now.
            cart_item.extra_price_fields.append(data)
        return cart_item
