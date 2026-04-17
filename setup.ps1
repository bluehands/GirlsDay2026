#Requires -Version 7.0
# ==============================================================================
# GirlsDay 2026 – Setup-Skript
# ==============================================================================
# Dieses Skript installiert alle noetigen Programme und richtet das Projekt ein.
# Ausfuehren mit:
#   irm https://raw.githubusercontent.com/bluehands/GirlsDay2026/main/setup.ps1 | iex
# ==============================================================================

# ------------------------------------------------------------------------------
# Schritt 0: Als Administrator neu starten, falls noetig
# ------------------------------------------------------------------------------
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]"Administrator")) {
    Write-Host "Administrator-Rechte benoetigt. Starte neu als Administrator..."
    if ($PSCommandPath) {
        Start-Process powershell "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    } else {
        # Wurde per "irm ... | iex" gestartet – Skript in temp-Datei speichern und neu starten
        $tempScript = "$env:TEMP\girlsday_setup.ps1"
        $MyInvocation.MyCommand.ScriptBlock | Out-File -FilePath $tempScript -Encoding UTF8
        Start-Process powershell "-ExecutionPolicy Bypass -File `"$tempScript`"" -Verb RunAs
    }
    exit
}

# ------------------------------------------------------------------------------
# Hilfsfunktionen
# ------------------------------------------------------------------------------

# Gibt einen gruenen OK-Text aus
function Write-OK($msg) {
    Write-Host "  [OK] $msg" -ForegroundColor Green
}

# Gibt einen gelben Info-Text aus
function Write-Info($msg) {
    Write-Host "  [..] $msg" -ForegroundColor Yellow
}

# Gibt einen roten Fehler-Text aus
function Write-Err($msg) {
    Write-Host "  [!!] $msg" -ForegroundColor Red
}

# Aktualisiert $env:PATH aus der Registry (nach winget-Installationen)
function Refresh-Path {
    $machinePath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
    $userPath    = [Environment]::GetEnvironmentVariable("PATH", "User")
    $env:PATH    = "$machinePath;$userPath"
}

# Installiert ein Programm via winget, falls der Test-Befehl fehlschlaegt
function Install-IfMissing {
    param(
        [string]$TestCommand,               # z.B. "git --version"
        [string]$WingetId,                  # z.B. "Git.Git"
        [string]$DisplayName,               # z.B. "Git"
        [string]$Scope = ""                 # "machine" fuer systemweite Installation (alle Benutzer)
    )
    Write-Info "Pruefe $DisplayName..."
    $result = $null
    try {
        $result = Invoke-Expression $TestCommand 2>&1
    } catch {}

    if ($LASTEXITCODE -eq 0 -and $result) {
        Write-OK "$DisplayName ist bereits installiert: $($result | Select-Object -First 1)"
    } else {
        Write-Info "$DisplayName wird installiert (winget: $WingetId)..."
        $wingetArgs = @("install", "--id", $WingetId, "--silent", "--accept-package-agreements", "--accept-source-agreements")
        if ($Scope) {
            $wingetArgs += @("--scope", $Scope)
        }
        winget @wingetArgs
        if ($LASTEXITCODE -ne 0) {
            Write-Err "$DisplayName konnte nicht installiert werden (winget Exit-Code: $LASTEXITCODE)."
            Write-Err "Bitte $DisplayName manuell installieren und das Skript erneut ausfuehren."
            Read-Host "Enter druecken zum Beenden"
            exit 1
        } else {
            Write-OK "$DisplayName wurde installiert."
            Refresh-Path
        }
    }
}

# Konvertiert einen SecureString in einen normalen String
function ConvertFrom-SecureStringPlain([SecureString]$secure) {
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
    }
}

# ------------------------------------------------------------------------------
# Konfiguration
# ------------------------------------------------------------------------------
$repoUrl  = "https://github.com/bluehands/GirlsDay2026.git"
$repoPath = "C:\GirlsDay2026"
$venvPath = "$repoPath\.venv"

# ------------------------------------------------------------------------------
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  GirlsDay 2026 – Setup startet!"           -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ------------------------------------------------------------------------------
# Schritt 1: Voraussetzungen installieren
# ------------------------------------------------------------------------------
Write-Host "--- Schritt 1: Programme installieren ---" -ForegroundColor Cyan

# winget-Quellen aktualisieren (verhindert "Fehler beim Oeffnen der Quelle(n)")
Write-Info "Aktualisiere winget-Quellen..."
winget source update
Write-OK "winget-Quellen aktualisiert."

Install-IfMissing "git --version"      "Git.Git"                     "Git"

# Python: falls eine per-User-Installation des aktuellen (Admin-)Benutzers
# existiert, diese zuerst entfernen. Der Python-Installer wechselt sonst in
# den "Modify"-Modus und scheitert beim Wechsel zur Machine-Installation (0x80070643).
# Hinweis: $env:LOCALAPPDATA zeigt auf das Profil des aktuell eingeloggten
# (Admin-)Benutzers – das ist korrekt, denn genau diese Installation stoert.
$pythonUserPath = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
if (Test-Path $pythonUserPath) {
    Write-Info "Per-User Python 3.11 gefunden unter aktuellem Benutzerprofil. Wird deinstalliert..."
    winget uninstall --id Python.Python.3.11 --silent --accept-source-agreements
    Write-OK "Per-User Python 3.11 wurde deinstalliert."
}

Install-IfMissing "py -3.11 --version" "Python.Python.3.11"          "Python 3.11"          -Scope "machine"
Install-IfMissing "code --version"     "Microsoft.VisualStudioCode"  "Visual Studio Code"   -Scope "machine"

# ------------------------------------------------------------------------------
# Schritt 2: Repository klonen oder aktualisieren
# ------------------------------------------------------------------------------
Write-Host ""
Write-Host "--- Schritt 2: Projekt-Dateien holen ---" -ForegroundColor Cyan

if (-Not (Test-Path $repoPath)) {
    Write-Info "Klone Repository nach $repoPath..."
    git clone $repoUrl $repoPath
    if ($LASTEXITCODE -ne 0) {
        Write-Err "Repository konnte nicht geklont werden. Bitte Internet-Verbindung pruefen."
        Read-Host "Enter druecken zum Beenden"
        exit 1
    }
    Write-OK "Repository wurde geklont."
} else {
    Write-Info "Ordner $repoPath existiert bereits. Aktualisiere..."
    git -C $repoPath pull
    Write-OK "Repository ist aktuell."
}

# Sicherstellen dass alle lokalen Benutzer (Schuelerinnen) den Ordner lesen
# und ausfuehren koennen. Das Skript laeuft als Admin, der Ordner gehoert dem
# Admin – ohne explizite Rechte koennte der Student-Account keinen Zugriff haben.
Write-Info "Setze Zugriffsrechte auf $repoPath fuer alle Benutzer..."
icacls $repoPath /grant "Users:(OI)(CI)RX" /T /Q
Write-OK "Zugriffsrechte gesetzt (Benutzer: Lesen + Ausfuehren)."

# ------------------------------------------------------------------------------
# Schritt 3: Python Virtual Environment erstellen
# ------------------------------------------------------------------------------
Write-Host ""
Write-Host "--- Schritt 3: Python-Umgebung einrichten ---" -ForegroundColor Cyan

# System-Python suchen (installiert nach C:\Program Files durch --scope machine).
# py -3.11 wuerde ggf. eine per-User-Installation nehmen, deren Pfad in pyvenv.cfg
# landet und auf anderen Benutzerkonten nicht existiert.
$pythonExe = "C:\Program Files\Python311\python.exe"
if (-Not (Test-Path $pythonExe)) {
    # Fallback: py launcher fragen
    $pythonExe = (py -3.11 -c "import sys; print(sys.executable)" 2>&1).Trim()
}
if (-Not (Test-Path $pythonExe)) {
    Write-Err "Python 3.11 nicht gefunden unter $pythonExe. Bitte Setup erneut ausfuehren."
    Read-Host "Enter druecken zum Beenden"
    exit 1
}
Write-OK "Verwende Python: $pythonExe"

if (-Not (Test-Path $venvPath)) {
    Write-Info "Erstelle virtuelle Python-Umgebung..."
    & $pythonExe -m venv $venvPath
    Write-OK "Virtuelle Umgebung erstellt."
} else {
    Write-OK "Virtuelle Umgebung existiert bereits."
}

# ------------------------------------------------------------------------------
# Schritt 4: Python-Pakete installieren
# ------------------------------------------------------------------------------
Write-Host ""
Write-Host "--- Schritt 4: Python-Pakete installieren ---" -ForegroundColor Cyan
Write-Info "Installiere Pakete aus requirements.txt (kann einige Minuten dauern)..."

# Pakete installieren. openai ist bewusst nicht in requirements.txt, damit
# crewai seinen bevorzugten openai-Stand installieren kann ohne Konflikt.
& "$venvPath\Scripts\pip.exe" install -r "$repoPath\requirements.txt"

if ($LASTEXITCODE -ne 0) {
    Write-Err "Paket-Installation fehlgeschlagen. Bitte Fehlermeldung oben pruefen."
    Read-Host "Enter druecken zum Beenden"
    exit 1
}

# openai auf die getestete Version erzwingen.
# crewai 1.8.1 zieht openai>=1.83 mit, aber diese Version bricht crewai
# wegen eines entfernten Typs (ChatCompletionMessageFunctionToolCall).
# --force-reinstall --no-deps ueberschreibt nur openai ohne andere Pakete anzufassen.
Write-Info "Setze openai auf getestete Version zurueck (openai==1.76.2)..."
& "$venvPath\Scripts\pip.exe" install openai==1.76.2 --force-reinstall --no-deps

if ($LASTEXITCODE -ne 0) {
    Write-Err "openai-Downgrade fehlgeschlagen. Bitte Fehlermeldung oben pruefen."
    Read-Host "Enter druecken zum Beenden"
    exit 1
}
Write-OK "Alle Pakete wurden installiert (openai==1.76.2 erzwungen)."

# ------------------------------------------------------------------------------
# Schritt 5: VS Code Einstellungen schreiben
# ------------------------------------------------------------------------------
Write-Host ""
Write-Host "--- Schritt 5: VS Code konfigurieren ---" -ForegroundColor Cyan

$vscodeDir = "$repoPath\.vscode"
if (-Not (Test-Path $vscodeDir)) {
    New-Item -ItemType Directory -Path $vscodeDir | Out-Null
}

$settings = @{
    "python.defaultInterpreterPath" = "$venvPath\Scripts\python.exe"
} | ConvertTo-Json -Depth 3

Set-Content -Path "$vscodeDir\settings.json" -Value $settings -Encoding UTF8
Write-OK "VS Code wurde konfiguriert (Python-Interpreter zeigt auf .venv)."

# extensions.json: VS Code zeigt beim ersten Oeffnen ein Popup
# "Empfohlene Erweiterungen installieren?" fuer den jeweiligen Benutzer.
$extensions = @{
    recommendations = @(
        "ms-python.python",
        "ms-toolsai.jupyter"
    )
} | ConvertTo-Json -Depth 3

Set-Content -Path "$vscodeDir\extensions.json" -Value $extensions -Encoding UTF8
Write-OK "Erweiterungs-Empfehlungen geschrieben (.vscode\extensions.json)."

# ------------------------------------------------------------------------------
# Schritt 6: API-Schluessel konfigurieren (.env Datei)
# ------------------------------------------------------------------------------
Write-Host ""
Write-Host "--- Schritt 6: API-Schluessel konfigurieren ---" -ForegroundColor Cyan

# API-Schluessel werden in C:\GirlsDay2026\.env geschrieben.
# Diese Datei gilt fuer alle Benutzer auf diesem Computer, da das Verzeichnis
# C:\GirlsDay2026 fuer alle Benutzer lesbar ist (siehe Schritt 2).
# Die .env Datei ist in .gitignore eingetragen und wird nicht ins Repo gepusht.

$envFile = "$repoPath\.env"

# Liest einen Wert aus der .env Datei
function Get-EnvValue([string]$key) {
    if (Test-Path $envFile) {
        $line = Get-Content $envFile | Where-Object { $_ -match "^$key=" } | Select-Object -First 1
        if ($line) { return $line.Substring($key.Length + 1) }
    }
    return $null
}

# Schreibt oder aktualisiert einen Schluessel in der .env Datei
function Set-EnvValue([string]$key, [string]$value) {
    if (Test-Path $envFile) {
        $lines = Get-Content $envFile
        if ($lines -match "^$key=") {
            $lines = $lines -replace "^$key=.*", "$key=$value"
            Set-Content $envFile $lines -Encoding UTF8
        } else {
            Add-Content $envFile "`n$key=$value" -Encoding UTF8
        }
    } else {
        Add-Content $envFile "$key=$value" -Encoding UTF8
    }
}

