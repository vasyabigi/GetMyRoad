from django.contrib import admin

from core.models import Category, Place, Trip, TripPoint

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'is_main', 'place_count')


class PlaceAdmin(admin.ModelAdmin):
	list_display = ('name', 'categories_display')

	def categories_display(self, obj):
		return ' - '.join([cat.name for cat in obj.categories.all()])


class TripInline(admin.StackedInline):
	model = TripPoint
	extra = 0


class TripAdmin(admin.ModelAdmin):
	list_display = ('name', 'user')
	inlines = [TripInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(TripPoint)
