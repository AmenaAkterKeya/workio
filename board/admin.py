from django.contrib import admin
from .models import Board,List,Card,Member
# Register your models here.
admin.site.register(Board)
admin.site.register(List)
admin.site.register(Card)
admin.site.register(Member)