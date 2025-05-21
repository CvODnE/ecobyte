import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecobyte.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Delete all users
User.objects.all().delete()
print("All users have been deleted successfully!") 