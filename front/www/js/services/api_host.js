angular.module('TD_services.api_host',[]);
angular.module('TD_services.api_host')
    .factory('api_host',
             [function() {
                 var api_host_ip = "";
                 return {
                     api_host:function(){
                         return api_host_ip;
                     },
                     set_api_host:function(ip_to_set){
                         api_host_ip = ip_to_set;
                     }
                 };
}]);
