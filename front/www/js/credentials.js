angular.module('credentials',[]);
angular.module('credentials')
    .factory('credentialsService',
             ['$cookies',function($cookies) {
                 var credentials = {};

                 var logged_in = {};
                 
                 var set_pss_user_credentials_from_cookies = function(event){                     
                     
                     if(event==undefined){
                         
                         return;
                     }
                     if(!_.isEmpty(credentials) && credentials[event]!=undefined){
                         logged_in[event] = true;
                         return;
                     }
                     
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
                 var initialize_event_credentials = function(event_name){
                     credentials[event_name]={};
                 };
                 var get_wizard_stack_index = function(event, stack){
                     if(credentials[event].wizard_stack_indexes[stack]==undefined){
                         credentials[event].wizard_stack_indexes[stack]=0;
                         $cookies.putObject('credentials_cookie',credentials);                         
                     }
                     return credentials[event].wizard_stack_indexes[stack];
                 };
                 var increment_wizard_stack_index = function(event, stack){
                     credentials[event].wizard_stack_indexes[stack] = credentials[event].wizard_stack_indexes[stack] + 1;
                     $cookies.putObject('credentials_cookie',credentials);                     
                 };
                 // var get_cookie_count = function(event,cookie_key){
                 //     if(credentials[event].cookie_counts[cookie_key]==undefined){
                 //         credentials[event].cookie_counts[cookie_key]=1;
                 //         $cookies.putObject('credentials_cookie',credentials);                         
                 //     }
                 // return credentials[event].cookie_counts[cookie_key];
                 // };
                 
                 // var increment_cookie_count = function(event,cookie_key){
                 //     credentials[event].cookie_counts[cookie_key] = credentials[event].cookie_counts[cookie_key] + 1;
                 //     $cookies.putObject('credentials_cookie',credentials);                     
                 // };
                 
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
                     //credentials[event].cookie_counts = JSON.parse(credential_to_set.pss_user.cookie_counts);
                     credentials[event].wizard_stack_indexes = JSON.parse(credential_to_set.pss_user.wizard_stack_indexes);
                     $cookies.putObject('credentials_cookie',credentials);
                     logged_in[event] = true;
                     //$cookies.put('session_user_id',credentials[event].pss_user_id);
                     //$cookies.put('session_user',credentials[event].username);
                     //$cookies.put('session_roles',credentials[event].roles);                     
                 };
                 
                 var remove_credentials_on_logout = function(event){                     
                     
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
                         is_logged_in:is_logged_in,
                         //increment_cookie_count:increment_cookie_count,
                         //get_cookie_count:get_cookie_count,
                         increment_wizard_stack_index:increment_wizard_stack_index,
                         get_wizard_stack_index:get_wizard_stack_index,
                         initialize_event_credentials:initialize_event_credentials
                         };
                 }
             ]
            );
