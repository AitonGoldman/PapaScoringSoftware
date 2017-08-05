describe('user tests', function() {
    var User;
    var mock_modals;
    var mock_timeout_resources;
    var mock_state;
    api_host='http://hostname/';    

    beforeEach(function() {
        module(function($provide) {
            mock_modals = {loading:jasmine.createSpy(),loaded:jasmine.createSpy()};
            $provide.value('Modals', mock_modals);
            mock_state = {go:jasmine.createSpy()};
            $provide.value('$state',mock_state);            
        });        
    });    

    
    // Before each test load our api.users module    
    beforeEach(angular.mock.module('TD_services.timeout_resources'));        
    beforeEach(angular.mock.module('TD_services.utils'));    
    beforeEach(angular.mock.module('TD_services.user'));
    beforeEach(function() {
        module(function($provide) {
            mock_timeout_resources = {CurrentUser:jasmine.createSpy()};            
            $provide.value('TimeoutResources',mock_timeout_resources);
        });        
    });    

    
    // Before each test set our injected Users factory (_Users_) to our local Users variable
    beforeEach(inject(function(_User_,_$rootScope_,_Utils_) {        
        Utils = _Utils_;
        User = _User_;
        $rootScope=_$rootScope_;        
    }));


    
    it('Test set/get user_site', function() {
        User.set_user_site('test_site');
        expect(User.get_user_site()).toEqual('test_site');
    });

    it('Test user login/logout', function() {
        expect(User.logged_in_user()).toEqual(undefined);
        User.set_logged_in_user({'username':'test_user'});
        expect(User.logged_in_user()).toEqual({'username':'test_user'});
        User.log_out();
        expect(User.logged_in_user()).toEqual(undefined);
    });

    it('Test check_current_user()', function() {
        expect(User.logged_in_user()).toEqual(undefined);
        test_user={'username':'test_user'};
        mock_timeout_resources.CurrentUser.and.returnValue(Utils.resolved_promise({data:test_user}));
        User.check_current_user();        
        $rootScope.$apply();        
        expect(mock_timeout_resources.CurrentUser).toHaveBeenCalled();
        expect(User.logged_in_user()).toEqual(test_user);
        User.log_out();
        mock_timeout_resources.CurrentUser.and.returnValue(Utils.resolved_promise({data:null}));
        User.check_current_user();        
        $rootScope.$apply();                
        expect(User.logged_in_user()).toEqual(undefined);
    });
    it('Test has_role() on logged in user with no roles attribute', function() {
        test_user_no_roles_list={'username':'test_user'};
        User.set_logged_in_user(test_user_no_roles_list);        
        expect(User.has_role('admin')).toEqual(false);        
    });        
    it('Test has_role() with empty roles list', function() {        
        test_user_empty_roles_list={'username':'test_user','roles':[]};
        User.set_logged_in_user(test_user_empty_roles_list);
        expect(User.has_role('admin')).toEqual(false);
    });
    it('Test has_role() with roles list', function(){            
        test_user_admin_role={'username':'test_user','roles':['admin','scorekeeper','other']};
        User.set_logged_in_user(test_user_admin_role);
        expect(User.has_role('admin')).toEqual(true);
    });
});
