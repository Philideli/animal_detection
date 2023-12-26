from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from animal_detection.app.backend.detection.views import run_detection, rerun_detection, detection_detail, detections_overview, image_original, image_result

urlpatterns = [
    path('detection/run', run_detection, name='detection-run'),
    path('detection/<int:id>/rerun', rerun_detection, name='detection-rerun'),
    path('detection/<int:id>/image/original', image_original, name='detection-image-original'),
    path('detection/<int:id>/image/result', image_result, name='detection-image-result'),
    path('detection/<int:id>', detection_detail, name='detection-image-result'),
    path('detections/overview', detections_overview, name='detection-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)