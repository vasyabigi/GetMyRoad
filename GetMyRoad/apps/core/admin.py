from django.contrib import admin

from core.models import Category, Place, Trip, TripPoint

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'is_main', 'place_count')


class PlaceAdmin(admin.ModelAdmin):
	list_display = ('name', 'categories_display')

	def categories_display(self, obj):
		return ' - '.join([cat.name for cat in obj.categories.all()])

admin.site.register(Category, CategoryAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Trip)
admin.site.register(TripPoint)
