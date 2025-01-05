from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import UserProfile, User
from users.forms import UserCreationForm, UserChangeForm

admin.site.unregister(Group)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    model=UserProfile
    search_fields = ('first_name', 'last_name')
    list_display = ('__str__', 'birthday', 'location', 'phone_number', 'active')
    ordering = ('-active', 'last_name', 'first_name')
    list_filter = ('active',)

@admin.register(User)
class UserAdminForm(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    autocomplete_fields = ('profile',)
    list_display = ("email", "is_staff", "is_active", "profile")
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "profile")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)