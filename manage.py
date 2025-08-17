#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
print(f"DJANGO_SETTINGS_MODULE is set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

def main():
    """Run administrative tasks."""
    os.environ['DJANGO_SETTINGS_MODULE'] = 'LMS-sys.settings'

    # Add the project root directory to sys.path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, project_root)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
