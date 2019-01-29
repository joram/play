from django.contrib import admin
from apps.authentication.models import User


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
