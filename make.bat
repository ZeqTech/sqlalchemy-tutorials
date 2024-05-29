@ECHO OFF

@REM Variables
SET command=%1

@REM Decide what to do from this Windows Equivalent of a makefile
if %command%==format GOTO :FORMAT
if %command%==format-check GOTO :FORMAT-CHECK

:FORMAT
    ruff format ep*
    GOTO :END

:FORMAT-CHECK
    ruff format ep* --check
    GOTO :END

:END
