compass compile
cat js/jquery.tokeninput.js js/main.js js/init.js | uglifyjs - -cm -o js/prod.min.js
