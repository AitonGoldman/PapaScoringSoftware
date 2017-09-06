angular.module('credentials',[]);
angular.module('credentials')
    .factory('credentialsService',
             [function() {
                 var credentials = {};
                 var set_credentials = function(event,credential_to_set){
                     credentials[event].username=credential_to_set.username;
                     credentials[event].pss_user_id=credential_to_set.pss_user_id;                     
                     credentials[event].player_id=credential_to_set.player_id;
                     credentials[event].roles=credential_to_set.roles;
                 };

                 var has_role = function(role,event){
                     
                 };

                 var is_logged_in = function(event){                     
                     if(credentials[event] == undefined || (credentials[event] != undefined && [event].username==undefined && credentials[event].player_id==undefined)){
                         return false;
                     } else {
                         return true;
                     }
                 };
                 return {credentials:credentials,
                         set_credentials:set_credentials,
                         is_logged_in:is_logged_in
                         };
              }
             ]
            );
