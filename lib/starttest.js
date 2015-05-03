(function() {
  var shell = require('shelljs');
  var path = require('path');
  var cmd = path.join(__dirname, 'test.js');
  var user = process.env.npm_package_config_user;

  //shell.exec('sudo -u ' + user + ' -g ' + user + ' node ' + cmd + ' start');
  shell.exec('node ' + cmd + ' start');
})();
