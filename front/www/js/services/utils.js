angular.module('TD_services.utils', []);
angular.module('TD_services.utils').factory('Utils', ['Modals','User','$q',function(Modals, User, $q) {                
    var resolved_promise = function(){
	var defer = $q.defer();
	defer.resolve();
	return defer.promise;
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

        resolved_promise:resolved_promise,
        
        controller_bootstrap: function(scope, state, do_not_check_current_user){
            scope.site=state.params.site;
            User.set_user_site(scope.site);
            if(do_not_check_current_user == undefined && User.logged_in() == false){
                return User.check_current_user();
            } else {
                return resolved_promise();
            }                                 
        }
    };
}]);
