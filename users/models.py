from django.db import models
from django.conf import settings
from materials.models import Course, Lesson
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # Add any custom fields you need for your user model here
    phone = models.CharField(max_length=20, verbose_name='телефон', null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name='город', null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='аватарка', null=True, blank=True)

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveIntegerField()

    PAYMENT_METHODS = [
        ('cash', 'Наличные'), # This was already here, keeping it.
        ('transfer', 'Перевод на счет'),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    def __str__(self):
        if self.paid_course:
            return f"{self.user.email} paid for course {self.paid_course.title} on {self.payment_date}"
        elif self.paid_lesson:
            return f"{self.user.email} paid for lesson {self.paid_lesson.title} on {self.payment_date}"
        return f"{self.user.email} made a payment on {self.payment_date}"

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['-payment_date']

