var rp = require('request-promise');
var td_utils = require('./td-test-utils');
describe('User', function() {
    beforeEach(function() {
        this.ready_to_test = td_utils.beforeTdTest(true);        
    });
    it('edit single division tournament', function(done) {
        var EC = protractor.ExpectedConditions;
        this.ready_to_test.then(function(data){
            tournament_has_been_added_p = td_utils.add_new_tournament('poopyhead',true);
            wait_for_add_divisions = tournament_has_been_added_p.then(function(data){
                $('#tournament_edit_tournament_poopyhead_link').click();
                element(by.buttonText('Edit Tournament')).click();
                return browser.wait(EC.presenceOf($('#edit_division_division_info_title')), 25000);
            });
            finish_add_division_p = wait_for_add_divisions.then(function(data){
                element(by.model('division.finals_num_qualifiers')).clear();
                element(by.model('division.finals_num_qualifiers')).sendKeys("14");
                element(by.model('division.stripe_sku')).clear();
                element(by.model('division.stripe_sku')).sendKeys("1234");                
                $('#add_tournament_team_tournament_checkbox').click();
                $('#edit_division_division_info_title').click();
                el = element(by.id("add_tournament_add_button"));
                var tag = browser.executeScript("arguments[0].scrollIntoView(true)", el);                        
                $('#add_tournament_add_button').click();                
                //                return browser.wait(EC.presenceOf($('#AddDivsionsToTournament')), 5000);
                return td_utils.checkForError(false);
            });
            check_edit_division_p = finish_add_division_p.then(function(data){
                $('#EditAnotherTournament').click();
                return browser.wait(EC.presenceOf($('#tournament_edit_tournament_poopyhead_link')), 5000);
            });
            check_values_p = check_edit_division_p.then(function(data){
                $('#tournament_edit_tournament_poopyhead_link').click();
                element(by.buttonText('Edit Tournament')).click();
                return browser.wait(EC.presenceOf($('#edit_division_division_info_title')), 25000);
            });
            check_values_p.then(function(data){
                expect(element(by.model('division.finals_num_qualifiers')).getText()).toBe('14');
                expect(element(by.model('division.stripe_sku')).getText()).toBe('1234');
                expect(element(by.model('division.use_stripe')).getText()).toBe(true);
                expect(element(by.model('division.team_tournament')).getText()).toBe(true);
                done();
            });
         });
     });
    it('edit single division tournament - local price ', function(done) {
        var EC = protractor.ExpectedConditions;
        this.ready_to_test.then(function(data){
            tournament_has_been_added_p = td_utils.add_new_tournament('poopyhead',true);
            wait_for_add_divisions = tournament_has_been_added_p.then(function(data){
                $('#tournament_edit_tournament_poopyhead_link').click();
                element(by.buttonText('Edit Tournament')).click();
                return browser.wait(EC.presenceOf($('#edit_division_division_info_title')), 25000);
            });
            finish_add_division_p = wait_for_add_divisions.then(function(data){
                element(by.model('division.use_stripe')).click();
                element(by.model('division.local_price')).sendKeys("4321");                
                $('#edit_division_division_info_title').click();
                el = element(by.id("add_tournament_add_button"));
                var tag = browser.executeScript("arguments[0].scrollIntoView(true)", el);                        
                $('#add_tournament_add_button').click();                
                //                return browser.wait(EC.presenceOf($('#AddDivsionsToTournament')), 5000);
                return td_utils.checkForError(false);
            });
            check_edit_division_p = finish_add_division_p.then(function(data){
                $('#EditAnotherTournament').click();
                return browser.wait(EC.presenceOf($('#tournament_edit_tournament_poopyhead_link')), 5000);
            });
            check_values_p = check_edit_division_p.then(function(data){
                $('#tournament_edit_tournament_poopyhead_link').click();
                element(by.buttonText('Edit Tournament')).click();
                return browser.wait(EC.presenceOf($('#edit_division_division_info_title')), 25000);
            });
            check_values_p.then(function(data){                
                expect(element(by.model('division.local_price')).getText()).toBe('4321');
                expect(element(by.model('division.use_stripe')).getText()).toBe(false);                
                done();
            });
         });
     });
    
    
    // it('add user', function(done) {
    //     var EC = protractor.ExpectedConditions;
    //     this.ready_to_test.then(function(data){
    //          td_utils.add_new_user('poopyhead').then(function(data){
    //              td_utils.checkForError(false,done);
    //          });
    //      });
    //  });
    // it('new user login', function(done) {        
    //     var EC = protractor.ExpectedConditions;
    //     this.ready_to_test.then(function(data){
    //         add_new_user_p = td_utils.add_new_user('poopyhead');
    //         ready_to_logout_p = add_new_user_p.then(function(data){
    //             return td_utils.open_menu();
    //         });
    //         logged_out_p = ready_to_logout_p.then(function(data){
    //             element(by.id('logout_link')).click();
    //             return browser.wait(EC.presenceOf($('#LoginAgainButton')), 5000);
    //         });
    //         logged_out_p.then(function(data){                
    //             return td_utils.login_through_webpage('poopyhead','poopyhead');
    //         });
    //         browser.sleep(3000).then(function(data){
    //             td_utils.checkForError(false,done);
    //         });            
    //     });
    // });
    
});
