from django.contrib import admin
from .models import User, Listing, Bid, Comment, Watch, Category

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watch)
admin.site.register(Category)