angular.module('TD_services.api_host',[]);
angular.module('TD_services.api_host')
    .factory('api_host',
             [function() {
                 var api_host_ip = "";
                 var results_host_ip = "";
                 return {
                     api_host:function(){
                         return api_host_ip;
                     },
                     results_host:function(){
                         return results_host_ip;
                     },                     
                     set_api_host:function(ip_to_set){
                         api_host_ip = ip_to_set;
                     },
                     set_results_host:function(ip_to_set){
                         results_host_ip = ip_to_set;
                     }
                     
                 };
}]);
