angular.module('app.player_token.confirm',['app.player_token.confirm.process',
    /*REPLACEMECHILD*/]);
angular.module('app.player_token.confirm').controller(
    'app.player_token.confirm',[
        '$scope','$state','TimeoutResources','Utils','Modals','User',
        function($scope, $state, TimeoutResources, Utils,Modals,User) {
            $scope.site=$state.params.site;

            $scope.utils = Utils;
            $scope.token_info = $state.params.token_info;
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);
            pub_key_promise = TimeoutResources.GetStripePublicKey($scope.bootstrap_promise,{site:$scope.site});
            pub_key_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.stripe_public_key = $scope.resources.stripe_public_key.data;
                Modals.loaded();
            });
            $scope.create_tickets = function(){
                // $scope.added_tokens = {};
                // $scope.added_tokens['divisions']=$scope.token_info.divisions;
                // $scope.added_tokens['metadivisions']=$scope.token_info.metadivisions;
                // $scope.added_tokens['teams']=$scope.token_info.teams;
                // $scope.added_tokens['player_id']=User.logged_in_user().player.player_id;
                // Modals.loading();
                // token_add_promise = TimeoutResources.AddPlayerTokens(undefined,{site:$scope.site},$scope.added_tokens);                
                // token_add_promise.then(function(data){
                //     $scope.resources=TimeoutResources.GetAllResources();                    
                //     Modals.loaded();
                //     $scope.stripe_dialog();
                // });
            };
            $scope.stripe_dialog = function(){
                $scope.added_tokens = {};
                $scope.added_tokens['divisions']=$scope.token_info.divisions;
                $scope.added_tokens['metadivisions']=$scope.token_info.metadivisions;
                $scope.added_tokens['teams']=$scope.token_info.teams;
                $scope.added_tokens['player_id']=User.logged_in_user().player.player_id;
                Modals.loading();
                token_add_promise = TimeoutResources.AddPlayerTokens(undefined,{site:$scope.site},$scope.added_tokens);                
                token_add_promise.then(function(data){
                    $scope.resources=TimeoutResources.GetAllResources();                                        
                    //$scope.stripe_dialog();
                });

                var handler = StripeCheckout.configure({
                    key: $scope.stripe_public_key,
                    image: 'https://www.pbchallenge.net/pics/resize_pinball.png',
                    locale: 'auto',
                    opened: function(){
                        Modals.loaded();                
                    },
                    token: function(token) {                    
                        $scope.ticket_purchase_in_progress = true;
                        $state.go('.process',{process_step:{process:true},
                                              token_info:{addedTokens:$scope.added_tokens,
                                                          stripeToken:token.id,
                                                          email:token.email,
                                                          tokens:$scope.resources.added_player_tokens.data.tokens,
                                                          total_cost:$scope.token_info.total_cost}
                                             });                    
                    }
                });
                
                handler.open({
                    name: 'TOM Self Service',
                    description: 'Purchase Tickets',
                    amount: $scope.token_info.total_cost*100
                });
            };                            
        }]
);
