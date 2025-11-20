@echo off
REM Install Elastic Beanstalk CLI (awsebcli) for current user (cmd.exe)
REM Usage: run from project root as: scripts\install_eb.cmd

echo Checking for Python launcher 'py'...
where py >nul 2>&1 || (
  echo Python launcher 'py' not found. Install Python 3 and ensure 'py' is on PATH.
  exit /b 1
)

echo Installing/Upgrading awsebcli (current user)...
py -3 -m pip install --upgrade --user awsebcli

echo Resolving user Scripts directory...
for /f "delims=" %%A in ('py -3 -c "import site,sys;print(site.USER_BASE)"') do set USERBASE=%%A
if not defined USERBASE (
  echo Could not resolve USER_BASE; falling back to %%USERPROFILE%%\AppData\Roaming\Python\Scripts
  set SCRIPTS=%USERPROFILE%\AppData\Roaming\Python\Scripts
) else (
  set SCRIPTS=%USERBASE%\Scripts
)

echo Scripts folder: %SCRIPTS%
if exist "%SCRIPTS%\eb.exe" (
  echo Found eb.exe in %SCRIPTS%
) else (
  echo WARNING: eb.exe not found in %SCRIPTS% - verify pip output above.
)

echo Adding Scripts folder to PATH for this session...
set PATH=%SCRIPTS%;%PATH%

echo Run 'eb --version' to verify installation.
eb --version 2>nul || echo If 'eb' is not found, add %SCRIPTS% to your user PATH and reopen the shell.

exit /b 0
