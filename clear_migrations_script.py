import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connections

def run_script():
    with connections['default'].cursor() as cursor:
        cursor.execute("DELETE FROM django_migrations WHERE app IN ('users', 'admin')")
    print("Migration history for 'users' and 'admin' apps cleared.")

if __name__ == "__main__":
    run_script()