#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.options import TabularInline, ModelAdmin
from shop_simplevariations.models import Option, OptionGroup

class OptionInline(TabularInline):
    model = Option

class OptionGroupAdmin(ModelAdmin):
    inlines = [OptionInline,]

admin.site.register(OptionGroup, OptionGroupAdmin)