# from captcha.fields import ReCaptchaField
# from crispy_forms.bootstrap import FormActions
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import HTML, Div, Fieldset, Layout, Submit
from django import forms
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app_food_request.models import FoodRequest


class FoodRequestForm(forms.ModelForm):
    # captcha = ReCaptchaField(
    #     label="",
    # )

    terms_and_conditions = forms.BooleanField(
        label=_(
            '<div class="toc">I have read and agree to the '
            '<a class="toc" href="/en/terms-and-conditions/">Terms and Conditions</a>'
            "</div>"
        ),
        required=True,
    )

    class Meta:
        model = FoodRequest
        fields = [
            "ngo_name",
            "county_coverage",
            "town",
            "address",
            "contact_person",
            "phone_number",
            "email",
            "backup_phone_number",
            "adult_vegetarian_portions",
            "child_vegetarian_portions",
            "adult_meat_portions",
            "child_meat_portions",
            "adult_restricted_portions",
            "adult_restriction_notes",
            "child_restricted_portions",
            "child_restriction_notes",
            "delivery_hours",
            "delivery_daily_frequency",
            "preferred_packaging",
            "notes",
            
            "terms_and_conditions",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # # TODO: Add captcha support
        # if not settings.RECAPTCHA_PUBLIC_KEY:
        #     del self.fields["captcha"]
