@echo off
echo 🔄 Pushing changes to GitHub...

git add .
git status
echo.
echo Enter your commit message:
set /p commit_msg=
git commit -m "%commit_msg%"
git push

echo.
echo ✅ Successfully pushed to GitHub!
pause
