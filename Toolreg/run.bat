@echo off
set /p num_threads="nhap so tab chrome can chay 1-6 : "

REM Kiểm tra xem người dùng có nhập số từ 1 đến 6 hay không
if %num_threads% LSS 1 (
    echo "So luong luong chay tu 1 den 6. dang thoat..."
    exit /b
)
if %num_threads% GTR 6 (
    echo "so luong luong tu 1 den 6. dang thoat..."
    exit /b
)

REM Chạy các file Python theo số lượng luồng đã chọn
if %num_threads% GEQ 1 start "" python C:\Users\Admin\Music\Toolreg\reg1.py
if %num_threads% GEQ 2 start "" python C:\Users\Admin\Music\Toolreg\reg2.py
if %num_threads% GEQ 3 start "" python C:\Users\Admin\Music\Toolreg\reg3.py
if %num_threads% GEQ 4 start "" python C:\Users\Admin\Music\Toolreg\reg4.py
if %num_threads% GEQ 5 start "" python C:\Users\Admin\Music\Toolreg\reg5.py
if %num_threads% GEQ 6 start "" python C:\Users\Admin\Music\Toolreg\reg6.py