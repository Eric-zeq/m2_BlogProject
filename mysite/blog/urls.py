from . import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from blog import views
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'posts',views.PostViewSet,basename='post')

urlpatterns= [
    path('',views.PostList.as_view(), name='home'),
    path('register/',views.register_request,name='register'),
    path('login/',views.login_request,name='login'),
    path('logout/',views.logout_request,name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/v1/',include(router.urls)),
     # 获取 Token（登录）DRF access 
     #access：短期有效令牌，用于授权 API 请求。
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 刷新 Token refresh Token
    #refresh：长期有效令牌，用于获取新的 access_token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 密码重置相关 URL password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # 解决/account/login,修改/admin/templates/registration/password_reset_complete.html  <a> 标签
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('<slug:slug>/',views.PostDetail.as_view(),name='post_detail'),
]

