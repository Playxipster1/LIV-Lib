from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserProfileForm, CustomPasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Обработка ошибок
def custom_404(request, exception):
    """Запрашиваемая страница не существует"""
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    """Серверная ошибка 500"""
    return render(request, 'errors/500.html', status=500)

def custom_403(request, exception):
    """Нет доступа к страницке 403"""
    return render(request, 'errors/403.html', status=403)

def custom_400(request, exception):
    """Браузер отправил неверный запрос 400"""
    return render(request, 'errors/400.html', status=400)

def home(request):
    popular_products = Product.objects.filter(is_available=True)[:4]
    
    context = {
        'popular_products': popular_products,
        'categories': Category.objects.all(),
    }
    return render(request, 'home.html', context)

def product_list(request):
    """Список всех товаров с шаблоном"""
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    # Поиск товаров
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Сортировка товаров
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
    
    # Расчёт общей стоимости
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
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
    
    # Счёт общего количества
    total_quantity = cart.total_quantity()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_quantity': total_quantity,
            'message': f'Товар "{product.name}" добавлен в корзину'
        })
    
    messages.success(request, f'Товар "{product.name}" добавлен в корзину')
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
            messages.success(request, 'Количество товара обновлено')
        else:
            cart_item.delete()
            messages.success(request, 'Товар удален из корзины')
    
    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):
    """Удаление товара из корзины"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = Cart.objects.get(user=request.user)
        total_quantity = cart.total_quantity()
        return JsonResponse({
            'success': True,
            'cart_total_quantity': total_quantity,
            'message': 'Товар удален из корзины'
        })
    
    messages.success(request, f'Товар "{product_name}" удален из корзины')
    return redirect('cart_view')

@login_required
def clear_cart(request):
    """Очистка корзины"""
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    
    messages.success(request, 'Корзина очищена')
    return redirect('cart_view')

# Заказная часть
@login_required
def checkout(request):
    """Оформление заказа"""
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.select_related('product').all()
    except Cart.DoesNotExist:
        cart_items = []
    
    if not cart_items:
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('cart_view')
    
    # Расчёт общей стоимости
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)
    
    if request.method == 'POST':
        try:
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                shipping_address=f"{request.POST.get('city')}, {request.POST.get('address')}",
                phone_number=request.POST.get('phone'),
                email=request.POST.get('email'),
                notes=f"Способ оплаты: {request.POST.get('payment_method')}\nПолучатель: {request.POST.get('first_name')} {request.POST.get('last_name')}\nИндекс: {request.POST.get('postal_code')}"
            )
            
            # Создание элементов заказа
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            cart.items.all().delete()
            
            messages.success(request, f'Заказ #{order.id} успешно оформлен!')
            return redirect('checkout_success', order_id=order.id)
            
        except Exception as e:
            messages.error(request, f'Ошибка при оформлении заказа: {str(e)}')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'categories': Category.objects.all(),
    }
    return render(request, 'checkout.html', context)

@login_required
def checkout_success(request, order_id):
    """Страница успешного оформления заказа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.select_related('product').all()
    
    context = {
        'order': order,
        'order_items': order_items,
        'categories': Category.objects.all(),
    }
    return render(request, 'checkout_success.html', context)

@login_required
def order_list(request):
    """Список заказов пользователя"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """Детали заказа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def cancel_order(request, order_id):
    """Отмена заказа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Заказ #{order.id} отменен')
    else:
        messages.error(request, 'Невозможно отменить заказ в текущем статусе')
    
    return redirect('order_list')

@login_required
def edit_profile(request):
    """Редактирование профиля пользователя"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'categories': Category.objects.all(),
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def change_password(request):
    """Смена пароля пользователя"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'categories': Category.objects.all(),
    }
    return render(request, 'accounts/change_password.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)  # 👈 Желтое - ИГНОРИРУЕМ
        
        if user is not None:
            login(request, user)  # 👈 Желтое - ИГНОРИРУЕМ
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'accounts/login.html')