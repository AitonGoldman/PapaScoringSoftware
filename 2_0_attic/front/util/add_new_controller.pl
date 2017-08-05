#!/usr/bin/perl
use Getopt::Long;
GetOptions ("name=s" => \$name,
            "path=s"   => \$path, 
            "param=s"  => \@module_params,
            "post_param=s"  => \@module_post_params,
            "help" => \$help); 

$help_message =<<"END_HELP_MESSAGE";
add_new_controller.pl --name <module name> --path <path to src dir> --param <param name> --post_param <post param name>

--name         The name of the module - ex : app.login.process
--path         Path to src dir - ex : /Users/agoldma/git/github/TD/front/src
--param        The name of a parameter to define for the ui-router state - the parameter passed to this controller will be a string value
--post_param   The name of a parameter to define for the ui-router state - the parameter passed to this controller will be an object
END_HELP_MESSAGE

if($help ne ""){      
    print $help_message;
    die();
}
$full_module_name = $name;
$path_to_src_dir = $path;

if ($full_module_name eq "" || $path_to_src_dir eq "" ){
    print "Uh oh - don't forget full module path ('--name blah.poop.arrr') and path to top level src dir ('--path /Users/agoldma/git/github/TD/front/src')\n\n";
    print $help_message;
    die();
}



