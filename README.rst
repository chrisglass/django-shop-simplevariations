================================
django SHOP - Simple Variations
================================

This app's purpose is to provide a way to quickly create product variations for most simple cases.

It considers variations as a {label: value} entry in the cart modifiers, so it is perfect for things like
differently priced colors, or build-your-own computers for example.


Installation
============

This requires django SHOP to work (https://github.com/chrisglass/django-shop)

* Add the app to your installed app
* Add `shop.simplevariations.cart_modifier.ProductOptionsModifier` to your `SHOP_CART_MODIFIERS` setting.

Usage
======

* Create an Option group in the admin view
* Bind it to a product
* Add options and the corresponding price to the group.
* When a `CartItemOption` object is linked to a `CartItem`, the option's value will be added to the CartItem's price
  and a corresponding extra field willbe added to the Cart/Order.


Contributing
============

Feel free to fork this project on github, send pull requests...
development discussion happends on the django SHOP mailing list (django-shop@googlegroups.com)
