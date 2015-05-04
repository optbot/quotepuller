(function() {
  'use strict';
  var shell = require('shelljs');
  var path = require('path');
  var user = process.env.npm_package_config_user;
  var cmd = path.join(__dirname, 'quotepuller.sh');
  var opts = 'foo'

  shell.exec('sudo -u ' + user + ' -g ' + user + ' ' + cmd + ' ' + opts);
})();
