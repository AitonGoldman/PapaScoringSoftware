describe('utils tests', function() {
    var Util;            
    //api_host='http://hostname/';    
    
    // Before each test load our api.users module    
    beforeEach(angular.mock.module('TD_services.utils'));    
    
    // Before each test set our injected Users factory (_Users_) to our local Users variable
    beforeEach(inject(function(_Utils_,_$rootScope_) {        
        Utils = _Utils_;
        $rootScope=_$rootScope_;        
    }));
   it('', function() {
                
    });
   it('test resolved_promise()', function() {
       var resolved_promise_no_data = Utils.resolved_promise();
       expect(resolved_promise_no_data.$$state.status).toEqual(1);
       expect(resolved_promise_no_data.$$state.value).toEqual(undefined);       
       var resolved_promise_with_data = Utils.resolved_promise({'data':'test_data'});
       expect(resolved_promise_with_data.$$state.value).toEqual({'data':'test_data'});       
    });
   it('test rejected_promise()', function() {
       var rejected_promise_no_data = Utils.rejected_promise();
       expect(rejected_promise_no_data.$$state.status).toEqual(2);
       expect(rejected_promise_no_data.$$state.value).toEqual(undefined);       
       var rejected_promise_with_data = Utils.rejected_promise({'data':'test_data'});
       expect(rejected_promise_with_data.$$state.value).toEqual({'data':'test_data'});       
    });

});
