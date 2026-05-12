from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from app.views import CustomTokenObtainPairView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import (
    BalanceViewSet, DistrictViewSet, TeacherViewSet, GroupViewSet,
    DistrictStudentViewSet, StudentViewSet, PaymentViewSet, ExpenseViewSet,
    HomeworkViewSet, NewsViewSet, AttendanceViewSet, CustomScheduleViewSet
)
router = DefaultRouter()
router.register(r'balances', BalanceViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'district-students', DistrictStudentViewSet)
router.register(r'students', StudentViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'homeworks', HomeworkViewSet)
router.register(r'news', NewsViewSet)
router.register(r'attendances', AttendanceViewSet)
router.register(r'custom-schedules', CustomScheduleViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]