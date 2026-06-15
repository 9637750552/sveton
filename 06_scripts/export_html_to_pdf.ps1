param(
  [Parameter(Mandatory = $true)]
  [string]$HtmlPath,

  [Parameter(Mandatory = $true)]
  [string]$PdfPath
)

$ErrorActionPreference = "Stop"

$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"

if (Test-Path -LiteralPath $edgePath) {
  $browserPath = $edgePath
}
elseif (Test-Path -LiteralPath $chromePath) {
  $browserPath = $chromePath
}
else {
  throw "Microsoft Edge or Google Chrome was not found."
}

$tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("sveton-md-pdf-" + [guid]::NewGuid().ToString("N"))

try {
  New-Item -ItemType Directory -Path $tempDir | Out-Null

  $localHtmlPath = Join-Path $tempDir "input.html"
  $localPdfPath = Join-Path $tempDir "output.pdf"
  Copy-Item -LiteralPath $HtmlPath -Destination $localHtmlPath

  $htmlUri = (New-Object System.Uri($localHtmlPath)).AbsoluteUri
  $arguments = @(
    "--headless=new",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "--print-to-pdf=$localPdfPath",
    $htmlUri
  )

  $process = Start-Process -FilePath $browserPath -ArgumentList $arguments -Wait -PassThru -WindowStyle Hidden

  if ($process.ExitCode -ne 0) {
    throw "Browser PDF export failed with exit code $($process.ExitCode)."
  }
  if (-not (Test-Path -LiteralPath $localPdfPath)) {
    throw "Browser PDF export finished, but no PDF was created."
  }

  Copy-Item -LiteralPath $localPdfPath -Destination $PdfPath -Force
}
finally {
  if (Test-Path -LiteralPath $tempDir) {
    Remove-Item -LiteralPath $tempDir -Recurse -Force
  }
}
