angular.module('app.tournament.add_tournament',['app.tournament.add_tournament.process',
    /*REPLACEMECHILD*/]);
angular.module('app.tournament.add_tournament').controller(
    'app.tournament.add_tournament',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        $scope.tournament = {use_stripe:true,single_division:true,scoring_type:'HERB'};        
        $scope.disable_form_submit = function(){
            if(Utils.var_empty($scope.tournament.tournament_name)){
                return true;
            }
            if($scope.tournament.single_division == true){
                if(Utils.var_empty($scope.tournament.finals_num_qualifiers)){
                    return true;
                }
                if($scope.tournament.division_is_limited_herb == true){
                    return false;
                }                
                if($scope.tournament.use_stripe == true && Utils.var_empty($scope.tournament.stripe_sku)){
                    return true;
                }
                if($scope.tournament.use_stripe == false && Utils.var_empty($scope.tournament.local_price)){
                    return true;
                }
            }
            
            return false;
        };
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResource.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
