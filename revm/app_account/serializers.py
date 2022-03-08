from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "type",
            "first_name",
            "last_name",
            "business_name",
            "identification_no",
            "phone_number",
            "email",
            "password",
            "re_password",
        ]

    def validate_email(self, email):
        email = get_adapter().clean_email(email)

        if email and email_address_exists(email):
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."),
            )
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data["password"] != data["re_password"]:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            "type": self.validated_data.get("type", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "business_name": self.validated_data.get("business_name", ""),
            "identification_no": self.validated_data.get("identification_no", ""),
            "phone_number": self.validated_data.get("phone_number", ""),
            "email": self.validated_data.get("email", ""),
            "password": self.validated_data.get("password", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password"], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(detail=serializers.as_serializer_error(exc))
        user.set_password(self.cleaned_data["password"])
        user.type = self.cleaned_data["type"]
        user.business_name = self.cleaned_data["business_name"]
        user.identification_no = self.cleaned_data["identification_no"]
        user.save()
        # self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
