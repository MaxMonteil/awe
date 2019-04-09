const puppeteer = require('puppeteer');
const url = process.argv.slice(2)[0];
const fs = require('fs');
const outputDir = process.argv.slice(3)[0]

puppeteer
  .launch({ args: [ '--no-sandbox', '--disable-setuid-sandbox' ] })
  .then(function(browser) {
    return browser.newPage();
  })
  .then(function(page) {
    return page.goto(url).then(function() {
      return page.content();
    });
  })
  .then(function(html) {
    fs.writeFile(outputDir+"output.html", html, function(err) {
      if(err) {
          return console.log(err);
      }

      console.log("The file was saved!");
      process.exit()
    });
  })
  .catch(function(err) {
    console.log(err);
  });
