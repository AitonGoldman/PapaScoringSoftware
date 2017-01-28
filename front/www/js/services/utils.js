angular.module('TD_services.utils', []);
angular.module('TD_services.utils').factory('Utils', ['$q','$cordovaInAppBrowser',function($q,$cordovaInAppBrowser) {                
    var resolved_promise = function(value){
	var defer = $q.defer();
	defer.resolve(value);
	return defer.promise;
    };
       
    var rejected_promise = function(value){
	var defer = $q.defer();
	defer.reject(value);
	return defer.promise;
    };
    var native_open_in_browser = function(url){        
        $cordovaInAppBrowser.open(http_prefix + '://'+server_ip_address+url, '_system');
    };            

    
    return {        
        stop_post_reload : function(){
            //FIXME : fill me in later
        },
        var_empty: function(var_to_check){
            if(var_to_check == undefined || var_to_check == ""){
                return true;
            }
            return false;
        },
        native_open_in_browser:native_open_in_browser,
        resolved_promise:resolved_promise,
        rejected_promise:rejected_promise                
    };
}]);
