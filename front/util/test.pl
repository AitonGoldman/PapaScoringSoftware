#!/usr/bin/perl
#$string_to_match = "app.tournamentselect_scorekeeper.machineselect_scorekeeper.recordscore_scorekeeper.confirm.process";

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

%url_params = get_params_from_routes($ARGV[0],"app.tournamentselect_scorekeeper.machineselect_scorekeeper.recordscore_scorekeeper.confirm.process"); 
foreach $x (keys(%url_params)){
    print "$x\n";
}

