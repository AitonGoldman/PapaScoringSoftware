var rp = require('request-promise');
var td_utils = require('./td-test-utils');
describe('Player', function() {
    beforeEach(function() {        
        td_utils.beforeTdTestEx(true,'test_admin','test_admin','_with_tournaments');        
    });
    it('edit player', function() {
        var EC = protractor.ExpectedConditions;
        var new_player_first_name='booboo';
        var new_player_last_name='noonoo';
        td_utils.add_new_player(new_player_first_name,new_player_last_name,true);        
        element(by.id('AddAnotherPlayer')).click();
        element(by.id('manage_players_edit_player_1_link')).click();
        element(by.buttonText('Edit Player')).click();        
        element(by.model('player_info.first_name')).clear();
        element(by.model('player_info.first_name')).sendKeys(new_player_first_name+'edited');        
        element(by.model('player_info.last_name')).clear();
        element(by.model('player_info.last_name')).sendKeys(new_player_last_name+'edited');
        element(by.model('player_info.ifpa_ranking')).clear();
        element(by.model('player_info.ifpa_ranking')).sendKeys('123456');
        element(by.id('edit_player_edit_button')).click();
        td_utils.checkForError(false);
        element(by.id('GoHomeButton')).click();
        element(by.id('home_manage_players_button')).click();        
        element(by.id('manage_players_edit_player_1_link')).click();
        element(by.buttonText('Edit Player')).click();        
        expect(element(by.model('player_info.first_name')).getAttribute('value')).toBe(new_player_first_name+'edited');
        expect(element(by.model('player_info.last_name')).getAttribute('value')).toBe(new_player_last_name+'edited');
        expect(element(by.model('player_info.ifpa_ranking')).getAttribute('value')).toBe('123456');
        
    });        
});
