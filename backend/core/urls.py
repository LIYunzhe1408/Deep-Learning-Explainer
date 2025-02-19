# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('get_image/', views.get_image, name="get_image"),
    path('explain_image/', views.explain_image, name="explain_image"),
    path('get_seg_sample/', views.getSegSample, name="get_seg_sample"),
    path('get_seg_metrics/', views.getSemanticSegmentationMetrics, name="get_model_data"),
    path('get_option_pics/', views.getOptionPics, name="get_option_pics"),
    path('get_extraction_pics/', views.getExtractionImages, name="get_extraction_pics"),
    path('get_tree_images/', views.getTreeImages, name="get_tree_images"),
    path('get_local_explanation_images/', views.getLocalExplanationImages, name="get_local_explanation_images"),
    path('get_segmented_result/', views.getSegmentedResult, name="get_segmented_result"),
    path('get_explanation_comparison_images/', views.getExplanationComparisonImages, name="get_explanation_comparison_images"),
    path('get_explanation_metrics/', views.getExplanationMetrics, name="get_explanation_metrics"),



    path('add_user/', views.addUser, name="add_user"),
    path('search_log/', views.searchLog, name="search_log"),
    path('clear_logIn/', views.clearLogIn, name="clear_logIn"),
    path('update_profile/', views.updateProfile, name="update_profile"),
    path('delete_user/', views.deleteUser, name="delete_user"),
    path('check_loggedIn/', views.checkLoggedIn, name="check_loggedIn"),
]