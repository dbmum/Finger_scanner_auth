from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_home, name="start"),
    path("scan/", views.show_scan, name="scan"),
    path("verify/", views.verify, name="verify"),
    path("manage_perks/", views.show_manage_perks, name="manage perks"),
    path("add_perk/", views.add_perk, name="manage perks"),
    path("manage_people/", views.show_manage_people, name="manage people"),
    path("add_person/", views.show_add_person, name="add person"),
    path("enroll_person/", views.enroll_new_person, name="add new person"),
    path("edit_person/<int:id>/", views.show_edit_person, name="edit person"),
    path("make_edit/<int:id>/", views.make_edit, name="make edit of person"),
    path("make_delete/<int:id>/", views.make_delete, name="make delete of person"),
    path("make_perk_delete/<int:id>/", views.delete_perk, name="make delete of perk")
]