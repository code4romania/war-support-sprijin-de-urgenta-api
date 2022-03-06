from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from app_account.models import USERS_GROUP, CJCCI_GROUP, CNCCI_GROUP


# NOTE restricted for current user via admin `get_queryset` if current user in USER_GROUP, no restrictions for CNCCI
user_permissions = [
    "view_customuser",
    "view_itemoffer",
    "add_itemoffer",
    "change_itemoffer",
    "delete_itemoffer",
    "view_itemrequest",
    "add_itemrequest",
    "change_itemrequest",
    "delete_itemrequest",
    "view_resourcerequest",
    "add_resourcerequest",
    "change_resourcerequest",
    "delete_resourcerequest",
    "view_otheroffer",
    "add_otheroffer",
    "change_otheroffer",
    "delete_otheroffer",
    "view_otherrequest",
    "add_otherrequest",
    "change_otherrequest",
    "delete_otherrequest",
    "view_transportserviceoffer",
    "add_transportserviceoffer",
    "change_transportserviceoffer",
    "delete_transportserviceoffer",
    "view_transportservicerequest",
    "add_transportservicerequest",
    "change_transportservicerequest",
    "delete_transportservicerequest",
    "view_volunteeringoffer",
    "add_volunteeringoffer",
    "change_volunteeringoffer",
    "delete_volunteeringoffer",
    "view_volunteeringrequest",
    "add_volunteeringrequest",
    "change_volunteeringrequest",
    "delete_volunteeringrequest",
]

cjcci_permissions = cncci_permissions = [
    "add_customuser",
    "change_customuser",
    "delete_customuser",
    "view_customuser",
    "add_itemoffer",
    "change_itemoffer",
    "delete_itemoffer",
    "view_itemoffer",
    "add_itemrequest",
    "change_itemrequest",
    "delete_itemrequest",
    "view_itemrequest",
    "add_resourcerequest",
    "change_resourcerequest",
    "delete_resourcerequest",
    "view_resourcerequest",
    "add_subcategory",
    "change_subcategory",
    "view_subcategory",
    "add_category",
    "change_category",
    "view_category",
    "add_otheroffer",
    "change_otheroffer",
    "delete_otheroffer",
    "view_otheroffer",
    "add_otherrequest",
    "change_otherrequest",
    "delete_otherrequest",
    "view_otherrequest",
    "add_transportserviceoffer",
    "change_transportserviceoffer",
    "delete_transportserviceoffer",
    "view_transportserviceoffer",
    "add_transportservicerequest",
    "change_transportservicerequest",
    "delete_transportservicerequest",
    "view_transportservicerequest",
    "add_type",
    "change_type",
    "delete_type",
    "view_type",
    "add_volunteeringoffer",
    "change_volunteeringoffer",
    "delete_volunteeringoffer",
    "view_volunteeringoffer",
    "add_volunteeringrequest",
    "change_volunteeringrequest",
    "delete_volunteeringrequest",
    "view_volunteeringrequest",
]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users_group, _ = Group.objects.get_or_create(name=USERS_GROUP)
        users_group.permissions.set(
            Permission.objects.filter(codename__in=user_permissions).values_list("id", flat=True)
        )
        self.stdout.write(
            self.style.SUCCESS(f"'{USERS_GROUP}' group has been created and appropriate permissions were assigned")
        )

        cncci_group, _ = Group.objects.get_or_create(name=CNCCI_GROUP)
        cncci_group.permissions.set(
            Permission.objects.filter(codename__in=cncci_permissions).values_list("id", flat=True)
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"'{CNCCI_GROUP}' group has been created and appropriate permissions were assigned"
            )
        )

        cjcci_group, _ = Group.objects.get_or_create(name=CJCCI_GROUP)
        cjcci_group.permissions.set(
            Permission.objects.filter(codename__in=user_permissions).values_list("id", flat=True)
        )
        self.stdout.write(
            self.style.SUCCESS(f"'{CJCCI_GROUP}' group has been created and appropriate permissions were assigned")
        )
