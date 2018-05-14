from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tourmarks.models import User, Visit, Location

admin.site.register(User, UserAdmin)
admin.site.register(Location)
admin.site.register(Visit)
