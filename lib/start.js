(function() {
  'use strict';

  exports = module.exports = {
    foo: testMsg
  }

  function testMsg() {
    console.log('@optbot/template: testing');
  }

  console.log('@optbot/template: other modules only see this on require()');
})();
