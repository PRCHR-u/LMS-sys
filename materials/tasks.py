import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Course

logger = logging.getLogger(__name__)

@shared_task
def check_course_updates():
    # Эта задача останется для периодической проверки, если потребуется
    logger.info("Checking for course updates...")
    # Здесь можно добавить логику, если нужно

@shared_task
def send_update_email(user_email, course_title):
    """
    Асинхронная задача для отправки email об обновлении курса.
    """
    logger.info(f"Sending update email to {user_email} for course: {course_title}")
    try:
        send_mail(
            subject=f'Обновление курса: {course_title}',
            message=f'Материалы курса "{course_title}", на который вы подписаны, были обновлены.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,
        )
        logger.info(f"Email successfully sent to {user_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {user_email}: {e}")
