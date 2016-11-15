angular.module('app.tournament.division_list.add_division',['app.tournament.division_list.add_division.process',
    /*REPLACEMECHILD*/]);
angular.module('app.tournament.division_list.add_division').controller(
    'app.tournament.division_list.add_division',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.tournament_id=$state.params.tournament_id;
        $scope.division = {use_stripe:true,scoring_type:'HERB',tournament_id:$scope.tournament_id};        

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        $scope.disable_form_submit = function(){
            if(Utils.var_empty($scope.division.division_name)){
                return true;
            }
            if($scope.division.use_stripe == true && Utils.var_empty($scope.division.stripe_sku)){
                return true;
            }
            if($scope.division.use_stripe == false && Utils.var_empty($scope.division.local_price)){
                return true;
            }
            if(Utils.var_empty($scope.division.finals_num_qualifiers)){
                return true;
            }                
            
            return false;
        };
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
