(function() {
  'use strict';
  var argv = require('yargs').argv;
  var shell = require('shelljs');
  var path = require('path');
  var serviceName = path.basename(process.env.npm_package_name);
  var serviceRoot = path.join('/usr/local/lib/quichean', serviceName);
  var serviceMain = path.join(serviceRoot, 'quotepuller.py');
  var nconf = require('nconf');
  var configFile = path.join(process.env.npm_config_quichean_nconf_path,
    'pytools', 'config.json');
  var user = process.env.npm_package_config_user;
  var cmd = path.join(__dirname, 'daemon.sh');
  var action = argv.action;
  var opts;
  var venv;

  nconf.file(configFile);
  venv = path.join(nconf.get('virtualenvs:path'), user);
  opts = ('--user ' + user + ' --venv ' + venv + ' --service ' + serviceMain
    + ' --action ' + action);
  shell.exec(cmd + ' ' + opts);
})();
