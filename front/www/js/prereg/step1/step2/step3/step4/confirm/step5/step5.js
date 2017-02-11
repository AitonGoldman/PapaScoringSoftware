angular.module('prereg.step1.step2.step3.step4.confirm.step5',['prereg.step1.step2.step3.step4.confirm.step5.process',
    /*REPLACEMECHILD*/]);
angular.module('prereg.step1.step2.step3.step4.confirm.step5').controller(
    'prereg.step1.step2.step3.step4.confirm.step5',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.linked_division_id=$state.params.linked_division_id;
	$scope.uploaded_file_name=$state.params.uploaded_file_name;
        $scope.first_name = $state.params.player_first_name;
        $scope.last_name = $state.params.player_last_name;
        $scope.player_email = $state.params.player_email;        
        $scope.ifpa_ranking = $state.params.ifpa_ranking;
        $scope.linked_division_id = $state.params.linked_division_id;
	$scope.linked_division_name=$state.params.linked_division_name;
        $scope.uploaded_file_name = $state.params.uploaded_file_name;        
        $scope.utils = Utils;
        $scope.player_info = {};
        $scope.player_info['first_name']=$scope.first_name;
        $scope.player_info['last_name']=$scope.last_name;
        if($scope.ifpa_ranking == ""){
            $scope.ifpa_ranking = 99999999;
        }
        $scope.player_info['ifpa_ranking']=$scope.ifpa_ranking;
        $scope.isWebView = ionic.Platform.isWebView();        
        
        $scope.player_info['email_address']=$scope.player_email;
        $scope.player_info['linked_division_id']=$scope.linked_division_id;
        $scope.player_info['pic_file']=$scope.uploaded_file_name;
        Modals.loading();
        pub_key_promise = TimeoutResources.GetStripePublicKey(undefined,{site:$scope.site});
        player_add_promise = TimeoutResources.AddPreRegPlayer(pub_key_promise,{site:$scope.site},$scope.player_info);                
        player_add_promise.then(function(data){
            $scope.resources=TimeoutResources.GetAllResources();                    
            $scope.stripe_public_key = $scope.resources.stripe_public_key.data;
            Modals.loaded();
            //$scope.stripe_dialog();
        });

        $scope.stripe_dialog = function(){            
            Modals.loading();                
            var handler = StripeCheckout.configure({
                key: $scope.stripe_public_key,
                image: 'https://www.pbchallenge.net/pics/resize_pinball.png',
                opened: function(){
                    Modals.loaded();                
                },
                
                locale: 'auto',
                token: function(token) {                    
                    //$scope.ticket_purchase_in_progress = true;                    
                    $state.go('.process',{process_step:{process:true},
                                          player_id:$scope.resources.added_pre_reg_player.data.player_id,
                                          player_cc_email:token.email,                                          
                                          stripe_token:token.id
                                       });                    
                }
            });
            
            handler.open({
                name: 'TD Self Service',
                description: 'Pre-Register For PAPA 20',
                amount: 10000
            });            
        };                            
         
        //$scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
