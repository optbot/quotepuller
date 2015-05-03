function say(msg) {
  console.log(msg);
}

process.on('SIGTERM', function() {
  say('Caught terminate signal');
  process.exit();
});

process.on('SIGINT', function() {
  say('Caught interrupt signal');
  process.exit();
});

(function goForever() {
  say('going');
  setTimeout(goForever, 10000);
})();
