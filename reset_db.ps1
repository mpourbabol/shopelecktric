$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

$venvPython = Join-Path $ProjectRoot "venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    $venvPython = "python"
}

Write-Host "Dropping and recreating home_appliances_db..."
$sql = @"
IF DB_ID('home_appliances_db') IS NOT NULL
BEGIN
    ALTER DATABASE home_appliances_db SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE home_appliances_db;
END
CREATE DATABASE home_appliances_db;
"@
sqlcmd -S localhost -U ebi -P "aA1aA1aA1" -Q $sql
if ($LASTEXITCODE -ne 0) {
    Write-Error "sqlcmd failed. Ensure SQL Server is running and credentials are correct."
}

Write-Host "Running migrations..."
& $venvPython manage.py migrate
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Seeding home appliances data..."
& $venvPython manage.py seed_home_appliances
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Creating superuser ebi@example.com..."
$superuserScript = @"
from accounts.models import User
if not User.objects.filter(email='ebi@example.com').exists():
    User.objects.create_superuser('ebi@example.com', 'ebi', 'aA1aA1aA1')
    print('Superuser created.')
else:
    print('Superuser already exists.')
"@
$superuserScript | & $venvPython manage.py shell
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Compiling translations..."
& $venvPython manage.py compilemessages -l de --ignore=venv
if ($LASTEXITCODE -ne 0) {
    Write-Warning "compilemessages had issues; continuing..."
}

Write-Host "Running system check..."
& $venvPython manage.py check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Verifying product count..."
$countScript = "from home.models import Product; print(Product.objects.count())"
$count = $countScript | & $venvPython manage.py shell
Write-Host "Product count: $count"

Write-Host "Database reset complete."
