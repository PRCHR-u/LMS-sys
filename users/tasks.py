import logging
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User

logger = logging.getLogger(__name__)

@shared_task
def deactivate_inactive_users():
    """
    Deactivates users who have not logged in for more than 30 days.
    """
    one_month_ago = timezone.now() - timedelta(days=30)
    
    # Find users who are active and haven't logged in for a month.
    # We also check if last_login is not null to avoid errors.
    inactive_users = User.objects.filter(
        is_active=True,
        last_login__isnull=False,
        last_login__lt=one_month_ago
    )
    
    count = inactive_users.count()
    if count > 0:
        logger.info(f"Found {count} inactive users to deactivate.")
        for user in inactive_users:
            user.is_active = False
            # We only update the is_active field
            user.save(update_fields=['is_active'])
            logger.info(f"Deactivated user: {user.email} (ID: {user.id})")
        logger.info(f"Successfully deactivated {count} users.")
    else:
        logger.info("No inactive users found to deactivate.")

