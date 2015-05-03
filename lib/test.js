(function() {
  var startStopDaemon = require('start-stop-daemon');
    var path = require('path');
  var winston = require('winston');
  var logfile = path.join(__dirname, 'log/test.log');
  var logger = new (winston.Logger)({
    transports: [new (winston.transports.File)({filename: logfile})]
  });
  var daemonopts = {
    outFile: path.join(__dirname, 'log/out.log'),
    errFile: path.join(__dirname, 'log/err.log')
  };

  function say(msg) {
    logger.info(msg);
  }

  process.on('SIGTERM', function() {
    say('Caught terminate signal');
    process.exit();
  });

  process.on('SIGINT', function() {
    say('Caught interrupt signal');
    process.exit();
  });

  function goForever() {
    say('going');
    setTimeout(goForever, 4000);
  }

  startStopDaemon(daemonopts, goForever);
})();
