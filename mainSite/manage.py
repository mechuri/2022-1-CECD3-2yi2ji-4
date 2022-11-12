#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pyngrok import conf, ngrok



def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainSite.settings')
    try:
        from django.core.management import execute_from_command_line
        conf.get_default().auth_token = "2GxFR7UZzIsaZV4U2lsa3O6Fy99_4brTz4fvJ3pns2GTKR8BR"
        # ngrok.kill()
        ngrok.connect(8000)
        tunnels = ngrok.get_tunnels()
        for kk in tunnels: # Forwording 정보 출력
          print(kk)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
