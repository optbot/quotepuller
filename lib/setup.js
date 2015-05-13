(function() {
  'use strict';

  var argv = require('yargs').argv;
  var pytools = require('@optbot/pytools');
  var shell = require('shelljs');
  var path = require('path');
  var environment = process.env.NODE_ENV || 'development';
  var serviceName = path.basename(process.env.npm_package_name);
  var serviceRoot = path.join('/usr/local/lib/quichean', serviceName);
  var nconf = require('nconf');
  var user = process.env.npm_package_config_user;
  var configFile = path.join(process.env.npm_config_quichean_nconf_path,
    'pytools', 'config.json');

  nconf.file(configFile);
  if (argv.daemon) {
    console.log('Setting up daemon only. User and virtual environment assumed.');
  } else {
    createUser();
    makeVenv();
    enableLogging();
  }
  writeConfig(enableDaemon);

  function createUser() {
    shell.exec(path.join(__dirname, 'createuser.sh') + ' ' + user +
      ' "--shell /bin/bash"');
  }

  function makeVenv() {
    var venvPath = nconf.get('virtualenvs:path');
    var venvs;
    shell.exec('apt-get install -y python-dev');
    shell.exec('apt-get install -y freetype*');
    shell.exec('apt-get install -y libxft-dev');
    shell.exec('apt-get install -y libxml2-dev libxslt1-dev');
    shell.exec('apt-get install -y cython');
    shell.exec('apt-get install -y python-scipy');
    shell.exec('apt-get install -y python-numpy');
    shell.exec('apt-get install -y python-pandas');
    pytools.init();
    console.log('pytools initialized');
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
  }

  function enableLogging() {
    var logPath = path.join(process.env.npm_config_quichean_logging_path, user);
    shell.mkdir('-p', logPath);
    shell.exec('chown ' + user + ':' + user + ' ' + logPath);
  }

  function writeConfig(successCallback) {
    var logPath = path.join(process.env.npm_config_quichean_logging_path, user);
    var logfmt = nconf.get('python:logging:format');
    var python = '/usr/bin/python';
    var configWriter = path.join(__dirname, 'configure.py');
    var dbconn;
    var opts;

    console.log('creating config file');
    console.log('NODE_ENV: ' + process.env.NODE_ENV);
    dbconn = (environment === 'production' ? 
        process.env.npm_package_config_db_prod : process.env.npm_package_config_db_dev);
    opts = ('--logpath "' + logPath + '" --dbconn "' + dbconn + '" ' +
      '--logfmt "' + logfmt + '" --service ' + serviceName);
    shell.exec(python + ' ' + configWriter + ' ' + opts, function(code, output) {
      if (code != 0) {
        console.error('Could not write configuration to file. Aborting');
        process.exit(code);
      }
      else {
        successCallback();
      }
    });
  }

  function enableDaemon() {
    var toCopy = path.join(__dirname, '../src/*');

    console.log('enabling daemon');
    shell.rm('-rf', path.join(serviceRoot, '*'));
    shell.mkdir('-p', serviceRoot);
    shell.cp('-Rf', toCopy, serviceRoot);
    setVenv();
    shell.exec('chown -R ' + user + ':' + user + ' ' + path.join(serviceRoot, '*'));
    writeUpstart();
  }

  function setVenv() {
    var fname = path.join(serviceRoot, 'python.txt');
    var python = path.join(nconf.get('virtualenvs:path'), user, 'bin/python');
    shell.exec('echo "' + python + '" > ' + fname);
  }

  function writeUpstart() {
    var source = path.join(__dirname, serviceName + '.upstart');
    var target = path.join('/etc/init', serviceName + '.conf');
    console.log('writing upstart');
    shell.exec('cat ' + source + ' > ' + target);
  }
})();
