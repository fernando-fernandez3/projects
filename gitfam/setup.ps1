# GitFam Easy Setup Script for Windows

Write-Host "🌳 GitFam Setup" -ForegroundColor Cyan
Write-Host "===============" -ForegroundColor Cyan
Write-Host ""

# Check if uv is installed
$uvInstalled = Get-Command uv -ErrorAction SilentlyContinue

if (-not $uvInstalled) {
    Write-Host "📦 Installing uv package manager..." -ForegroundColor Yellow
    irm https://astral.sh/uv/install.ps1 | iex
    Write-Host "✓ uv installed" -ForegroundColor Green
} else {
    Write-Host "✓ uv already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "📚 Installing GitFam CLI..." -ForegroundColor Yellow
uv sync

Write-Host ""
Write-Host "✓ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Next steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Run the quick start wizard:"
Write-Host "    uv run gitfam quick-start" -ForegroundColor White
Write-Host ""
Write-Host "  Or initialize manually:"
Write-Host "    uv run gitfam init-project" -ForegroundColor White
Write-Host "    uv run gitfam create-branch" -ForegroundColor White
Write-Host "    uv run gitfam add-family-member" -ForegroundColor White
Write-Host ""
Write-Host "  Generate website:"
Write-Host "    uv run gitfam generate-website" -ForegroundColor White
Write-Host ""
Write-Host "💡 Tip: Activate virtual environment to use commands without 'uv run':" -ForegroundColor Yellow
Write-Host "    .venv\Scripts\activate" -ForegroundColor White
Write-Host ""
Write-Host "📖 For more help, see: docs/CLI_GUIDE.md" -ForegroundColor Cyan
Write-Host ""
