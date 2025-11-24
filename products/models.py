from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Категории товаров"""
    name = models.CharField(    
        max_length=100,         
        verbose_name="Название категории"
    )
    description = models.TextField(     
        blank=True,
        verbose_name="Описание"
    )
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"   

    def __str__(self):      
        return self.name

class Manufacturer(models.Model):   
    """Издатели"""
    name = models.CharField(
        max_length=100,
        verbose_name="Название"
    )
    country = models.CharField(
        max_length=100,
        verbose_name="Страна"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    class Meta:
        verbose_name = "Издатель"
        verbose_name_plural = "Издатели"

    def __str__(self):
        return self.name

class Product(models.Model):
    """Товар"""
    name = models.CharField(
        max_length=200,
        verbose_name="Название товара"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    price = models.DecimalField(
        max_digits=10,      
        decimal_places=2,   
        verbose_name="Цена"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
    )
    manufacturer = models.ForeignKey(   
        Manufacturer,
        on_delete=models.CASCADE,
        related_name="manufacturer",
        verbose_name="Издатель",
    )
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Доступно для продажи"
    )
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering =["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.price} руб."

class Cart(models.Model):
    """Корзина пользователя"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина {self.user.username}"

    def total_price(self):
        """Общая стоимость корзины"""
        return sum(item.total_price() for item in self.items.all())

    def total_quantity(self):
        """Общее количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())
        
class CartItem(models.Model):
    """Элемент корзины"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def total_price(self):
        """Общая стоимость позиции"""
        return self.product.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая стоимость')
    shipping_address = models.TextField(verbose_name='Адрес доставки')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Email')
    notes = models.TextField(blank=True, verbose_name='Примечания к заказу')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        return self.quantity * self.price