from django.contrib import admin

# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from django.contrib.auth import (
    authenticate,
    get_user_model

)

user = get_user_model()

class UserResource(resources.ModelResource):

    class Meta:
        model = user
        # fields = ('username', 'email', 'email2', 'password', 'last_name', 'first_name',)

class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    list_display = ('username', 'email', 'first_name', 'last_name', 'password')
    list_filter = ('is_staff', 'is_superuser')


admin.site.unregister(user)
# admin.site.register(user, MyUserAdmin)
admin.site.register(user, UserAdmin)