@echo off
title NCLEX NGN Case Study Studio
echo ================================================================
echo   Starting NCLEX NGN Case Study Studio...
echo   Local server is running at http://localhost:3000
echo   All edits will save directly to cases-data.js on your hard drive!
echo ================================================================
echo.
cd /d "%~dp0"
start http://localhost:3000
node server.js
pause
