angular.module('TD_services.utils', []);
angular.module('TD_services.utils').factory('Utils', ['$q','$cordovaInAppBrowser',function($q,$cordovaInAppBrowser) {

    var check_tiebreaker_is_important = function(important_bye_ranks,important_qualifying_rank,rank_to_test){
        //important_bye_rank = $scope.resources.division_final_important_tiebreaker_ranks.data.important_tiebreakers.bye;
        //important_qualifying_rank = $scope.resources.division_final_important_tiebreaker_ranks.data.important_tiebreakers.qualifying;        
        console.log(important_bye_ranks,important_qualifying_rank,rank_to_test);
        if (_.indexOf(important_bye_ranks,rank_to_test) != -1){
            console.log('poop');
            return true;
        }
        if (important_qualifying_rank==rank_to_test){
            console.log(important_qualifying_rank+ " "+rank_to_test);

            return true;
        }
        return false;
    };
    
    
    var extract_results_from_response = function(my_resource){
        return _.keyBy(my_resource, function(o) {
            return o.resource_name;
        });
    };
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
        rejected_promise:rejected_promise,
        extract_results_from_response,
        check_tiebreaker_is_important
    };
}]);
