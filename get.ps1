param(
    [Parameter(Mandatory=$true)]
    [int]$Number
)

$url = "https://flipflop.slome.org/2026/$Number/input"

$sessionId = $env:PHPSESSID

if ([string]::IsNullOrEmpty($sessionId)) {
    Write-Error "PHPSESSID environment variable is not set."
    exit 1
}

$cookie = New-Object System.Net.Cookie("PHPSESSID", $sessionId, "/", "flipflop.slome.org")

$webSession = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$webSession.Cookies.Add($cookie)

$output = "$Number.in.txt"

Invoke-WebRequest `
    -Uri $url `
    -WebSession $webSession `
    -OutFile $output

Write-Host "Downloaded $url -> $output"