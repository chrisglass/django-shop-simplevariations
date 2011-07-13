# -*- coding: utf-8 -*-
from django.db import models
from shop.models.cartmodel import CartItem
from shop.models.productmodel import Product
from shop.util.fields import CurrencyField

#===============================================================================
# Text options
#===============================================================================

class TextOption(models.Model):
    """
    This part of the option is selected by the merchant - it lets him/her "flag"
    a product as being able to receive some text as an option, and sets its
    price.
    """
    name = models.CharField(max_length=255, help_text="A name for this option - this will be displayed to the user")
    description = models.CharField(max_length=255, null=True, blank=True, help_text='A longer description for this option')
    price = CurrencyField(help_text='The price for this custom text') # The price
    #length = models.IntegerField() # TODO: make this limiting in the form
    products = models.ManyToManyField(Product, related_name='text_options')
    
    
    def __unicode__(self):
        return self.name

class CartItemTextOption(models.Model):
    """
    An option representing a bit of custom text a customer can define, i.e.
    for engraving or custom printing etc...
    The text is stored on the cart item because we assume we will not engrave or
    print many times the same bit of text. 
    
    If your use case is different, you should probably make a "text bit" Model
    """
    text = models.CharField(max_length=255) # The actual text the client input
    
    text_option = models.ForeignKey(TextOption)
    cartitem = models.ForeignKey(CartItem, related_name='text_option')
    
    def __unicode__(self):
        return self.text

#===============================================================================
# Multiple choice options
#===============================================================================

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

