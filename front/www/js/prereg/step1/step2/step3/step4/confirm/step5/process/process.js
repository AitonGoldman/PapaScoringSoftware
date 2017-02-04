angular.module('prereg.step1.step2.step3.step4.confirm.step5.process',[/*REPLACEMECHILD*/]);
angular.module('prereg.step1.step2.step3.step4.confirm.step5.process').controller(
    'prereg.step1.step2.step3.step4.confirm.step5.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.stripe_token=$state.params.stripe_token;
	$scope.player_id=$state.params.player_id;
	$scope.player_email=$state.params.player_email;        
	$scope.player_cc_email=$state.params.player_cc_email;        
        $scope.isWebView = ionic.Platform.isWebView();        

	$scope.linked_division_id=$state.params.linked_division_id;
	$scope.uploaded_file_name=$state.params.uploaded_file_name;

        $scope.utils = Utils;        
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        Modals.loading();        
        pay_promise = TimeoutResources.PayRegistrationFee(undefined,{site:$scope.site},
                                                          {stripe_token:$scope.stripe_token,
                                                           player_id:$scope.player_id,
                                                           player_email:$scope.player_email,
                                                           player_cc_email:$scope.player_cc_email
                                                          });
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        pay_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        },function(error){
            Modals.loaded();
            Modals.error('Pre-registration failed.  Please contact PAPA staff for help', $scope.site, 'app');
            
        });
    }]
);
