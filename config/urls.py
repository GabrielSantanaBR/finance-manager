from django.contrib import admin
from django.urls import include, path
from core.views import health

urlpatterns = [
    path("health/", health, name="health"),
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("accounts/", include("accounts.urls")),
    path("expenses/", include("expenses.urls")),
    path("revenues/", include("revenues.urls")),
    path("approvals/", include("approvals.urls")),
    path("reports/", include("reports.urls")),
    path("exports/", include("exports.urls")),
    path("fixed-expenses/", include("fixed_expenses.urls")),
    path("ministries/", include("ministries.urls")),
    path("treasury/", include("treasury.urls")),
    path("system/", include("core.urls")),
]
