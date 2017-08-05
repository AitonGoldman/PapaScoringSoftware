var rp = require('request-promise');
var td_utils = require('./td-test-utils');
describe('User', function() {
    beforeEach(function() {
       td_utils.beforeTdTestEx(true);        
    });
    it('remove division machine', function() {
        var EC = protractor.ExpectedConditions;
        new_tournament_name='poopyhead';
        td_utils.add_new_tournament(new_tournament_name,true);
        element(by.id('tournament_edit_tournament_poopyhead_link')).click();
        element(by.buttonText('Edit Tournament')).click();
        element(by.id('edit_tournament_add_machines_button')).click();
        element(by.id('manage_division_machines_add_machine_button')).click();
        element(by.model('division_machine.division_machine_name')).sendKeys("miss");
        element(by.id('add_division_machine_Miss-O_to_add')).click();        
        element(by.id('manage_division_machines_edit_Miss-O')).click();
        expect(element(by.linkText('Miss-O')).isPresent()).toBe(false);
        
     });
});
