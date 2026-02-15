$ErrorActionPreference = "Stop"

# ================= CONFIGURACION =================

$certName    = "Image_Converter_Dev"
$pfxPassword = "Condorito123*#*?"   # Cambia esto si deseas

$exePath = "I:\Proyectos Finales Python\Proyecto Image_Converter\Image_Converter\dist_installer\Image_Converter_Setup.exe"

$pfxPath = "$PSScriptRoot\$certName.pfx"
$cerPath = "$PSScriptRoot\$certName.cer"

# ================= FUNCIONES =================

function Get-Signtool {
    Write-Host "[INFO] Buscando signtool.exe..." -ForegroundColor Cyan
    $signtoolPath = $null

    $searchFolders = @(
        "C:\Program Files (x86)\Windows Kits\10\bin",
        "C:\Program Files\Windows Kits\10\bin",
        "C:\Program Files (x86)\Microsoft SDKs\Windows"
    )

    foreach ($folder in $searchFolders) {
        $found = Get-ChildItem -Path $folder -Filter signtool.exe -Recurse -ErrorAction SilentlyContinue |
                 Where-Object { $_.FullName -like "*\x64\*" } |
                 Sort-Object LastWriteTime -Descending |
                 Select-Object -First 1

        if ($found) {
            $signtoolPath = $found.FullName
            break
        }
    }

    if (-not $signtoolPath) {
        Write-Error "[ERROR] No se encontro signtool.exe. Instala el Windows SDK."
        exit 1
    }

    Write-Host "[OK] Signtool encontrado en: $signtoolPath" -ForegroundColor Green
    return $signtoolPath
}

# ================= LIMPIEZA =================
#
# Write-Host "[INFO] Eliminando certificados anteriores..." -ForegroundColor Cyan
# Get-ChildItem Cert:\CurrentUser\My |
#     Where-Object { $_.Subject -like "*CN=$certName*" } |
#     Remove-Item -ErrorAction SilentlyContinue
#
# Remove-Item $pfxPath, $cerPath -Force -ErrorAction SilentlyContinue
#
# ================= CREAR CERTIFICADO =================
#
# Write-Host "[INFO] Creando certificado autofirmado..." -ForegroundColor Green
# $cert = New-SelfSignedCertificate `
#     -Type CodeSigningCert `
#     -Subject "CN=Walter Pablo Tellez Ayala, O=Image Converter, E=pharmakoz@gmail.com, C=BO" `
#     -KeyAlgorithm RSA `
#     -KeyLength 2048 `
#     -HashAlgorithm SHA256 `
#     -KeyExportPolicy Exportable `
#     -CertStoreLocation "Cert:\CurrentUser\My" `
#     -FriendlyName "Image Converter Code Signing Certificate" `
#     -NotAfter (Get-Date).AddYears(5)
#
# ================= EXPORTAR =================
#
# Write-Host "[INFO] Exportando certificados..." -ForegroundColor Green
# $securePass = ConvertTo-SecureString $pfxPassword -AsPlainText -Force
#
# Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $securePass | Out-Null
# Export-Certificate    -Cert $cert -FilePath $cerPath | Out-Null
#
# ================= INSTALAR EN ROOT =================
#
# Write-Host "[INFO] Instalando certificado en Root (usuario actual)..." -ForegroundColor Green
# try {
#     Import-Certificate -FilePath $cerPath -CertStoreLocation "Cert:\CurrentUser\Root" | Out-Null
# } catch {
#     Write-Warning "[WARN] No se pudo instalar en Root. Ejecuta PowerShell como administrador si deseas confianza total."
# }

# ================= FIRMAR EXE =================

if (-not (Test-Path $exePath)) {
    Write-Error "[ERROR] No se encontro el ejecutable: $exePath"
    exit 1
}

$signtool = Get-Signtool

$exeFilename = Split-Path -Path $exePath -Leaf
Write-Host "[INFO] Firmando $exeFilename..." -ForegroundColor Yellow
& $signtool sign `
    /f $pfxPath `
    /p $pfxPassword `
    /fd SHA256 `
    /tr http://timestamp.digicert.com `
    /td SHA256 `
    "$exePath"

if ($LASTEXITCODE -ne 0) {
    Write-Error "[ERROR] Error durante la firma. Codigo: $LASTEXITCODE"
    exit 1
}

Write-Host "[OK] $exeFilename firmado correctamente." -ForegroundColor Green
Write-Host "[SUCCESS] Proceso finalizado con exito." -ForegroundColor Green
