//        element(by.id('')).click();
var rp = require('request-promise');
var td_utils = require('./td-test-utils');
describe('User', function() {
    beforeEach(function() {
        td_utils.beforeTdTestEx(true);        
    });
    it('edit single division tournament', function() {
        var EC = protractor.ExpectedConditions;
        new_tournament_name = 'poopyhead';
        td_utils.add_new_tournament(new_tournament_name,true);
        element(by.id('tournament_edit_tournament_'+new_tournament_name+'_link')).click();
        element(by.buttonText('Edit Tournament')).click();        
        element(by.model('division.finals_num_qualifiers')).clear();
        element(by.model('division.finals_num_qualifiers')).sendKeys("14");
        element(by.model('division.local_price')).clear();
        element(by.model('division.local_price')).sendKeys("10");                
        //$('#add_tournament_team_tournament_checkbox').click();        
        element(by.model('division.team_tournament')).click();
        el = element(by.id("add_tournament_add_button"));
        browser.executeScript("arguments[0].scrollIntoView(true)", el);                        
        element(by.id('add_tournament_add_button')).click();                
        td_utils.checkForError(false);
        element(by.id('EditAnotherTournament')).click();
        element(by.id('tournament_edit_tournament_'+new_tournament_name+'_link')).click();
        element(by.buttonText('Edit Tournament')).click();        
        expect(element(by.model('division.finals_num_qualifiers')).getAttribute('value')).toBe('14');
        expect(element(by.model('division.local_price')).getAttribute('value')).toBe('10');
        expect(element(by.model('division.use_stripe')).$('div').$('input').isSelected()).toBe(false);
        expect(element(by.model('division.team_tournament')).$('div').$('input').isSelected()).toBe(true);        
     });            
});
