# Sports2D - ติดตั้ง environment สำหรับ Python 3.11
# วิธีใช้: เปิด PowerShell แล้วรัน .\setup_venv.ps1

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot

Write-Host "=== Sports2D Setup (Python 3.11) ===" -ForegroundColor Cyan
Write-Host ""

# ตรวจสอบ Python
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Host "ไม่พบคำสั่ง python กรุณาติดตั้ง Python 3.11" -ForegroundColor Red
    exit 1
}
$version = & python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
if (-not $version) {
    Write-Host "ไม่สามารถอ่านเวอร์ชัน Python ได้" -ForegroundColor Red
    exit 1
}
Write-Host "Python: $version" -ForegroundColor Green

# สร้าง venv ถ้ายังไม่มี
$venvPath = Join-Path $projectRoot ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "กำลังสร้าง .venv ..." -ForegroundColor Yellow
    & python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "สร้าง .venv เรียบร้อย" -ForegroundColor Green
} else {
    Write-Host "พบ .venv แล้ว" -ForegroundColor Green
}

# activate และติดตั้ง
$activate = Join-Path $venvPath "Scripts\Activate.ps1"
Write-Host "กำลังติดตั้งแพ็กเกจ (อาจใช้เวลาสักครู่) ..." -ForegroundColor Yellow
& $activate; pip install --upgrade pip -q; pip install -e . -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "ลองติดตั้งจาก requirements.txt ก่อน แล้วค่อย pip install -e ." -ForegroundColor Yellow
    & $activate; pip install -r requirements.txt; pip install -e .
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
Write-Host ""
Write-Host "ติดตั้งเสร็จแล้ว" -ForegroundColor Green
Write-Host ""
Write-Host "วิธีรัน GUI:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python -m Sports2D.gui_app" -ForegroundColor White
Write-Host ""
