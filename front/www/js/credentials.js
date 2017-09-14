angular.module('credentials',[]);
angular.module('credentials')
    .factory('credentialsService',
             ['$cookies',function($cookies) {
                 var credentials = {};

                 var logged_in = {};
                 
                 var set_pss_user_credentials_from_cookies = function(event){                     
                     console.log('setting credentials from cookies...');                     
                     if(event==undefined){
                         console.log('bailing...');
                         return;
                     }
                     if(!_.isEmpty(credentials) && credentials[event]!=undefined){
                         logged_in[event] = true;
                         return;
                     }
                     console.log('actually setting credentials from cookies...');
                     if(!_.isEmpty(credentials)){
                         logged_in[event] = false;
                         return;                         
                     }
                     credentials = $cookies.getObject('credentials_cookie');                     
                     if(credentials==undefined){                                                  
                         credentials={};
                     }
                     if(credentials[event]!=undefined){
                         logged_in[event] = true;
                         return;                         
                     } else {
                         logged_in[event] = false;
                         return;
                     }
                 };

                 var get_credentials = function(){
                     return credentials;
                 };
                 
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
                     $cookies.putObject('credentials_cookie',credentials);
                     logged_in[event] = true;
                     //$cookies.put('session_user_id',credentials[event].pss_user_id);
                     //$cookies.put('session_user',credentials[event].username);
                     //$cookies.put('session_roles',credentials[event].roles);                     
                 };
                 
                 var remove_credentials_on_logout = function(event){                     
                     console.log('removing '+event);
                     credentials[event]=undefined;                                          
                     $cookies.remove('credentials_cookie');
                     $cookies.putObject('credentials_cookie',credentials);
                     logged_in[event]=false;                     
                 };
                 
                 var has_role = function(role,event){
                     return _.indexOf(_.concat(credentials[event].admin_roles,credentials[event].event_roles),role) != -1;
                 };

                 var is_logged_in = function(event){                                                               
                     return logged_in[event]!=undefined && logged_in[event]==true;
                 };
                 
                 return {get_credentials:get_credentials,
                         set_pss_user_credentials_from_cookies:set_pss_user_credentials_from_cookies,
                         set_pss_user_credentials:set_pss_user_credentials,
                         remove_credentials_on_logout:remove_credentials_on_logout,
                         is_logged_in:is_logged_in
                         };
                 }
             ]
            );
