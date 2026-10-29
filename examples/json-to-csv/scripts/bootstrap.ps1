param([string]$Python, [string]$Root, [switch]$Prepare)
$ErrorActionPreference = 'Stop'
if ([Environment]::OSVersion.Version.Build -lt 22000) { throw 'Windows 11 or newer build required; other systems untested' }
if (-not $Root) { $Root = Join-Path $env:LOCALAPPDATA 'portable-skill-creator' }
$Root = [IO.Path]::GetFullPath($Root)
if (-not [Environment]::Is64BitOperatingSystem -or [Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString() -ne 'X64') { throw 'Windows x64 required' }
function Test-Python([string]$Candidate) {
    if (-not $Candidate -or $Candidate -like '*WindowsApps*') { return $false }
    try {
        $r = & $Candidate -I -c "import sys; print('PSC_OK' if sys.version_info[:2]==(3,12) else 'PSC_WRONG') " 2>$null
        return ($LASTEXITCODE -eq 0 -and $r -eq 'PSC_OK')
    } catch { return $false }
}
$envPython = Join-Path $Root 'env\Scripts\python.exe'
$candidates = @($Python, $envPython)
foreach ($name in @('python','python3')) { $c = Get-Command $name -ErrorAction SilentlyContinue; if ($c) { $candidates += $c.Source } }
$chosen = $null
foreach ($candidate in $candidates) { if (Test-Python $candidate) { $chosen=$candidate; break } }
if (-not $chosen -and -not $Prepare) {
    @{status='needs_setup'; remedy='Run bootstrap.ps1 -Prepare or pass -Python with a real Python 3.12 executable'; cloud_api_called=$false} | ConvertTo-Json
    exit 3
}
if (-not $chosen) {
    $pin = Get-Content (Join-Path $PSScriptRoot '..\assets\runtime.json') -Raw | ConvertFrom-Json
    New-Item -ItemType Directory -Force -Path $Root | Out-Null
    $toolsRoot = Join-Path $Root ('uv-' + $pin.uv_version)
    $uv = Join-Path $toolsRoot 'uv.exe'
    if (-not (Test-Path -LiteralPath $uv)) {
        $zip = Join-Path $Root 'uv-download.zip'
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -UseBasicParsing -Uri $pin.url -OutFile $zip
        if ((Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant() -ne $pin.sha256) { throw 'Runtime checksum mismatch' }
        Expand-Archive -LiteralPath $zip -DestinationPath $toolsRoot -Force
        Remove-Item -LiteralPath $zip
    }
    $oldCache=$env:UV_CACHE_DIR; $oldPython=$env:UV_PYTHON_INSTALL_DIR; $oldConfig=$env:UV_NO_CONFIG
    try {
        $env:UV_CACHE_DIR=Join-Path $Root 'cache'; $env:UV_PYTHON_INSTALL_DIR=Join-Path $Root 'python'; $env:UV_NO_CONFIG='1'
        & $uv venv --python $pin.python (Join-Path $Root 'env')
        if ($LASTEXITCODE -ne 0) { throw 'Private environment creation failed; inspect network/policy and retry after repair' }
    } finally { $env:UV_CACHE_DIR=$oldCache; $env:UV_PYTHON_INSTALL_DIR=$oldPython; $env:UV_NO_CONFIG=$oldConfig }
    $chosen=$envPython
}
if (-not (Test-Python $chosen)) { throw 'Python executable did not pass the runtime check' }
@{status='ready';scope='creator_runtime_only';python=$chosen;cloud_api_called=$false} | ConvertTo-Json