# OTEL_SDK_DISABLED immer setzen (deaktiviert CrewAI-Telemetrie)
Set-EnvValue "OTEL_SDK_DISABLED" "true"
Write-OK "OTEL_SDK_DISABLED=true in .env gesetzt."

# Hilfsfunktion: Fragt nach einem API-Schluessel
function Set-ApiKey {
    param(
        [string]$KeyName,
        [string]$Description,
        [bool]$Optional = $false
    )

    $existing = Get-EnvValue $KeyName

    Write-Host ""
    if ($existing) {
        Write-Host "  $KeyName ist bereits gesetzt." -ForegroundColor Green
        Write-Host "  Neuen Wert eingeben zum Ueberschreiben, oder Enter druecken zum Beibehalten:" -NoNewline
    } else {
        if ($Optional) {
            Write-Host "  $KeyName ($Description, optional):" -NoNewline
        } else {
            Write-Host "  $KeyName ($Description):" -NoNewline
        }
    }

    Write-Host " " -NoNewline
    $secure = Read-Host -AsSecureString
    $plain  = ConvertFrom-SecureStringPlain $secure

    if ($plain.Length -gt 0) {
        Set-EnvValue $KeyName $plain
        Write-OK "$KeyName wurde in .env gesetzt."
    } elseif ($existing) {
        Write-OK "$KeyName bleibt unveraendert."
    } else {
        if ($Optional) {
            Write-Info "$KeyName wurde nicht gesetzt (optional, kann spaeter in $envFile nachgetragen werden)."
        } else {
            Write-Err "$KeyName wurde nicht gesetzt! Bitte spaeter manuell in $envFile eintragen."
        }
    }
}

Set-ApiKey -KeyName "OPENAI_API_KEY"  -Description "benoetigt fuer alle Samples"  -Optional $false
Set-ApiKey -KeyName "SERPER_API_KEY"  -Description "benoetigt fuer Sample 2b/2c"  -Optional $true

# ------------------------------------------------------------------------------
# Fertig!
# ------------------------------------------------------------------------------
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Setup abgeschlossen!"                      -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Naechste Schritte:" -ForegroundColor Cyan
Write-Host "  1. VS Code oeffnen:     code $repoPath"
Write-Host "  2. Notebook auswaehlen: crewai_samples.ipynb"
Write-Host "  3. Viel Spass beim GirlsDay 2026! :)"
Write-Host ""
Read-Host "Enter druecken zum Beenden"
