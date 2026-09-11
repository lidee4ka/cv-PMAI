#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "Публикация https://lidee4ka.github.io/cv-PMAI/"
echo "Папка: $PWD"

if [[ ! -f index.html ]]; then
  echo "Нет index.html. Запускайте из cv-PMAI-для-github." >&2
  exit 1
fi
if [[ ! -d assets ]]; then
  echo "Нет папки assets — без CSS/JS страница на Pages будет пустой." >&2
  exit 1
fi

if ! command -v gh >/dev/null || ! command -v git >/dev/null; then
  cat <<'TXT'
Нужны git и GitHub CLI (gh), либо GitHub Desktop:

1. https://github.com/new — имя cv-PMAI, Public, без README
2. GitHub Desktop: Add local repository → эта папка → Publish в lidee4ka/cv-PMAI
3. Settings → Pages → Deploy from a branch → main / (root)

Сайт: https://lidee4ka.github.io/cv-PMAI/
TXT
  exit 1
fi

gh auth status

if [[ ! -d .git ]]; then
  git init
  git checkout -b main
fi

git add -A
if git diff --cached --quiet; then
  echo "Нечего коммитить."
else
  git commit -m "Publish CV Product Manager (cv-PMAI)"
fi

if gh repo view lidee4ka/cv-PMAI >/dev/null 2>&1; then
  git remote remove origin 2>/dev/null || true
  git remote add origin https://github.com/lidee4ka/cv-PMAI.git
  git push -u origin main
else
  gh repo create lidee4ka/cv-PMAI --public --source=. --remote=origin --push \
    --description "CV Лидии Мялкиной — Product Manager · UX/UI · AI"
fi

gh api --method POST -H "Accept: application/vnd.github+json" \
  /repos/lidee4ka/cv-PMAI/pages \
  -f "build_type=legacy" \
  -f "source[branch]=main" \
  -f "source[path]=/" >/dev/null 2>&1 || \
  echo "Pages, возможно, уже включены. Проверьте Settings → Pages: main / (root)."

echo "Готово. Через минуту: https://lidee4ka.github.io/cv-PMAI/"
echo "Репозиторий: https://github.com/lidee4ka/cv-PMAI"
