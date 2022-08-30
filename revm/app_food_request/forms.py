# from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Fieldset, Layout, Submit
from django import forms
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app_food_request.models import FoodRequest


class FoodRequestForm(forms.ModelForm):
    # captcha = ReCaptchaField(
    #     label="",
    # )

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
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Send request'), css_class='btn-blue'))
        self.helper.form_tag = False

        # # TODO: Add captcha support
        # if not settings.RECAPTCHA_PUBLIC_KEY:
        #     del self.fields["captcha"]
