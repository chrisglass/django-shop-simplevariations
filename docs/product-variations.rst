====================
Product variations
====================

One big complexity in shop systems is how to handle product variations: different
colors for the same product, different languages for books, or "build it 
youself" computers...

In Django SHOP we suggest you use the following method to define theses variations:

* Create an OptionGroup model, and bind it to your model
* Add some options: they simply consist of a description and price for the time
  being.
* Options will now be displayed as "normal" cart modifiers, and so will appear
  on the Order object and the "bill".
  