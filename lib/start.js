(function() {
  'use strict';

  var forever = require('forever-monitor');
  var nconf = require('nconf');
  var path = require('path');
  var shell = require('shelljs');
  var configFile = path.join(process.env.npm_config_quichean_nconf_path,
    'pytools', 'config.json');
  var user = process.env.npm_package_config_user;
  var service = path.join(__dirname, 'service.py');
  var dbconn = process.env.npm_package_config_db;
  var args;
  var venv;
  var child;

  nconf.file(configFile);
  // jscs:disable maximumLineLength
  args = '--logpath ' +
    path.join(process.env.npm_config_quichean_logging_path, user, 'service.log') +
    ' --logfmt "' + nconf.get('python:logging:format') + '"' +
    ' --dbconn ' + dbconn;
  // jscs:enable maximumLineLength
  venv = path.join(nconf.get('virtualenvs:path'), user, 'bin/activate');
  shell.exec('. ' + venv);
  //shell.exec('sudo -u ' + user + ' -g ' + user + ' -E python ' + service +
  //  ' ' + args);
  child = forever.start(['sudo -u', user, '-g ', user, '-E python', service, args], {
    silent: true,
    max: 1
  });
})();
