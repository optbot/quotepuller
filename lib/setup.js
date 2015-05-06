(function() {
  'use strict';

  var pytools = require('@optbot/pytools');
  var shell = require('shelljs');
  var path = require('path');
  var nconf = require('nconf');
  var user = process.env.npm_package_config_user;
  var dbconn = process.env.npm_package_config_db;
  var configFile = path.join(process.env.npm_config_quichean_nconf_path,
    'pytools', 'config.json');
  var configWriter = path.join(__dirname, 'configure.py');
  var python = '/usr/bin/python'
  var venvPath;
  var venvs;
  var logPath;
  var logfmt;
  var opts;

  // create 'quotepuller' user
  shell.exec(path.join(__dirname, 'createuser.sh') + ' ' + user +
    ' "--shell /bin/bash"');
  // set up python virtual environment
  shell.exec('apt-get install -y python-dev');
  shell.exec('apt-get install -y freetype*');
  shell.exec('apt-get install -y libxft-dev');
  shell.exec('apt-get install -y libxml2-dev libxslt1-dev');
  pytools.init();
  console.log('pytools initialized');
  nconf.file(configFile);
  venvPath = nconf.get('virtualenvs:path');
  shell.cd(venvPath);
  venvs = shell.ls();
  if (venvs.indexOf(user) < 0) {
    shell.exec('virtualenv ' + user);
    shell.exec('chown root:sudo *');
  } else {
    console.log('virtualenv ' + user + ' already exists, updating');
  }
  shell.cd(user);
  shell.cp('-f', path.join(__dirname, 'requirements.txt'), '.');
  shell.exec('pip install -r requirements.txt');
  shell.exec('chown -R ' + user + ':sudo .');
  // logging
  logPath = path.join(process.env.npm_config_quichean_logging_path, user);
  shell.mkdir('-p', logPath);
  shell.exec('chown ' + user + ':' + user + ' ' + logPath);
  // save configurations to be read by main service script
  logfmt = nconf.get('python:logging:format');
  opts = ('--logpath "' + logPath + '" --dbconn "' + dbconn + '" ' +
    '--logfmt "' + logfmt + '"');
  shell.exec(python + ' ' + configWriter + ' ' + opts);
})();
