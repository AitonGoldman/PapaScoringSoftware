import { Component,ViewChild } from '@angular/core';
import { IonicPage, NavController, NavParams, Scroll } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { trigger, style, transition, animate  } from '@angular/animations'

/**
 * Generated class for the TestPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'sr/:sliceDelta/:pause'
})
@Component({
    selector: 'page-sr',
    templateUrl: 'sr.html',
    animations: [
        trigger('scrollOut', [
            transition(':leave', [
                style({transform: 'translateY(0)', opacity: 1}),
                animate('1500ms', style({transform: 'translateY(-100%)', opacity: 0}))
            ])                        
        ])
    ]
    })
export class SrPage extends PssPageComponent {
    //@ViewChild('tournamentScroll1') scrollTournamentOne: Scroll;    
    @ViewChild('tournamentMachineScroll1') scrollTournamentMachineOne: Scroll;    
    testAnim:string = "poop";
    tournaments:any=[];
    tournamentsLoading:any=[false,false,false,false];
    tournamentMachinesLoading:any=[false,false]
    tournamentSettings:any=null;
    sliceDelta:number=10;
    pause:number=5000;
    tournamentIndexToDisplay:number=0;
    listOfIndexes:any=[0,1];
    setRowColor(e,result){        
        let rankRestriction=false;        
        if(this.tournaments[this.tournamentIndexToDisplay].finals_style=="PAPA"){
            rankRestriction=this.tournaments[this.tournamentIndexToDisplay].number_of_qualifiers;
        } else {
            rankRestriction=this.tournaments[this.tournamentIndexToDisplay].number_of_qualifiers_for_a_when_finals_style_is_ppo;
        }
        console.log(result);
        if(result && result.ifpa_ranking_restricted==true && result.rank > rankRestriction){
            return '#FF6347';
        }                
        if(e==true){
            return '#EEEEEE'
        }
        if(e!=true){
            return null
        };
    }
    
    refreshTournamentResults(tournament_index_in_tournament_list,initialize?){
        let tournament_id=this.tournaments[tournament_index_in_tournament_list].tournament_id;
        this.tournamentsLoading[tournament_index_in_tournament_list]=true;
        this.pssApi.getTournamentResultsHidden(this.eventId,tournament_id)            
            .subscribe((result)=>{
                if(result == null){
                    this.refreshTournamentResults(tournament_index_in_tournament_list)

                    return;
                }
                this.tournamentsLoading[tournament_index_in_tournament_list]=false;
                this.tournaments[tournament_index_in_tournament_list].results=result.data;
                
                this.tournamentSettings=result.tournament;
                setTimeout(()=>{
                    //tournament_index_in_tournament_list=tournament_index_in_tournament_list+1;
                    //if(tournament_index_in_tournament_list >= this.listOfIndexes.length){
                    //    tournament_index_in_tournament_list=0;
                    //}
                    console.log('refreshing...')
                    this.refreshTournamentResults(tournament_index_in_tournament_list);
                    // this.scrollToIonScroll(this.tournaments[tournament_index_in_tournament_list].results,0,()=>{                        
                    //     console.log('refreshing...');                        
                    // this.refreshTournamentResults(tournament_index_in_tournament_list);
                    // })
                },this.pause)
                if(initialize!=null){
                    this.scrollOverTournamentMachineResults(tournament_index_in_tournament_list,0)
                }                
            })        
    }
    
    scrollOverTournamentResults(tournament_index_in_tournament_list){
        this.refreshTournamentResults(tournament_index_in_tournament_list,true)
    }

    scrollOverTournamentMachineResults(tournament_index_in_tournament_list,tournament_machine_index_in_machine_list){
        let tournament_id=this.tournaments[tournament_index_in_tournament_list].tournament_id;
        this.tournamentMachinesLoading[tournament_index_in_tournament_list]=true;

        if(tournament_machine_index_in_machine_list >= this.tournaments[tournament_index_in_tournament_list].tournament_machines.length){
            tournament_machine_index_in_machine_list=0;
        }
        let tournament_machine_id=this.tournaments[tournament_index_in_tournament_list].tournament_machines[tournament_machine_index_in_machine_list].tournament_machine_id;

        this.pssApi.getTournamentMachineResultsHidden(this.eventId,tournament_id,tournament_machine_id)            
            .subscribe((result)=>{
                if(result == null){
                    this.scrollOverTournamentMachineResults(tournament_index_in_tournament_list,tournament_machine_index_in_machine_list)                    
                    return;
                }
                this.tournamentMachinesLoading[tournament_index_in_tournament_list]=false;
                this.tournaments[tournament_index_in_tournament_list].tournament_machine_index=tournament_machine_index_in_machine_list;
                this.tournaments[tournament_index_in_tournament_list].tournament_machines[tournament_machine_index_in_machine_list].results=result.data;
                setTimeout(()=>{
                    this.scrollToIonScroll(this.tournaments[tournament_index_in_tournament_list].tournament_machines[tournament_machine_index_in_machine_list].results,0,()=>{
                        console.log('refreshing...');                        
                        this.scrollOverTournamentMachineResults(tournament_index_in_tournament_list,tournament_machine_index_in_machine_list+1)
                    })
                },this.pause)
            })        
        
    }    
    scrollToIonScroll(results,index,refresh) {
        console.log('here we go...'+index)
        if(index>=results.length){
            refresh();
            return;
        }
        let sliceAmount=index+this.sliceDelta;
        if(sliceAmount>=results.length){
            sliceAmount=results.length-index+index;
        }
        for(let result of results.slice(index,sliceAmount)){
            result.hide=true;
        }        
        if(sliceAmount==results.length){            
            refresh();
            return;            
        }
        
        
        setTimeout(()=>{
            this.scrollToIonScroll(results,index+this.sliceDelta,refresh)            
        },this.pause);                

        

        // if(this.scrollOffset>20){
        //     this.scrollOffset=1;
        // }
        // let yOffset = document.getElementById("span_"+this.scrollOffset)//.offsetTop;
        // this.scrollOffset=this.scrollOffset+1;
        // yOffset.scrollIntoView(false,{behaivor:"smooth"})
        // setTimeout(()=>{
        //     console.log('looping...');
        //     this.scrollTo();
        // },300)            
        
    }

    generateGetAllTournamentsAndMachinesAndEventPlayerProcessor(){
        return (result) => {
            if(result == null){
                return;
            }            
            let tournaments=result.data.map((tournament)=>{                
                tournament.tournament_machines = tournament.tournament_machines.sort((n1,n2)=>{
                    if(n1.tournament_machine_name < n2.tournament_machine_name){
                        return -1;
                    }
                    if(n1.tournament_machine_name > n2.tournament_machine_name){
                        return 1;
                    }
                    return 0;                                    
                })
                return tournament;
            });
            this.tournaments=tournaments.sort((n1,n2)=>{
                if(n1.tournament_name < n2.tournament_name){
                    return -1;
                }
                if(n1.tournament_name > n2.tournament_name){
                    return 1;
                }
                return 0;                
            })
            this.scrollOverTournamentResults(1)
            this.scrollOverTournamentResults(0)            
            
        }
    }
    // initially, get list of tournaments and machines
    // create tournament objects in list, which contain list of machines
    //  each object has a results, and each machine has results
    // for each tournament, scrollOverTournamentResults(tournament_id){
    //  load results (with no loading message) and assign to the tournament object results
    //  when we reach end of scroll, repeat
    //  need to provide a loading indicator
    // }
    //
    // for each machine, scrollOverMachineResults(tournament_machine_id){
    //  get tournament machine results, and assign to tournament -> tournament_machine -> results
    //  when we reach end of scroll, repeat
    //  need to provide a loading indicator    
    //}
    //
    ionViewDidLoad() {
        console.log('ionViewDidLoad TestPage');
        this.eventId=1;
        this.eventName="test";
        if (this.navParams.get("sliceDelta")!=null){
            this.sliceDelta=Number(this.navParams.get("sliceDelta"));
        }
        if (this.navParams.get("pause")!=null){
            this.pause=Number(this.navParams.get("pause"));
        }

        if (this.navParams.get("tournamentIndexToDisplay")!=null){
            this.tournamentIndexToDisplay=Number(this.navParams.get("tournamentIndexToDisplay"));
        }
        
        this.pssApi.getAllTournamentsAndMachinesHidden(this.eventId)            
            .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor())

        
        
        //this.scrollTo();
        
    }

}
