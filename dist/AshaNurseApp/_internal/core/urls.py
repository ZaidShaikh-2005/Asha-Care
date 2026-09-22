from django.urls import path

from . import views


urlpatterns = [
    path('', views.login_view, name='login'),

    path(
        'forgot-pin/',
        views.forgot_pin,
        name='forgot_pin'
    ),

    path(
        'reset-pin/<uidb64>/<token>/',
        views.reset_pin,
        name='reset_pin'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'add-village/',
        views.add_village,
        name='add_village'
    ),

    path(
        'add-family/',
        views.add_family,
        name='add_family'
    ),

    path(
        'family-list/',
        views.family_list,
        name='family_list'
    ),

    path(
        'family/<int:family_id>/',
        views.family_detail,
        name='family_detail'
    ),

    path(
        'village/<int:village_id>/house/<int:house_number>/',
        views.house_detail,
        name='house_detail'
    ),

    path(
        'add-member/',
        views.add_member,
        name='add_member'
    ),

    path(
        'member-list/',
        views.member_list,
        name='member_list'
    ),

    path(
        'member/<int:member_id>/',
        views.member_detail,
        name='member_detail'
    ),

    path(
        'member/<int:member_id>/edit/',
        views.edit_member,
        name='edit_member'
    ),

    # NEW
    path(
        'ayushman-pending/',
        views.ayushman_pending,
        name='ayushman_pending'
    ),

    path(
        'abha-pending/',
        views.abha_pending,
        name='abha_pending'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'ayushman-submitted/',
        views.ayushman_submitted,
        name='ayushman_submitted'
    ),

    path(
        'ayushman-pending/',
        views.ayushman_pending,
        name='ayushman_pending'
    ),

    path(
        'abha-pending/',
        views.abha_pending,
        name='abha_pending'
    ),
]