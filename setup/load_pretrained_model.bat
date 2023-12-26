@echo off
setlocal EnableDelayedExpansion

IF "%1"=="" (
    echo No pretrained model directory provided
    exit 1
)
SET pt_models_dir=%1

IF "%2"=="" (
    echo No pretrained model name provided
    exit 1
)
SET pt_model_name=%2

IF "%3"=="" (
    SET pt_download_link=http://download.tensorflow.org/models/object_detection/tf2/20200711/%pt_model_name%.tar.gz
) ELSE (
    SET pt_download_link=%3%
)


IF not exist %pt_models_dir%\ mkdir %pt_models_dir%

cd %pt_models_dir%
powershell.exe -Command "Invoke-WebRequest -OutFile %pt_model_name%.tar.gz %pt_download_link%" || goto :error
tar -zxvf %pt_model_name%.tar.gz || goto :error
DEL %pt_model_name%.tar.gz || goto :error

goto :EOF

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%