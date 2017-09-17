angular.module('event_tournament_lib',[]);
angular.module('event_tournament_lib')
    .factory('eventTournamentLib',
             ['resourceWrapperService',function(resourceWrapperService) {
                 var on_get_tournament_event_success = function(data){                    
                     var item=data['item'];
                     var orig_item_fields=[];
                     for(i in item){
                         orig_item_fields.push(i);
                     }
                     item.bobo={};
                     for(idx in orig_item_fields){
                         field_name = orig_item_fields[idx];
                         item.bobo[field_name]=item[field_name];
                     }
                     var descriptions=data['descriptions'];                                          
                     return [descriptions,item];
                 };
                 
                 var toggle_item_active = function(item,event_name){
                     var id;
                     var rest_route;
                     
                     if(item.event_id!=undefined){
                         id=item.event_id;
                         rest_route='put_edit_event';
                     } else {
                         id=item.tournament_id;
                         rest_route='put_edit_tournament';
                     }                     
                     var on_success = function(data){
                         item.active=data['item'].active;
                         if(item.active == true){                        
                             item.icon='ion-play';
                         } else {                        
                             item.icon='ion-stop';
                         }                                              
                     };
                     
                     var new_state=item.active!=true;
                     var prom =resourceWrapperService.get_wrapper_with_loading(rest_route,on_success,{id:id,event_name:event_name},{active:new_state});                        
                     
                 };
                 return {
                     toggle_item_active:toggle_item_active,
                     on_get_tournament_event_success:on_get_tournament_event_success
                 };
             }
             ]
            );
