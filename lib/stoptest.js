(function() {
  var shell = require('shelljs');
  var path = require('path');
  var cmd = path.join(__dirname, 'test.js');

  shell.exec('node ' + cmd + ' stop');
})();
