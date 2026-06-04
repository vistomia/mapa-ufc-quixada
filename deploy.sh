vue build
cd dist
git init
git add .
git commit -m "gh-page"
git remote add origin git@github.com:vistomia/mapa-ufc-quixada.git
git push --force origin main:gh-pages