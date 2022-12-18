from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from .views import _cart_id
def counter(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                # Lay cart_items la tat ca cac CartItem co user = request.user
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                # Neu ko authenticated lay cart_items la cac CartItem co cart = cart id dau tien
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                count += cart_item.quantity
        except Cart.DoesNotExist:
            count = 0
    
    return dict(count=count)