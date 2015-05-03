(function() {
  'use strict';

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

  nconf.file(configFile);
  // jscs:disable maximumLineLength
  args = '--logpath ' +
    path.join(process.env.npm_config_quichean_logging_path, user, 'service.log') +
    ' --logfmt "' + nconf.get('python:logging:format') + '"' +
    ' --dbconn ' + dbconn;
  // jscs:enable maximumLineLength
  venv = path.join(nconf.get('virtualenvs:path'), user, 'bin/activate');
  shell.exec('. ' + venv);
  shell.exec('sudo -u ' + user + ' -g ' + user + ' -E python ' + service +
    ' ' + args);
  // http://big-elephants.com/2013-01/writing-your-own-init-scripts/
  //shell.exec('start-stop-daemon --background --verbose --start --oknodo --chuid ' + user + ':' + user +
  //  ' --name ' + user + ' --exec ' + service + ' -- ' + args);
})();
