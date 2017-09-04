var Homepage = function() {
    var login_link = element(by.id('list_item_Login'));
    //element(by.model('loginData.username')).sendKeys("login");

    //var nameInput = element(by.model('yourName'));
    //var greeting = element(by.binding('yourName'));

  this.get = function() {
    browser.get('http://0.0.0.0:8100/');
  };

  this.login = function(name) {
          login_link.click();
  };

};

module.exports = Homepage;
