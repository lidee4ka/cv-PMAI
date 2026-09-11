#Requires -Version 5
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Публикация https://lidee4ka.github.io/cv-PMAI/"
Write-Host "Папка: $PSScriptRoot"

if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot "index.html"))) {
  throw "В этой папке нет index.html. Запускайте скрипт из cv-PMAI-для-github."
}
if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot "assets"))) {
  throw "Нет папки assets — без CSS/JS страница на Pages будет пустой."
}

function Write-Manual {
  Write-Host @"

GitHub CLI (gh) не найден или не вошёл в аккаунт. Залейте вручную:

1. https://github.com/new — имя cv-PMAI, Public, без README
2. GitHub Desktop: Add local repository → эта папка → Publish в lidee4ka/cv-PMAI
3. Settings → Pages → Deploy from a branch → main / (root)

Сайт: https://lidee4ka.github.io/cv-PMAI/
"@
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  Write-Manual
  exit 1
}

gh auth status
if ($LASTEXITCODE -ne 0) {
  Write-Host "Нужен вход: gh auth login (GitHub.com, аккаунт lidee4ka)"
  gh auth login
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "Нужен git. Или используйте GitHub Desktop — см. README.md"
}

if (-not (Test-Path .git)) {
  git init
  git checkout -b main
}

git add -A
git status
if (git diff --cached --quiet) {
  Write-Host "Нечего коммитить — файлы уже в индексе или без изменений."
} else {
  git commit -m "Publish CV Product Manager (cv-PMAI)"
}

$created = $true
gh repo view lidee4ka/cv-PMAI 2>$null
if ($LASTEXITCODE -eq 0) {
  $created = $false
  Write-Host "Репозиторий lidee4ka/cv-PMAI уже есть — пушим туда."
  git remote remove origin 2>$null
  git remote add origin https://github.com/lidee4ka/cv-PMAI.git
  git push -u origin main
} else {
  gh repo create lidee4ka/cv-PMAI --public --source=. --remote=origin --push --description "CV Лидии Мялкиной — Product Manager · UX/UI · AI"
}

gh api --method POST -H "Accept: application/vnd.github+json" /repos/lidee4ka/cv-PMAI/pages -f "build_type=legacy" -f "source[branch]=main" -f "source[path]=/" 2>$null
if ($LASTEXITCODE -ne 0) {
  Write-Host "Pages, возможно, уже включены. Проверьте Settings → Pages: main / (root)."
}

Write-Host "Готово. Через минуту: https://lidee4ka.github.io/cv-PMAI/"
if ($created) { Write-Host "Репозиторий: https://github.com/lidee4ka/cv-PMAI" }
