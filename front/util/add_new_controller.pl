#!/usr/bin/perl

# goal : only add end of module path
# parse module into array - done
# get last element - done
# check dir exists, abort if it does - done
# mkdir - done
# output js from template
# output html from template
# put contents into routes
# insert module into parent module dependency



if (@ARGV < 2){
    print "Uh oh - don't forget - arg 1 is full module path ('blah.poop.arrr') and arg 2 is path to top level src dir\n";
    die;
}

$full_module_name = $ARGV[0];
$path_to_src_dir = $ARGV[1];

@module_path_array = split(/\./,$full_module_name);
$new_module = $module_path_array[$#module_path_array];
$parent_module = $module_path_array[$#module_path_array-1];
$parent_module_file_path = $path_to_src_dir.'/'.join('/',@module_path_array[0..$#module_path_array-1]);
$module_file_path = $path_to_src_dir.'/'.join('/',@module_path_array);
$module_relative_file_path = join('/',@module_path_array);
$routes_path = $path_to_src_dir.'/'.join('/',@module_path_array[0..1]);

if(-e $module_file_path){
    print "this is already here\n";
    die;
}

`mkdir -p $module_file_path`;

my $html_string = <<"END_HTML";
END_HTML

my $new_routes_string = <<"END_NEW_ROUTES";
angular.module('TOMApp').config(function(\$stateProvider, \$urlRouterProvider) {
    \$urlRouterProvider.otherwise('/app');
    
    \$stateProvider//REPLACE_ME
})
END_NEW_ROUTES

my $routes_string = <<"END_CONTROLLER";
.state('$full_module_name', 
        { 
 	 url: '/$new_module',
 	 views: {
 	     '\@': {
 	       templateUrl: '$module_relative_file_path/$new_module.html',
 	       controller: '$full_module_name',
 	     },
             'backbutton\@':{
               templateUrl: 'shared_html/backbutton.html'
             },
             'title\@':{
               template: ''
             }
 	   }
       })//REPLACE_ME
END_CONTROLLER


open($output1,'>',"$module_file_path/$new_module.html");
print $output1 $html_string;
close output1;

$old_parent = replace_string_in_file($parent_module_file_path."/$parent_module.js",'\/\*REPLACEMECHILD\*\/',"'$full_module_name',\/*REPLACEMECHILD\*\/");
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

%url_params = get_params_from_routes($routes_path."/routes.js",$full_module_name); 
$inherited_params = "";

foreach $x (keys(%url_params)){
    $inherited_params = $inherited_params.'$scope.'.$x.'=$state.params.'.$x.";\n";
}

my $module_string = <<"END_MODULE";
angular.module('$full_module_name',[/*REPLACEMECHILD*/]);
angular.module('$full_module_name').controller(
    '$full_module_name',
    function(\$scope, \$state, StatusModal, TimeoutResources) {
        $inherited_params
	//\$scope.player_info=\$state.params.newPlayerInfo;
	//if(\$scope.checkForBlankParams(\$scope.player_info) == true){
	//    return;
	//}        
    }
);
END_MODULE

open($output1,'>',"$module_file_path/$new_module.js");
print $output1 $module_string;
close output1;



sub get_params_from_routes {
    %params;
    open(input1,"$_[0]");
    $string_to_match = $_[1];
    while(<input1>){
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




