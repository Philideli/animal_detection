@echo off
setlocal EnableDelayedExpansion

if [%1]==[] goto usage

python "%1\object_detection\builders\model_builder_tf2_test.py" || goto :error
goto :eof

:usage
@echo Usage: %0 ^<PathToTFODAPi^>
exit /B 1
goto :EOF

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%