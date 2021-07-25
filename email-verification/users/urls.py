from django.urls import path

from .views import (
    SignUpView,
    CustomLoginView,
    ActivateView,
    CheckEmailView,
    SuccessView,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name="activate"),
    path('check-email/', CheckEmailView.as_view(), name="check_email"),
    path('success/', SuccessView.as_view(), name="success"),
]
