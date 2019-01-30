from django.contrib import admin
from apps.snake.models import Snake


class SnakeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Snake, SnakeAdmin)
