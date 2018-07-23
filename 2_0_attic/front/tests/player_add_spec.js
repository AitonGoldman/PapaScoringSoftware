var rp = require('request-promise');
var td_utils = require('./td-test-utils');
describe('Player', function() {
    beforeEach(function() {        
        td_utils.beforeTdTestEx(true,'test_admin','test_admin','_with_tournaments');        
    });
    it('check restrictions', function() {
        var EC = protractor.ExpectedConditions;
        var new_player_first_name='no';
        var new_player_last_name='oneofconsequence';
        td_utils.add_new_player(new_player_first_name,new_player_last_name,false);
    });
    it('check ifpa lookup', function() {
        var EC = protractor.ExpectedConditions;
        var new_player_first_name='aiton';
        var new_player_last_name='goldman';
        element(by.id('home_manage_players_button')).click();        
        element(by.id('manage_players_add_player_button')).click();        
        element(by.model('player_info.first_name')).sendKeys(new_player_first_name);    
        element(by.model('player_info.last_name')).sendKeys(new_player_last_name);        
        browser.wait(EC.stalenessOf($('#add_player_ifpa_ranking')), 1000);
        element(by.id('add_player_get_ifpa_ranking')).click();
        element(by.className('action-sheet-option')).click();
        expect(element(by.id('add_player_ifpa_ranking')).isDisplayed()).toBe(true);
    });    
    it('add player', function() {
        var EC = protractor.ExpectedConditions;
        var new_player_first_name='no';
        var new_player_last_name='oneofconsequence';
        td_utils.add_new_player(new_player_first_name,new_player_last_name,true);
        td_utils.checkForError(false);
        element(by.id('AddAnotherPlayer')).click();
        expect(element(by.id('manage_players_edit_player_1_link')).isDisplayed()).toBe(true);
    });        
});
