===============================
django SHOP - Simple Variations
===============================

This app's purpose is to provide a way to quickly create product variations for
most simple cases.

It considers variations as a {label: value} entry in the cart modifiers, so it
is perfect for things like differently priced colors, or build-your-own
computers for example.


Installation
============

This requires django SHOP to work (https://github.com/chrisglass/django-shop)

* Add the app to your INSTALLED_APPS in your settings.py
* Add `shop_simplevariations.cart_modifier.ProductOptionsModifier` to your
  `SHOP_CART_MODIFIERS` setting.
* Add `(r'^shop/cart/', include(simplevariations_urls)),` to your `urls.py`
  just before `(r'^shop/', include(shop_urls)),`

Your urls.py should look like this:

::

  from django.conf.urls.defaults import *
  from django.contrib import admin

  from shop import urls as shop_urls
  from shop_simplevariations import urls as simplevariations_urls


  admin.autodiscover()


  urlpatterns = patterns('',
      (r'^admin/', include(admin.site.urls)),
      (r'^shop/cart/', include(simplevariations_urls)),
      (r'^shop/', include(shop_urls)),
  )

Usage
=====

* Create an Option group in the admin view
* Bind it to a product
* Add options and the corresponding price to the group.
* When a `CartItemOption` object is linked to a `CartItem`, the option's value
  will be added to the CartItem's price and a corresponding extra field will be
  added to the Cart/Order.
* Override django-shop's `product_detail.html` template and add selection
  elements so that your users can select variations.


The product_detail.html template
================================
The simple `product_detail.html` that ships with the shop doesn't take
variations into consideration.

Therefore you need to override the template. django-shop-simplevariations
ships with two templatetags that help creating drop down lists so that a
customer can actually chose variation.

First make sure to load the simplevariation templatetags:

::

  {% load simplevariation_tags %}
  <h1>Product detail:</h1>
  ...

Next create the drop down lists of OptionsGroups and Options:

::

  <form method="post" action="{% url cart %}">{% csrf_token %}
  {% with option_groups=object|get_option_groups %}
    {% if option_groups %}
      <div>
        <h2>Variations:</h2>
        {% for option_group in option_groups %}
          <label for="add_item_option_group_{{ option_group.id }}">{{ option_group.name }}</label>
          {% with option_group|get_options as options %}
            <select name="add_item_option_group_{{ option_group.id }}">
              {% for option in options %}
                <option value="{{ option.id }}">{{ option.name }}</option>
              {% endfor %}
            </select>
          {% endwith %}
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}
  {% with text_options=object.text_options.all %}
    {% if text_options %}
      <div>
        <h2>Text options:</h2>
        {% for text_option in text_options %}
          <label for="add_item_text_option_{{ text_option.id }}">{{ text_option.name }}</label>
          <input type="text" name="add_item_text_option_{{ text_option.id }}" value=""/>
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}
  <input type="hidden" name="add_item_id" value="{{object.id}}">
  <input type="hidden" name="add_item_quantity" value="1">
  <input type="submit" value="Add to cart">
  </form>

Contributing
============

Feel free to fork this project on github, send pull requests...
development discussion happends on the django SHOP mailing list
(django-shop@googlegroups.com)
