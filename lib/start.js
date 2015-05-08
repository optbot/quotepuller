(function() {
  'use strict';
  var shell = require('shelljs');
  var path = require('path');
  var serviceName = path.basename(process.env.npm_package_name);
  var serviceRoot = path.join('/usr/local/lib/quichean', serviceName);
  var serviceMain = path.join(serviceRoot, 'quotepuller.py');
  var nconf = require('nconf');
  var configFile = path.join(process.env.npm_config_quichean_nconf_path,
    'pytools', 'config.json');
  var user = process.env.npm_package_config_user;
  var cmd = path.join(__dirname, 'start.sh');
  var opts;
  var venv;

  nconf.file(configFile);
  venv = path.join(nconf.get('virtualenvs:path'), user);
  opts = ('--user ' + user + ' --venv ' + venv + ' --service ' + serviceMain);

  console.log(opts);
  shell.exec(cmd + ' ' + opts);

  function showEnv() {
    Object.keys(process.env).forEach(function(item, i, arr) {
      console.log(item + ' : ' + process.env[item]);
    });
  }
})();
