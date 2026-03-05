from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from allauth.account.models import EmailAddress

# 1. Define the Profile Inline
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile Info'
    fk_name = 'user'

# 2. Extend the Custom User Admin
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_reg_method')
    list_select_related = ('profile', )

    # This helper function shows the registration method in the user list
    def get_reg_method(self, instance):
        return instance.profile.registration_method
    get_reg_method.short_description = 'Registered Via'

    # Ensure the profile is saved when the user is saved in admin
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

# 3. EmailAddress Admin - Unregister the default allauth one and use ours
admin.site.unregister(EmailAddress)

@admin.register(EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ['email', 'user', 'verified', 'primary']
    list_filter = ['verified', 'primary']
    search_fields = ['email', 'user__username']
    readonly_fields = ['user']

# 4. Register the Models
admin.site.register(User, CustomUserAdmin)

