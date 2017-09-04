// spec.js

var Homepage = require('../homepage.js');

describe('Protractor Demo App', function() {
  it('should have a title', function() {
      var homepage = new Homepage();
      //browser.get('http://0.0.0.0:8100/');
      homepage.get();
      homepage.login();
      //element(by.id('list_item_Login')).click();
      //element(by.model('loginData.username')).sendKeys("login");
      browser.sleep(5000);
      expect(browser.getTitle()).toEqual('Super Calculator');
  });
});