@module_path_array = split(/\./,$full_module_name);
$new_module = $module_path_array[$#module_path_array];
$parent_module = $module_path_array[$#module_path_array-1];
$parent_module_file_path = $path_to_src_dir.'/'.join('/',@module_path_array[0..$#module_path_array-1]);
$module_file_path = $path_to_src_dir.'/'.join('/',@module_path_array);
$module_relative_file_path = 'js/'.join('/',@module_path_array);
$routes_path = $path_to_src_dir.'/'.join('/',@module_path_array[0..1]);
@path_array = split(/\//,$path_to_src_dir);
$index_path_location = $path_array[$#path_array-1];

if(-e $module_file_path){
    print "this is already here\n";
    die;
}

`mkdir -p $module_file_path`;

my $new_routes_string = <<"END_NEW_ROUTES";
angular.module('TDApp').config(['\$stateProvider', '\$urlRouterProvider',function(\$stateProvider, \$urlRouterProvider) {    
    \$stateProvider//REPLACE_ME
}]);
END_NEW_ROUTES

if($new_module eq "process"){
    if(@module_post_params > 0){
        for($x=0;$x<@module_post_params;$x++){
            $module_post_params_string_for_param= <<"END_ROUTES_POST_PARAMS_STRING";
,$module_post_params[$x]:{}             
END_ROUTES_POST_PARAMS_STRING
            $module_post_params_string=$module_post_params_string.$module_post_params_string_for_param;
        }    
        
    } else {
        $module_post_params_string="";
    }

    $routes_params_string = <<"END_ROUTES_PARAMS_STRING";
, params: {
             process_step:{}
             $module_post_params_string
          }    
END_ROUTES_PARAMS_STRING
} else {
    $routes_params_string = "";
}

$url_params_string="";
$url_params_sref='<!-- ui-sref=".'.$new_module.'({';
if(@module_params>0){    
    for($x=0;$x<@module_params;$x++){
        $url_params_string=$url_params_string."/".$module_params[$x].'/:'.$module_params[$x];
        $url_params_sref=$url_params_sref."$module_params[$x]: ,";
    }    
}
if(@module_post_params>0){    
    for($x=0;$x<@module_post_params;$x++){        
        $url_params_sref=$url_params_sref."$module_post_params[$x]: ,";
    }    
}
$url_params_sref=$url_params_sref.'})" -->';
my $html_string = <<"END_HTML";
<ion-view view-title="">
  <ion-content>      
     $url_params_sref    
  </ion-content>
</ion-view>

END_HTML

if($new_module ne "process"){
    $back_button_string= 'shared_html/backbutton.html';    
} else {
    $back_button_string='shared_html/notbackbutton.html';
}

my $routes_string = <<"END_CONTROLLER";
.state('$full_module_name', 
        { 
         cache: false,
 	 url: '/$new_module$url_params_string',
 	 views: {
 	     'menuContent\@app': {
 	       templateUrl: '$module_relative_file_path/$new_module.html',
 	       controller: '$full_module_name'
 	     }
 	   }$routes_params_string
       })//REPLACE_ME
END_CONTROLLER

if(@module_path_array == 2){
    $index_routes_include = "\n<script src='$module_relative_file_path/routes.js'></script>";
} else {
    $index_routes_include="";
}

$old_index = replace_string_in_file($index_path_location."/index.html",'<!--REPLACEME-->',"<script src='$module_relative_file_path/$new_module.js'></script>$index_routes_include\n<!--REPLACEME-->");

open($output1,'>',"$index_path_location/index.html");
print $output1 $old_index;
close output1;


open($output1,'>',"$module_file_path/$new_module.html");
print $output1 $html_string;
close output1;



$old_parent = replace_string_in_file($parent_module_file_path."/$parent_module.js",'\/\*REPLACEMECHILD\*\/',"'$full_module_name',\n    \/*REPLACEMECHILD\*\/");
open($output1,'>',$parent_module_file_path."/$parent_module.js");
print $output1 $old_parent;
close output1;


if(!-e $routes_path."/routes.js"){
    my $output1;
    open($output1,'>',$routes_path."/routes.js");
    print $output1 $new_routes_string;
    close output1;
}
$old_routes = replace_string_in_file($routes_path."/routes.js",'\/\/REPLACE_ME',"$routes_string");
open($output1,'>',$routes_path."/routes.js");
print $output1 $old_routes;
close output1;

%url_params = get_params_from_routes($old_routes,$full_module_name); 

$inherited_params = '$scope.site=$state.params.site;'."\n";
foreach $x (keys(%url_params)){    
    $inherited_params = $inherited_params."\t".'$scope.'.$x.'=$state.params.'.$x.";\n";
}
$passed_in_post_params = "";

for($x=0;$x<@module_post_params;$x++){
    $passed_in_post_params = $passed_in_post_params."\n        \$scope.".$module_post_params[$x]."=\$state.params.".$module_post_params[$x].";";
}
if($new_module eq "process"){
    $check_process= << "CHECK_PROCESS_END";
 \$scope.process_step=\$state.params.process_step;
        if(_.size(\$scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',\$scope.site,'app');
            return;
        }
        $passed_in_post_params
CHECK_PROCESS_END
} else {
    $check_process='';
}

my $module_string = <<"END_MODULE";
angular.module('$full_module_name',[/*REPLACEMECHILD*/]);
angular.module('$full_module_name').controller(
    '$full_module_name',[
    '\$scope','\$state','TimeoutResources','Utils','Modals',
    function(\$scope, \$state, TimeoutResources, Utils,Modals) {
        $inherited_params
        \$scope.utils = Utils;
        \$scope.bootstrap_promise = \$scope.controller_bootstrap(\$scope,\$state);                
        $check_process     
        //Modals.loading();
        //$etc_data_promise = TimeoutResources.GetEtcData();
        //$etc_data_promise.then(function(data){
        // \$scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
END_MODULE

open($output1,'>',"$module_file_path/$new_module.js");
print $output1 $module_string;
close output1;

print "put $full_module_name in $module_file_path\n";

sub get_params_from_routes {
    %params;    
    #open(input2,"$_[0]");
    $string_to_match = $_[1];
    @old_routes=split(/\n/,$_[0]);
    for($z=0;$z<@old_routes;$z++){
        $_=$old_routes[$z];        
        if($_=~ /url\: \'(.+?)\'/){
            $url=$1;
        }
        if($_=~ /controller\: \'(.+?)\'/){
            $controller=$1;
            if(index($string_to_match,$controller)>=0){
                if(index($url,':')>=0){
                    @path_elems = split(/\//,$url);
                    for($x=0;$x<@path_elems;$x++){
                        $param_index = index($path_elems[$x],':');                    
                        if($param_index >= 0){                            
                            $params{substr($path_elems[$x],1)}=" ";
                        }
                    }
                }            
            }
        }
    }
    close input2;
    return %params
}


sub replace_string_in_file {
    my $file_name = $_[0];
    my $string_to_replace = $_[1];
    my $replacement_string = $_[2];
    my $input1;
    open($input1,'<', "$file_name");
    my $old_file="";
    while($line = <$input1>){
	$line=~ s/$string_to_replace/$replacement_string/;	
	$old_file=$old_file.$line;
    }
    close input1;
    return $old_file;
}




