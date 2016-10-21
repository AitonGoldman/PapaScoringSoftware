describe('timeout_resources tests', function() {
    var TimeoutResources;    
    var mock_modals;
    var mock_resource;
    var unreachable = "Can not perform action requested.  The server is unreachable.";
    var rejected = "The server did not accept the request.";
    var unauthorized = "You are not authroized the do this.";
    var conflict = "The server reports a conflict.";
    var puked = "WHOAH!  Server puked.";    
    var derp = "I have no earthly idea what the hell just happened.";
    api_host='http://hostname/';    

    var test_http_request = function(status,message){
        var mock_response = {status:status,config:{url:'http://hostname/test/backend/route'}};
        var rejection = TimeoutResources._ResponseInterceptor.responseError(mock_response);        
        expect(mock_modals.error).toHaveBeenCalledWith(message,'test');
        expect(rejection.$$state.value.data.message).toEqual(message);        
    };    

    var test_resource_generation = function(method,interceptor){
        var resource = TimeoutResources._GenerateResourceDefinition(':site/test/route',method, interceptor);        
        expect(mock_resource).toHaveBeenCalledWith(api_host+':site/test/route',
                                                   {site:'@site'},
                                                   {'custom_http':{method:method,
                                                                   timeout: 15000,
                                                                   interceptor:interceptor
                                                                  }
                                                   }
                                                  );
    };
    
    beforeEach(function() {
        module(function($provide) {
            mock_modals = {error:jasmine.createSpy()};
            $provide.value('Modals', mock_modals);
        });        
    });    

    // Before each test load our api.users module    
    beforeEach(angular.mock.module('TD_services.timeout_resources'));
    beforeEach(angular.mock.module('TD_services.utils'));
    beforeEach(angular.mock.module('TD_services.user'));
    beforeEach(function() {
        module(function($provide) {
            mock_resource = jasmine.createSpy();
            $provide.value('$resource', mock_resource);                        
        });        
    });    
    
    // Before each test set our injected Users factory (_Users_) to our local Users variable
    beforeEach(inject(function(_TimeoutResources_,_$rootScope_) {        
        TimeoutResources = _TimeoutResources_;
        $rootScope=_$rootScope_;
    }));
    

    it('interceptor should handle timeout/unreachable http request', function() {
        test_http_request(-1,unreachable);
    });
    it('interceptor should handle rejected http request', function() {
        test_http_request(400,rejected);
    });
    it('interceptor should handle unauthorized http request', function() {
        test_http_request(401,unauthorized);        
    });
    it('interceptor should handle conflict http request', function() {
        test_http_request(409,conflict);        
    });
    it('interceptor should handle puked http request', function() {
        test_http_request(500,puked);        
    });
    it('interceptor should handle unknown http response', function() {
        test_http_request(999,derp);        
    });
    it('_GenerateResourceDefinition should generate a PUT resource',function(){
        test_resource_generation('PUT',TimeoutResources._ResponseInterceptor);
        
    });
    it('_GenerateResourceDefinition should generate a POST resource',function(){
        test_resource_generation('POST',TimeoutResources._ResponseInterceptor);        
    });
    it('_GenerateResourceDefinition should generate a GET resource',function(){
        test_resource_generation('GET',TimeoutResources._ResponseInterceptor);        
    });
    it('_GenerateResourceDefinition should generate a DELETE resource',function(){
        test_resource_generation('DELETE',TimeoutResources._ResponseInterceptor);                
    });
    it('_GenerateResourceDefinition should handle a custom responseinterceptor',function(){
        var custom_response_interceptor = function(arg_one){};        
        mock_resource.calls.reset();
        var resource = TimeoutResources._GenerateResourceDefinition(':site/test/route','PUT', custom_response_interceptor);
        expect(mock_resource.calls.count()).toEqual(0);
        test_resource_generation('DELETE',{responseError:custom_response_interceptor});
        expect(mock_resource.calls.count()).toEqual(1);        
    });            
    it('_GenerateCustomHttpExecutor should handle a POST/PUT resource',function(){        
        var fake_resource={'custom_http':jasmine.createSpy()};
        fake_resource.custom_http.and.returnValue({'$promise':jasmine.createSpy()});
        var custom_executor = TimeoutResources._GenerateCustomHttpExecutor(fake_resource,'test_resource','post');                
        var custom_executor_promise = custom_executor(undefined,{test_url_arg:'test_url_arg'},{test_post_arg:'test_post_arg'});
        $rootScope.$apply();
        expect(fake_resource.custom_http).toHaveBeenCalledWith({test_url_arg:'test_url_arg'},{test_post_arg:'test_post_arg'});
        expect(fake_resource.custom_http()['$promise']).toEqual(custom_executor_promise.$$state.value);
    });
    it('_GenerateCustomHttpExecutor should handle a GET/DELETE resource',function(){        
        var fake_resource={'custom_http':jasmine.createSpy()};
        fake_resource.custom_http.and.returnValue({'$promise':jasmine.createSpy()});
        var custom_executor = TimeoutResources._GenerateCustomHttpExecutor(fake_resource,'test_resource','get');                
        var custom_executor_promise = custom_executor(undefined,{test_url_arg:'test_url_arg'});
        $rootScope.$apply();
        expect(fake_resource.custom_http).toHaveBeenCalledWith({test_url_arg:'test_url_arg'});
        expect(fake_resource.custom_http()['$promise']).toEqual(custom_executor_promise.$$state.value);
    });
    it('testing GetAllResources gets all resources',function(){        
        var fake_resource={'custom_http':jasmine.createSpy()};
        fake_resource.custom_http.and.returnValue({'$promise':jasmine.createSpy()});
        var custom_executor = TimeoutResources._GenerateCustomHttpExecutor(fake_resource,'test_resource','get');                
        var custom_executor_promise = custom_executor(undefined,{test_url_arg:'test_url_arg'});
        $rootScope.$apply();
        expect(TimeoutResources.GetAllResources()).toEqual({test_resource: fake_resource.custom_http()});
    });
    
    
});
