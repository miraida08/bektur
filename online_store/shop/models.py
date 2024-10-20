from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    date_registered = models.DateField(auto_now_add=True, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    STATUS_CHOICES = (
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
        ('simple', 'Simple')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
         return f'{self.first_name} - {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=32)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    product_video = models.FileField (upload_to='vid/', verbose_name='Видео', null=True, blank=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.product_name

    def get_average_rating(self):
        ratings = self.Ratings.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0

class ProductPhotos(models.Model):
    product = models.ForeignKey(Product, related_name='product_photo', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')


class Rating(models.Model):
    product = models.ForeignKey(Product, related_name='Ratings' , on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Рейтинг')

    def __str__(self):
        return f'{self.product}-{self.user}-{self.stars} stars'



class Review(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    parent_review = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    created_name = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.product}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CarItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

