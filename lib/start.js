(function() {
  'use strict';
  var shell = require('shelljs');
  var path = require('path');
  var nconf = require('nconf');
  var configFile = path.join(process.env.npm_config_quichean_nconf_path,
    'pytools', 'config.json');
  var dbconn = process.env.npm_package_config_db;
  var user = process.env.npm_package_config_user;
  var service = path.join(__dirname, 'service.py');
  var cmd = path.join(__dirname, 'quotepuller.sh');
  var logs = process.env.npm_config_quichean_logging_path; 
  var opts;
  var venvs;

  nconf.file(configFile);
  venvs = nconf.get('virtualenvs:path');
  opts = ('--logs ' + logs + ' --venvs ' + venvs + ' --dbconn ' + dbconn
    + ' --serv ' + service); 
  shell.exec('sudo -u ' + user + ' -g ' + user + ' ' + cmd + ' ' + opts);
})();
