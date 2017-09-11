angular.module('credentials',[]);
angular.module('credentials')
    .factory('credentialsService',
             ['$cookies',function($cookies) {
                 var credentials = {};                 
/*{
  "pss_user": {
    "admin_roles": [
      {
        "admin_role": true, 
        "admin_role_id": 1, 
        "name": "pss_admin"
      }
    ], 
    "event_roles": [], 
    "event_user": {
      "active": true, 
      "pss_user_id": 1
    }, 
    "events": [
      {
        "event_id": 1, 
        "event_name": "pss_admin"
      }, 
      {
        "event_id": 2, 
        "event_name": "poopone"
      }
    ], 
    "extra_title": null, 
    "first_name": "test_first_name", 
    "has_picture": false, 
    "ioniccloud_push_token": null, 
    "last_name": "test_last_name", 
    "pss_user_id": 1, 
    "username": "test_pss_admin_user"
  }
}*/
                 var set_pss_user_credentials = function(event,credential_to_set){                     
                     credentials[event] = {};
                     credentials[event].username=credential_to_set.pss_user.username;
                     credentials[event].pss_user_id=credential_to_set.pss_user.pss_user_id;
                     var admin_roles=credential_to_set.pss_user.admin_roles;
                     var event_roles=credential_to_set.pss_user.event_roles;
                     if (admin_roles.length > 0){
                         admin_roles=_.map(admin_roles, function(role){return role.name;});
                     } else {
                         admin_roles=[];
                     }
                     if (event_roles.length > 0){
                         event_roles=_.map(event_roles, function(role){return role.name;});
                     } else {
                         event_roles=[];
                     }
                     credentials[event].roles=_.concat(event_roles,admin_roles);
                     $cookies.put('session_user',credentials[event].username);
                     $cookies.put('session_roles',credentials[event].roles);                     
                 };
                 
                 var remove_credentials_on_logout = function(event,credential_to_set){                     
                     $cookies.remove('session_user');
                     $cookies.remove('session_roles');                                          
                 };
                 
                 var has_role = function(role,event){
                     return _.indexOf(_.concat(credentials[event].admin_roles,credentials[event].event_roles),role) != -1;
                 };

                 var is_logged_in = function(event){                     
                     if($cookies.get('session_user')!=undefined){                         
                         return true;
                     }
                     if(credentials[event] == undefined || (credentials[event] != undefined && credentials[event].username==undefined && credentials[event].player_id==undefined)){
                         return false;
                     } else {
                         return true;
                     }
                 };
                 return {credentials:credentials,
                         set_pss_user_credentials:set_pss_user_credentials,
                         is_logged_in:is_logged_in
                         };
                 }
             ]
            );
