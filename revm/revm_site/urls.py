from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    PasswordResetDoneView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from app_item.views import (
    CreateItemRequestViewSet,
    CreateItemOfferViewSet,
    GetItemCategoryViewSet,
)
from app_other.views import (
    CreateOtherRequestViewSet,
    CreateOtherOfferViewSet,
    GetOtherCategoryViewSet,
)
from app_transport_service.views import (
    CreateTransportServiceRequestViewSet,
    CreateTransportServiceOfferViewSet,
    GetTransportServiceCategoryViewSet,
)
from app_volunteering.views import (
    CreateVolunteeringOfferViewSet,
    CreateVolunteeringRequestViewSet,
    GetVolunteeringCategoryViewSet,
)

admin.site.site_title = settings.ADMIN_TITLE
admin.site.site_header = settings.ADMIN_TITLE
admin.site.index_title = settings.ADMIN_TITLE_SHORT


router = routers.DefaultRouter()
router.register(r"categories/item", GetItemCategoryViewSet, basename="item_categories")
router.register(r"categories/other", GetOtherCategoryViewSet, basename="other_categories")
router.register(r"categories/transport_service", GetTransportServiceCategoryViewSet, basename="transport_categories")
router.register(r"categories/volunteering", GetVolunteeringCategoryViewSet, basename="volunteering_categories")

router.register(r"request/item", CreateItemRequestViewSet, basename="item_request")
router.register(r"request/other", CreateOtherRequestViewSet, basename="other_request")
router.register(r"request/transport_service", CreateTransportServiceRequestViewSet, basename="transport_request")
router.register(r"request/volunteering", CreateVolunteeringRequestViewSet, basename="volunteering_request")

router.register(r"donate/item", CreateItemOfferViewSet, basename="item_resource")
router.register(r"donate/other", CreateOtherOfferViewSet, basename="other_resource")
router.register(r"donate/transport_service", CreateTransportServiceOfferViewSet, basename="transport_resource")
router.register(r"donate/volunteering", CreateVolunteeringOfferViewSet, basename="volunteering_resource")

urlpatterns = i18n_patterns(
    # Redirect admin to root; must be before the root url path
    path("admin/", RedirectView.as_view(url="/")),
    # URL patterns which accept a language prefix
    path("api/v1/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="swagger-ui"), name="swagger-ui"),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/", include(router.urls)),
    path("auth/", include("dj_rest_auth.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("impersonate/", include("impersonate.urls"), name="impersonate"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("password_reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password_reset/", PasswordResetView.as_view(), name="admin_password_reset"),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("", admin.site.urls, name="admin"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.ENABLE_DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
