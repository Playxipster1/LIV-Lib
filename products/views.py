from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Cart, CartItem

def home(request):
    """Главная страница с шаблоном"""
    popular_products = Product.objects.filter(is_available=True)[:4]
    categories = Category.objects.all()

    context = {
        'popular_products': popular_products,
        'categories': categories,
    }
    return render(request, 'home.html', context)

def product_list(request):
    """Список всех товаров с шаблоном"""
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    # Поиск
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Сортировка
    sort = request.GET.get("sort", "-created_at")
    if sort in ['name', 'price', '-price', '-created_at']:
        products = products.order_by(sort)
    context = {
        'products': products,
        'search_query': search_query,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)

def category_products(request, category_id):
    """Товары категории с шаблоном"""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_available=True)
    categories = Category.objects.all()

    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/category_products.html', context)

def about(request):
    """Страница о магазине"""
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'about.html', context)

@login_required
def cart_view(request):
    """Просмотр корзины"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'categories': Category.objects.all(),
    }
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, product_id):
    """Добавление товара в корзину"""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_quantity': cart.total_quantity(),
            'message': f'Товар "{product.name}" добавлен в корзину'
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

@login_required
def update_cart_item(request, item_id):
    """Обновление количества товара в корзине"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):
    """Удаление товара из корзины"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_quantity': request.user.cart.total_quantity(),
            'message': 'Товар удален из корзины'
        })
    
    return redirect('cart_view')

@login_required
def clear_cart(request):
    """Очистка корзины"""
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    
    return redirect('cart_view')

