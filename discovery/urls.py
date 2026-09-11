from django.urls import path
from .views import discovery_form, discovery_thanks

urlpatterns = [
    path("", discovery_form, name="discovery_form"),
    path("thanks/<uuid:reference>/", discovery_thanks, name="discovery_thanks"),
]
