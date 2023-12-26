from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from io import BytesIO
import os
import shutil
import traceback
import json

from animal_detection.app.backend.detection import cache
from animal_detection.app.backend.detection.constants import BOXES_COUNT_DEFAULT, SCORE_THRESHOLD_DEFAULT
from animal_detection.app.backend.detection.persistance.write import write_detection, delete_detection
from animal_detection.app.backend.detection.persistance.read import read_detection, get_all_detection_ids
from animal_detection.app.backend.detection.processing.preprocessing import get_new_detection_id, get_detection_dir_path, extract_params_from_request
from animal_detection.detect.detect_objects import execute as execute_detection


@csrf_exempt
def run_detection(request):
    if request.method == 'POST':  
        if not(request.FILES) or not('image' in request.FILES):
            return JsonResponse({"error": 'No image provided'}, status=400)
        
        file = request.FILES['image']
        try:
            detection_id = get_new_detection_id()
        except IndexError:
            return JsonResponse({"error": 'The maximum amount of detections has been reached. Please remove some of the older detections to run new detections'}, status=500)
        except:
            traceback.print_exc()
            return JsonResponse({"error": 'New detections cannot be processed'}, status=500)
                
        try:
            boxes_count, score_threshold = extract_params_from_request(request.POST)
        except:
            traceback.print_exc()
            return JsonResponse({"error": 'The provided parameters for detection (score threshold or boxes count) have invalid values'}, status=400)
            
        try:
            cache.write_bytes(file.name, file)
            detections, result_img = execute_detection(cache.get_full_path(file.name), boxes_count, score_threshold)
            write_detection(file, detections, result_img, detection_id, boxes_count, score_threshold)
            cache.remove_file(file.name)
            
            return JsonResponse({'id': detection_id}, status=200)
        except:
            detection_path = get_detection_dir_path(detection_id)
            if (os.path.isdir(detection_path)):
                shutil.rmtree(detection_path)
            traceback.print_exc()
            return JsonResponse({"error": 'Error occured during execution of object detection for given image'}, status=500)


@csrf_exempt
def rerun_detection(request, id):
    if request.method == 'PUT':  
        
        if not (id in get_all_detection_ids()):
            return JsonResponse({"error": 'No detection with given ID could be found'}, status=404)
        
        try:
            body = json.loads(request.body)
            boxes_count, score_threshold = extract_params_from_request(body)
        except:
            traceback.print_exc()
            return JsonResponse({"error": 'The provided parameters for detection (score threshold or boxes count) have invalid values'}, status=400)
         
        try:
            detection = read_detection(id, True)
            filename = detection.metadata['filename']
        except:
            traceback.print_exc()
            return JsonResponse({"error": 'Could not read detection with given ID'}, status=500)
        
        try:
            with open(detection.original_file_path, 'rb') as original_image_file:
                bytes_arr = original_image_file.read()
                
                reader1 = BytesIO(bytes_arr)
                reader2 = BytesIO(bytes_arr)
                file1 = File(reader1, 'copy_' +  filename)
                file2 = File(reader2, filename)
                cache.write_bytes(file1.name, file1)
                cache.write_bytes(file2.name, file2)
                
                detections, result_img = execute_detection(cache.get_full_path(file1.name), boxes_count, score_threshold)
                write_detection(file2, detections, result_img, id, boxes_count, score_threshold)
                cache.remove_file(file1.name)
                cache.remove_file(file2.name)
            
            return JsonResponse({'success': True}, status=200)
        except:
            traceback.print_exc()
            return JsonResponse({"error": 'Error occured during execution of object detection for given image'}, status=500)
        
        
@csrf_exempt
def detection_detail(request, id):
    if not (id in get_all_detection_ids()):
            return JsonResponse({"error": 'No detection with given ID could be found'}, status=404)
        
    if request.method == 'GET':
        try:
            detection = read_detection(id)
            return JsonResponse({'metadata': detection.metadata, 'objects': detection.detections_data_clean}, status=200)
        except:
            traceback.print_exc()
            return JsonResponse({"error": 'Could not read detection with given ID'}, status=500)
        
    if request.method == 'DELETE':
        try:
            delete_detection(id)
            return JsonResponse({'success': True}, status=200)
        except:
            traceback.print_exc()
            return JsonResponse({"error": 'Could not delete detection'}, status=500)
        

@csrf_exempt
def image_original(request, id):
    if not (id in get_all_detection_ids()):
        return JsonResponse({"error": 'No detection with given ID could be found'}, status=404)
    if request.method == 'GET':
        try:
            detection = read_detection(id, True)
            extension = detection.image_ext.replace('.', '')
            return HttpResponse(detection.original_image_file, content_type='image/' + extension)
        except:
            traceback.print_exc()
            return JsonResponse({"error": 'Could not retrieve image'}, status=500)
        
        
@csrf_exempt
def image_result(request, id):
    if not (id in get_all_detection_ids()):
        return JsonResponse({"error": 'No detection with given ID could be found'}, status=404)
    if request.method == 'GET':
        try:
            detection = read_detection(id, True)
            extension = detection.image_ext.replace('.', '')
            return HttpResponse(detection.result_image_file, content_type='image/' + extension)
        except:
            traceback.print_exc()
            return JsonResponse({"error": 'Could not retrieve image'}, status=500)
    

@csrf_exempt
def detections_overview(request):
    if request.method == 'GET':
        try:
            ids = get_all_detection_ids()
            result = []
            for id in ids:
                detection = read_detection(id)
                result.append({'id': id, 'metadata': detection.metadata, 'objects': detection.detections_data_clean})
            return JsonResponse({'detections': result}, status=200)
        except:
            traceback.print_exc()
            return JsonResponse({"error": 'Could not retrieve detections'}, status=500)

