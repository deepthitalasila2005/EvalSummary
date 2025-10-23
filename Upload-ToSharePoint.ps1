# SharePoint Upload Script for Evaluation Reports
# This script helps upload the organized evaluation reports to SharePoint
# Target: ATGEvals SharePoint Site

param(
    [string]$SiteUrl = "https://microsoft.sharepoint-df.com/teams/ATGEvals",
    [string]$LibraryName = "EvaluationReports"
)

Write-Host "SharePoint Upload Helper for Evaluation Reports" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

Write-Host "`nTo use this script, you need:"
Write-Host "1. SharePoint site URL (e.g., https://yourtenant.sharepoint.com/sites/yoursite)"
Write-Host "2. Document library name (default: EvaluationReports)"
Write-Host "3. PnP PowerShell module installed"

Write-Host "`nInstallation commands:"
Write-Host "Install-Module -Name PnP.PowerShell -Force" -ForegroundColor Yellow

Write-Host "`nUsage example:"
Write-Host ".\Upload-ToSharePoint.ps1 -SiteUrl 'https://yourtenant.sharepoint.com/sites/yoursite' -LibraryName 'EvaluationReports'" -ForegroundColor Yellow

Write-Host "`nFiles ready for upload in: $(Get-Location)\SharePoint_Upload" -ForegroundColor Cyan

# Uncomment and modify these lines when ready to upload:
<#
try {
    # Connect to SharePoint
    Connect-PnPOnline -Url $SiteUrl -Interactive
    
    # Create folders in SharePoint library
    $folders = @("Reports", "Bug_Analysis", "Summaries", "Assets")
    foreach ($folder in $folders) {
        Add-PnPFolder -Name $folder -Folder $LibraryName -ErrorAction SilentlyContinue
    }
    
    # Upload files
    Get-ChildItem -Recurse ".\SharePoint_Upload" | Where-Object { !$_.PSIsContainer } | ForEach-Object {
        $relativePath = $_.FullName.Replace((Get-Location).Path + "\SharePoint_Upload\", "").Replace("\", "/")
        Add-PnPFile -Path $_.FullName -Folder "$LibraryName/$($_.Directory.Name)" -ErrorAction Continue
        Write-Host "Uploaded: $relativePath" -ForegroundColor Green
    }
    
    Write-Host "`nUpload completed successfully!" -ForegroundColor Green
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
#>

Write-Host "`nFiles organized and ready for SharePoint upload!" -ForegroundColor Green