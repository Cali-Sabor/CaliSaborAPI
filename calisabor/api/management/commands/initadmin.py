__author__ = 'luisangelvargas91@gmail.com'

from django.conf import settings
from django.core.management.base import BaseCommand
from api.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            for user in settings.ADMINS:
                username = user[0].replace(' ', '')
                email = user[1]
                password = 'p445w0rd'
                print('Creating User for %s (%s)' % (username, email))
                admin = User.objects.create_superuser(email=email, username=username, password=password)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
        else:
            print('Admin Users can only be initialized if no Users exist')