# -*- coding: utf-8 -*-
from django.db import models
from shop.models.cartmodel import CartItem
from shop.models.productmodel import Product
from shop.util.fields import CurrencyField

class OptionGroup(models.Model):
    '''
    A logical group of options
    Example:
    
    "Colors"
    '''
    name = models.CharField(max_length=255)
    slug = models.SlugField() # Used in forms for example
    description = models.CharField(max_length=255, blank=True, null=True)
    products = models.ManyToManyField(Product, related_name="option_groups", 
                                      blank=True, null=True)
    
    def __unicode__(self):
        return self.name
        
    def get_options(self):
        '''
        A helper method to retrieve a list of options in this OptionGroup
        '''
        options = Option.objects.filter(group=self)
        return options

class Option(models.Model):
    '''
    A product option. Examples:
    
    "Red": 10$
    "Blue": 5$
    ...
    '''
    name = models.CharField(max_length=255)
    price = CurrencyField() # Can be negative
    group = models.ForeignKey(OptionGroup)
        
    def __unicode__(self):
        return self.name
    
class CartItemOption(models.Model):
    '''
    This holds the relation to product options from the cart item.
    It allows to know which options where selected for what cartItem.
    
    Generally, this is used by 
    shop.cart.modifiers.product_options.ProductOptionsModifier
    '''
    cartitem = models.ForeignKey(CartItem)
    option = models.ForeignKey(Option)
    