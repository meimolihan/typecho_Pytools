@echo off
color 0A

:MENU
color 0A
cls
echo ==============================
echo         Git ��Ŀ����ű�
echo ==============================
echo * 1. ��鵱ǰ�ֿ�״̬
echo.
echo * 2. ���͵�ǰ�ֿ����
echo.
echo * 3. ��ȡ��ǰ�ֿ����
echo.
echo * 4. ���ĵ�ǰ�ֿ��ǩ
echo ==============================
echo * 5. �������вֿ����
echo.
echo * 6. ��ȡ���вֿ����
echo ==============================
echo * 0. �˳�
echo ==============================
set /p choice="������������ (0 - 6): "



if "%choice%"=="1" goto CHECK_STATUS
if "%choice%"=="2" goto COMMIT_PUSH
if "%choice%"=="3" goto PULL_UPDATE
if "%choice%"=="4" goto UPDATE_GIT_TAG
if "%choice%"=="5" goto GIT_PUSH_ALL
if "%choice%"=="6" goto GIT_PUSH_ALL
if "%choice%"=="0" goto GIT_UPDATE_ALL

echo ��Чѡ�������ѡ��...
pause
goto MENU

echo ============= һ �� ���Git�ֿ�״̬ =================
:CHECK_STATUS
cls
echo ==============================
echo      ���ڼ��Git�ֿ�״̬...
echo ==============================
git status
echo ==============================
echo �����ɣ��������ʾȷ���ļ�״̬��
echo ==============================
pause
goto MENU

echo ============= �� ���ύ�����͸��� =================
:COMMIT_PUSH
cls
echo ========================================
echo              �ύ�����͸���
echo ========================================

set /p commit_msg=�������ύ��Ϣ��ֱ�ӻس�Ĭ��Ϊ "update"���� 
if "%commit_msg%"=="" set commit_msg=update

echo ========================================
echo ����������и��ĵ��ݴ���...
git add .
echo �����ɣ�

echo ========================================
echo �����ύ���ģ��ύ��ϢΪ��%commit_msg%
git commit -m "%commit_msg%"
echo �ύ��ɣ�

echo ========================================
echo �������͸��ĵ�Զ�ֿ̲�...
git push
echo ������ɣ����ĸ����ѳɹ�ͬ����Զ�ֿ̲⡣

echo ========================================
pause
goto MENU

echo ============= �� ����ȡԶ�̸��� =================
:PULL_UPDATE
cls
echo ========================================
echo          ���ڴ�Զ�ֿ̲���ȡ����...
echo ========================================
git pull
if %errorlevel% equ 0 (
    echo ��ȡ�ɹ������زֿ��������°汾��
) else (
    echo ��ȡʧ�ܣ����������Զ�ֿ̲��ַ�Ƿ���ȷ��
)
echo ========================================
pause
goto MENU


echo ============= �� ���ύ�����±�ǩ =================
:UPDATE_GIT_TAG
cls
REM ʹ�õ�ǰĿ¼��ΪGit�ֿ�·��
SET REPO_PATH=%CD%

echo ��ǰ�ֿ�·����%REPO_PATH%
echo ==============================

REM ����Ƿ�Ϊ��Ч��Git�ֿ�
IF NOT EXIST .git (
    echo ���󣺵�ǰĿ¼ %REPO_PATH% ����һ����Ч��Git�ֿ⡣
    echo ==============================
    pause
    EXIT /B 1
)

REM ������и��Ĳ��ύ
echo       ����������и���...
git add .
echo ==============================
echo �����ύ���ģ��ύ��ϢΪ "update"...
git commit -m "update"
echo ==============================

REM �����ύ��Զ�ֿ̲�
echo ���ڽ��ύ���͵�Զ�ֿ̲�...
git push
echo ==============================

REM ɾ�����ر�ǩ v1.0.0
echo ����ɾ�����ر�ǩ v1.0.0...
git tag -d v1.0.0
echo ==============================

REM ɾ��Զ�̱�ǩ v1.0.0
echo ����ɾ��Զ�̱�ǩ v1.0.0...
git push origin :refs/tags/v1.0.0
echo ==============================

REM ����ǩ�Ƿ�ɾ���ɹ�
echo ����ǩ v1.0.0 �Ƿ�ɾ���ɹ�...
git tag -l | findstr /I "v1.0.0" >nul
IF %ERRORLEVEL% EQU 0 (
    echo Զ�̱�ǩ v1.0.0 ɾ��ʧ�ܣ����ֶ���顣
) ELSE (
    echo Զ�̱�ǩ v1.0.0 ɾ���ɹ���
)
echo ==============================

REM �����±�ǩ
set /p tag_name=�������±�ǩ����ֱ�ӻس�Ĭ�ϱ�ǩ��Ϊ v1.0.0��:
if "%tag_name%"=="" (
    set tag_name=v1.0.0
)
echo ���ڴ����±�ǩ %tag_name%����ǩ��ϢΪ "Ϊ�����ύ�����´�����ǩ"...
git tag -a %tag_name% -m "Recreate tags for the latest submission"
echo ==============================

REM �����±�ǩ��Զ�ֿ̲�
echo ���ڽ��µı�ǩ %tag_name% ���͵�Զ�ֿ̲�...
git push origin %tag_name%
echo ==============================

REM ����ǩ�Ƿ����ͳɹ�
echo ����ǩ %tag_name% �Ƿ����ͳɹ�...
git tag -l | findstr /I "%tag_name%" >nul
IF %ERRORLEVEL% EQU 0 (
    echo ��ǩ %tag_name% ���ͳɹ���
) ELSE (
    echo ��ǩ %tag_name% ����ʧ�ܣ����ֶ���顣
)
echo ��ǰ�ֿ�·����%REPO_PATH%
echo ==============================
pause
goto MENU


echo ============= �� ���������вֿ���� =================
:GIT_PUSH_ALL
cls
:: ����Ҫ������Ŀ¼·�������޸�Ϊ���Ŀ��·����
set "target_dir=%~dp0"
echo Ŀ��Ŀ¼: %target_dir%

:: ����Ŀ��Ŀ¼�µ�������Ŀ¼
for /D %%i in ("%target_dir%\*") do (
    :: ����Ƿ���Git�ֿ�
    if exist "%%i\.git" (
        echo ============================================
        echo ���ڴ���ֿ�: %%~nxi
        echo ============================================
        
        :: ����ֿ�Ŀ¼
        pushd "%%i"
        
        :: ִ��Git����
        git add .
        git commit -m "update"
        git pull --rebase
        git push
        
        :: �����ϼ�Ŀ¼
        popd
        
        echo ============================================
        echo �ֿ� %%~nxi �������
        echo ============================================
        echo.
    ) else (
        echo ������Git�ֿ�: %%~nxi
    )
)

echo ������ЧGit�ֿ⴦�����
echo ============================================
pause
goto MENU 


echo ============= �� ����ȡ���вֿ���� =================
:GIT_UPDATE_ALL
cls
echo ============================================
echo      ����ɨ��Ŀ¼����Ŀ¼�е� Git �ֿ�...
echo ============================================
for /d /r "." %%d in (.) do (
    if exist "%%d\.git" (
        echo.
        echo ��⵽ Git �ֿ�: %%d
        cd /d "%%d"
        echo ������ȡԶ�̸���...
        git pull
        echo.
        echo ��ȡ���: %%d
        echo ============================================
    )
)

echo ɨ����ɣ�
pause
goto MENU 

echo ============================================
:EXIT_SCRIPT
echo ��лʹ�ã��ټ���
timeout /t 2 >nul
exit