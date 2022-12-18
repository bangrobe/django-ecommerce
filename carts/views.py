from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from store.models import Product, Variation
from .models import Cart, CartItem
# Create your views here.
# _ tuc la private function
def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    print("cart id", cart)
    return cart

def add_cart(request, product_id):
    # Take current user
    current_user = request.user
    product = Product.objects.get(id=product_id)
    #If the user is authenticated
    if current_user.is_authenticated:
        product_variation = [] #empty list
        if request.method == "POST":
            print(request.POST)
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except Exception as e:
                    pass
        # Check cart item exists voi filter product=product, user=request.user            
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            # Get cart_item object to check variation
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            # check existing variations -> database -> increase quantity
            exsiting_variation_list = []
            id = []
            for item in cart_item:
                exsiting_variation = item.variation.all()
                exsiting_variation_list.append(list(exsiting_variation))
                id.append(item.id)
            # product_variation la mot list lay o buoc tren
            if product_variation in exsiting_variation_list:
                # increate the cart item quantity
                # Create a new cart item
                # current variation -> product variation
                # item_id -> database
                index = exsiting_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
            # cart_item.quantity += 1
                item.save()
        else:
            cart_item = CartItem.objects.create(product=product, user=current_user, quantity=1)
        
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
                print(cart_item)
            cart_item.save()
        return redirect('cartpage')

    # If user is not authenticated
    # Khac biet voi code o tren, chung ta ko dung dieu kien filter user=request.user ma dung dieu kien cart = cart_id
    else:
        product_variation = [] #empty list
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except Exception as e:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using cart_id present in session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()
        print(product_variation)

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        print(is_cart_item_exists)
        if is_cart_item_exists:
            # Get cart_item object to check variation
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # check existing variations -> database -> increase quantity
            exsiting_variation_list = []
            id = []
            for item in cart_item:
                exsiting_variation = item.variation.all()
                exsiting_variation_list.append(list(exsiting_variation))
                id.append(item.id)
            print(exsiting_variation_list)
            # product_variation la mot list lay o buoc tren
            if product_variation in exsiting_variation_list:
                # increate the cart item quantity
                # Create a new cart item
                # current variation -> product variation
                # item_id -> database
                index = exsiting_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
            # cart_item.quantity += 1
                item.save()
        else:
            cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
                print(cart_item)
            cart_item.save()
        return redirect('cartpage')


def remove_cart(request, product_id, cart_item_id ):
    
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cartpage')

def remove_cart_item(request, product_id, cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()

    return redirect('cartpage')

def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter( user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter( user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'cart_items': cart_items,
        'grand_total': grand_total
    }
    return render(request, 'checkout.html', context)