from django.db import models
from django.conf import settings
from materials.models import Course, Lesson

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField()
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    def __str__(self):
        if self.paid_course:
            return f"{self.user.email} paid for course {self.paid_course.title} on {self.payment_date}"
        elif self.paid_lesson:
            return f"{self.user.email} paid for lesson {self.paid_lesson.title} on {self.payment_date}"
        return f"{self.user.email} made a payment on {self.payment_date}"
