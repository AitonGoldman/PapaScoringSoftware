angular.module('prereg.step1.step2.step3',['prereg.step1.step2.step3.step4',
    /*REPLACEMECHILD*/]);
angular.module('prereg.step1.step2.step3').controller(
    'prereg.step1.step2.step3',[
        '$scope','$state','TimeoutResources','Utils','Modals',
        function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
            $scope.ifpa_ranking=$state.params.ifpa_ranking;
        $scope.isWebView = ionic.Platform.isWebView();        
            
        if($scope.ifpa_ranking == ""){
            $scope.ifpa_ranking = 999999999;
        }        
        $scope.utils = Utils;
        $scope.division_ifpa_limits={};
        // $scope.division_ifpa_limits[1]=0;
        // $scope.division_ifpa_limits[2]=500;
        // $scope.division_ifpa_limits[3]=1000;
        // $scope.division_ifpa_limits[4]=1000;        
            dev_info = ionic.Platform.device();            
            if (_.size(dev_info)!=0){
                $scope.is_native=true;          
            } else {
                $scope.is_native=false;
            }                
        
        //$scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
            Modals.loading();
            div_promise = TimeoutResources.GetDivisions(undefined,{site:$scope.site});
            
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        div_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.division_selection = {};
            $scope.main_divisions = _.filter($scope.resources.divisions.data, { 'single_division': false});
            $scope.num_div_allowed=0;
            _.forEach($scope.main_divisions, function(value, key) {
                $scope.division_ifpa_limits[value.division_id]=value.ifpa_range_start;
                if($scope.division_ifpa_limits[value.division_id] < $scope.ifpa_ranking){
                    $scope.num_div_allowed=$scope.num_div_allowed+1;
                }                
                
            });       
            Modals.loaded();
        });
    }]
);
