var rp = require('request-promise');
var td_utils = require('./td-test-utils');
describe('User', function() {
    beforeEach(function() {
        td_utils.beforeTdTestEx(true);        
    });
    it('add single division tournament', function() {
        var EC = protractor.ExpectedConditions;
        td_utils.add_new_tournament('poopyhead',true,true);        
    });
    it('add single division tournament with stripe', function() {
        if (browser.params.test_stripe_sku == undefined){        
            console.log('You did not specify a strip_sku - skipping');
            return;
        }

        var EC = protractor.ExpectedConditions;
        td_utils.add_new_tournament('poopyhead',true,true,true,true);        
    });    
    it('add multi division tournament', function() {
        var EC = protractor.ExpectedConditions;
        new_tournament_name='poopyhead';
        td_utils.add_new_tournament(new_tournament_name,false);
        element(by.id('tournament_edit_tournament_poopyhead_link')).click();
        element(by.id('manage_tournaments_add_division_button')).click();
        element(by.model('division.division_name')).sendKeys('A');
        element(by.model('division.finals_num_qualifiers')).sendKeys("24");
        //element(by.model('division.stripe_sku')).sendKeys("12345abcd");
        element(by.model('division.use_stripe')).click();
        element(by.model('division.local_price')).sendKeys("5");            
        el = element(by.id("add_tournament_add_button"));
        browser.executeScript("arguments[0].scrollIntoView(true)", el);                        
        element(by.id('add_tournament_add_button')).click();
        td_utils.checkForError(false);
        element(by.id('AddDivisionsToTournament')).click();
        element(by.id('tournament_edit_division_A_link')).click();               
     });            
});
