angular.module('event_tournament_lib',[]);
angular.module('event_tournament_lib')
    .factory('eventTournamentLib',
             ['resourceWrapperService',function(resourceWrapperService) {
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
                     toggle_item_active:toggle_item_active
                 };
             }
             ]
            );
