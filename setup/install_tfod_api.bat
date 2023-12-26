@echo off
setlocal EnableDelayedExpansion

IF "%1"=="" (
    echo No install path supplied
    exit 1
)
SET install_path=%1

IF "%2"=="" (
    SET protoc_download_link=https://github.com/protocolbuffers/protobuf/releases/download/v3.19.3/protoc-3.19.3-win64.zip
) ELSE (
    SET protoc_download_link=%2%
)

IF exist %install_path%\ (
    echo object_detection folder exists, no need to clone again
) ELSE (
    git clone "https://github.com/tensorflow/models" "%install_path%" || goto :error
)

IF not exist %install_path%\research\ IF exist %install_path%\help\ goto tfod_installed
goto restructure_files

:tfod_installed
echo Most likely Tensorflow Object detection folders are already structured.
echo If not, please check the folder where TFOD API should be installed for errors
goto install_packages

:restructure_files
FOR /d %%a IN ("%install_path%\*") DO (
    IF /i not "%%~nxa"=="research" (
        RD /S /Q "%%a" || goto :error
    )
)
RD /S /Q "%install_path%\.git\" || goto :error

FOR %%a IN ("%install_path%\*") DO (
    DEL "%%a" || goto :error
)
move "%install_path%\research\object_detection" "%install_path%\" || goto :error
move "%install_path%\research\slim" "%install_path%\" || goto :error
RD /S /Q  "%install_path%\research\" || goto :error
mkdir "%install_path%\help" || goto :error

:install_packages
cd %install_path% || goto :error
:: obtain absolute path
set install_path=%cd%

cd %install_path%\help
powershell.exe -Command "Invoke-WebRequest -OutFile protoc.zip %protoc_download_link%" || goto :error
tar -xf protoc.zip || goto :error
cd %install_path% || goto :error
.\help\bin\protoc.exe .\object_detection\protos\*.proto --python_out=. || goto :error
@REM for %%a in ("%install_path%\object_detection\protos\*.proto") do %install_path%\help\bin\protoc.exe %install_path%\object_detection\protos\%%a --python_out=%install_path%

copy %install_path%\object_detection\packages\tf2\setup.py %install_path%\ || goto :error
cd %install_path% || goto :error
python setup.py build || goto :error
python setup.py install || goto :error
cd %install_path%\slim || goto :error
@REM python -m pip install .
pip install -e . || goto :error

:: fix possible errors
pip install numpy || goto :error
pip install wrapt || goto :error
pip install opt_einsum || goto :error
pip install gast || goto :error
pip install astunparse || goto :error
pip install termcolor || goto :error
pip install tensorflow --upgrade || goto :error
pip uninstall -y google || goto :error
pip install google-cloud || goto :error
pip uninstall -y protobuf || goto :error
pip uninstall -y google || goto :error
pip install google || goto :error
pip install protobuf || goto :error
pip install tensorflow-gpu --upgrade || goto :error
pip install matplotlib || goto :error
pip install pyyaml || goto :error
pip install datasetinsights || goto :error
goto :EOF

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%