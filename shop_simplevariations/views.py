from django.db.models import Q

from shop.models.cartmodel import CartItem
from shop.models.productmodel import Product
from shop.util.cart import get_or_create_cart
from shop.views.cart import CartDetails

from .models import Option, CartItemOption


class SimplevariationCartDetails(CartDetails):
    """Cart view that answers GET and POSTS request."""

    def post(self, *args, **kwargs):
        #it starts similar to the original post method
        product_id = self.request.POST['add_item_id']
        product_quantity = self.request.POST.get('add_item_quantity')
        if not product_quantity:
            product_quantity = 1
        product = Product.objects.get(pk=product_id)
        cart_object = get_or_create_cart(self.request)

        #now we need to find out which options have been chosen by the user
        option_ids = []
        for key in self.request.POST.keys():
            if key.startswith('add_item_option_group_'):
                option_ids.append(self.request.POST[key])

        #now we need to find out if there are any cart items that have the exact
        #same set of options
        qs = CartItem.objects.filter(cart=cart_object).filter(product=product)
        found_cartitem_id = None
        merge = False
        for cartitem in qs:
            # for each CartItem in the Cart, get it's options
            cartitemoptions = CartItemOption.objects.filter(
                cartitem=cartitem, option__in=option_ids)
            if len(cartitemoptions) == len(option_ids):
                found_cartitem_id = cartitem.id
                merge = True
                break

        #if we found a CartItem object that has the same options, we need
        #to select this one instead of just any CartItem that belongs to this
        #cart and this product.
        if found_cartitem_id:
            qs = CartItem.objects.filter(pk=found_cartitem_id)

        cart_item = cart_object.add_product(
            product, product_quantity, merge=merge, queryset=qs)
        cart_object.save()
        return self.post_success(product, cart_item)

    def post_success(self, product, cart_item):
        super(SimplevariationCartDetails, self).post_success(product, cart_item)
        #if this cart item already has an option set we don't need to do
        #anything because an existing option set will never change. if we got a
        #set of different options, that would become a new CartItem.
        if cart_item.cartitemoption_set.exists():
            return self.success()

        post = self.request.POST
        for key in self.request.POST.keys():
            if key.startswith('add_item_option_group_'):
                option = Option.objects.get(pk=int(post[key]))
                cartitem_option = CartItemOption()
                cartitem_option.cartitem = cart_item
                cartitem_option.option = option
                cartitem_option.save()
        return self.success()
