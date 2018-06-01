# coding: utf-8

#         app: us.nspaces.ccc.profiles
#      módulo: apps.profile.admin
# descripción: Admin area
#       autor: Javier Sanchez Toledano
#       fecha: miércoles, 9 de agosto de 2017

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from profiles.models import Profile

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class ProfileAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email',  'get_site', 'get_position','is_staff',)
    list_select_related = ('profile',)
    list_filter = ('profile__site', 'profile__position')
    icon = '<i class="material-icons">face</i>'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

    def get_site(self, user):           # pylint: disable=R0201
        return user.profile.get_site_display()

    def get_position(self, user):
        return user.profile.get_position_display()


admin.site.register(User, ProfileAdmin)
