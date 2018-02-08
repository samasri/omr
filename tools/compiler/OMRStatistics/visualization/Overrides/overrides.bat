@set /p answer=In order to successfully create the overrides visualizations, all chrome instances not opened using this batch file should be closed. Would you like to close any open instances automatically? [y/n]:

@if %answer% == y goto kill
@if %answer% == Y goto kill
@if %answer% == yes goto kill
@if %answer% == YES goto kill
@goto no

:kill
@taskkill /F /IM chrome.exe /T > nul
goto open
:end

:no
@echo.
@echo Override visualizations might not be created under these conditions
@timeout 10
goto open
:end

:open
@SET CURRENTDIR="%cd%"
@start chrome --allow-file-access-from-files %CURRENTDIR%/overrides.html
:end

