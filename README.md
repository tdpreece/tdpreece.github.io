# tdpreece.github.io

## Import posts from other repos
```bash
cd post_importer
# mk a virtualenv
pip install -r requirements.txt
./update_posts_from_other_repos
```

* git add changes
* git commit changes

## Update css
```bash
cd css_build
npm install
./node_modules/bower/bin/bower
./build_css
```
After making changes to the scss files
* git add changes
* git commit changes
