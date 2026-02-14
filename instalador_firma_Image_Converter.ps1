# instalador_firma_shutdownapp.ps1
$ErrorActionPreference = "Stop"

# === CONFIGURACIÓN ===
$certName     = "ShutdownAppDev"
$pfxPassword  = "Condorito123*#*?"
$publishFolder = "C:\Users\GAMT\Desktop\ShutdownApp - Publicar\ShutdownApp\publish"
$pfxPath = "$PSScriptRoot\$certName.pfx"
$cerPath = "$PSScriptRoot\$certName.cer"

# === FUNCIONES ===

function Get-Signtool {
    Write-Host "🔎 Buscando 'signtool.exe' en el sistema..." -ForegroundColor Cyan
    $signtool = Get-ChildItem -Path "C:\Program Files*" -Filter signtool.exe -Recurse -ErrorAction SilentlyContinue |
                Sort-Object FullName | Select-Object -First 1
    if (-not $signtool) {
        Write-Error "❌ No se encontró signtool.exe en tu sistema."
        exit 1
    }
    return $signtool.FullName
}

# === LIMPIEZA ANTERIOR ===
Write-Host "🧹 Eliminando certificados anteriores del almacén..." -ForegroundColor Cyan
Get-ChildItem -Path Cert:\CurrentUser\My   | Where-Object { $_.Subject -eq "CN=$certName" } | Remove-Item -ErrorAction SilentlyContinue
Get-ChildItem -Path Cert:\CurrentUser\Root | Where-Object { $_.Subject -eq "CN=$certName" } | Remove-Item -ErrorAction SilentlyContinue
Remove-Item -Path $pfxPath, $cerPath -ErrorAction SilentlyContinue -Force

# === CREAR CERTIFICADO CON DATOS PERSONALIZADOS ===
Write-Host "📜 Generando nuevo certificado auto-firmado con datos personalizados..." -ForegroundColor Green
$cert = New-SelfSignedCertificate -Type Custom `
  -Subject "CN=$certName, E=pharmakoz@gmail.com" `
  -KeyAlgorithm RSA -KeyLength 2048 -HashAlgorithm SHA256 `
  -KeyExportPolicy Exportable -CertStoreLocation "Cert:\CurrentUser\My" `
  -FriendlyName "$certName Certificate - Desarrollador Pablitus" `
  -NotAfter (Get-Date).AddYears(3)

# === EXPORTAR PFX Y CER ===
Write-Host "💾 Exportando .PFX y .CER..." -ForegroundColor Green
$securePass = ConvertTo-SecureString -String $pfxPassword -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $securePass
Export-Certificate -Cert $cert -FilePath $cerPath

# === INSTALAR EN ROOT ===
Write-Host "🔐 Instalando certificado en el almacén raíz..." -ForegroundColor Green
Import-Certificate -FilePath $cerPath -CertStoreLocation "Cert:\CurrentUser\Root" | Out-Null

# === UBICAR SIGNTOOL ===
$signtoolPath = Get-Signtool

# === FIRMAR TODOS LOS .EXE ===
Write-Host "🖊️ Firmando todos los archivos .exe en $publishFolder..." -ForegroundColor Green
$executables = Get-ChildItem -Path $publishFolder -Filter *.exe -Recurse

if ($executables.Count -eq 0) {
    Write-Warning "⚠️ No se encontraron archivos .exe en $publishFolder"
} else {
    foreach ($exe in $executables) {
        Write-Host "➡️ Firmando: $($exe.FullName)" -ForegroundColor Yellow
        & $signtoolPath sign /f $pfxPath /p $pfxPassword /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 "$($exe.FullName)"
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "❌ Error al firmar $($exe.Name)"
        } else {
            Write-Host "✅ $($exe.Name) firmado correctamente." -ForegroundColor Green
        }
    }
}
