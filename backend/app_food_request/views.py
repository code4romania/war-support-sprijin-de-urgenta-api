from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.utils.translation import gettext_lazy as _
from revm_site.utils.views import CreateResourceViewSet


from app_food_request.models import FoodRequest
from app_food_request.forms import FoodRequestForm
from app_food_request.serializers import FoodRequestSerializer



class FoodRequestCreateView(SuccessMessageMixin, CreateView):
    template_name = "food_request_form.html"
    model = FoodRequest
    form_class = FoodRequestForm
    success_message = _("Your request has been registered.")
    failure_message = _(
        "There was an error submitting your request. Please try again or contact the site administrator."
    )

    def get_success_url(self):
        return reverse("food_request_form")


class FoodRequestViewSet(CreateResourceViewSet):
    serializer_class = FoodRequestSerializer
