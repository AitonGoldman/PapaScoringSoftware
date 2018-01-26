import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { reorderArray } from 'ionic-angular';

/**
 * Generated class for the ScorekeeperMachineSelectPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'ScorekeeperMachineSelect/:eventId/:tournamentId'
})
@Component({
  selector: 'page-scorekeeper-machine-select',
  templateUrl: 'scorekeeper-machine-select.html',
})
export class ScorekeeperMachineSelectPage  extends PssPageComponent {
    tournamentId:any=null;
    tournamentMachines:any=null;
    reorderEnabled:boolean=false;
    undoMode:boolean=false;
    
    generateGetTournamentMachinesProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            let tournamentMachines=result.data;
            tournamentMachines.map((tournament)=>{
                tournament.expanded=false;
            })            
            this.tournamentMachines=tournamentMachines.sort((n1,n2)=>{
                if(n1.tournament_machine_name < n2.tournament_machine_name){
                    return -1;
                }
                if(n1.tournament_machine_name > n2.tournament_machine_name){
                    return 1;
                }
                return 0;                
            })
            this.tournamentsOrderList = this.listOrderStorage.getList('ScorekeeperMachineSelect',this.tournamentId);
            if(this.tournamentsOrderList!=null){
                this.tournamentMachines=this.tournamentMachines.sort((n1,n2)=>{
                    if(this.tournamentsOrderList[n1.tournament_machine_id]!=null && this.tournamentsOrderList[n2.tournament_machine_id]!=null){
                        return this.tournamentsOrderList[n1.tournament_machine_id].index - this.tournamentsOrderList[n2.tournament_machine_id].index;
                    } else {
                        return 1;
                    }                 
                })            
            }                                                
        };
    }
    reorderTournamentMachineItems(indexes) {
        
        this.tournamentMachines = reorderArray(this.tournamentMachines, indexes);
        
        let tournamentMachinesListToStore = {}
        this.tournamentMachines.forEach((item,index)=>{            
            tournamentMachinesListToStore[item.tournament_machine_id]={index:index+1,tournament_machine_id:item.tournament_machine_id};
        }) 
        this.listOrderStorage.updateList('ScorekeeperMachineSelect',this.tournamentId,tournamentMachinesListToStore)
    }

    ionViewWillLoad() {
        this.tournamentId=this.navParams.get('tournamentId');
        this.pssApi.getTournamentMachines(this.eventId,this.tournamentId)
            .subscribe(this.generateGetTournamentMachinesProcessor())    

      console.log('ionViewDidLoad ScorekeeperMachineSelectPage');
    }
    reorderItems(indexes) {
        this.tournamentMachines = reorderArray(this.tournamentMachines, indexes);
    }

    generateGetAllTournamentsAndMachinesAndQueuesProcessor(tournamentMachineId){
        return (result) => {            
            if(result == null){
                return;
            }            
            // let tournamentMachine=result.data.map((tournament)=>{
            //     for(let tournamentMachine of tournament.tournament_machines){
            //         if (tournamentMachine.tournament_machine_id==tournamentMachineId){
            //             return tournamentMachine;
            //         }
            //     }
            // })[0];
            let tournamentMachine=null;
            result.data.forEach((tournament, index) => {
                tournament.tournament_machines.forEach((tournament_machine,machine_index)=>{
                    if(tournament_machine.tournament_machine_id==tournamentMachineId){
                        tournamentMachine=tournament_machine;
                    }
                })
            });
            
            let nextPageString:string = "ScorekeeperStartPlayerPage"
            if(tournamentMachine.player_id!=null){
                nextPageString = "ScorekeeperRecordScorePage"
            } 
            this.navCtrl.push(nextPageString,            
                              this.buildNavParams({tournamentId:this.tournamentId,
                                                   tournamentMachineId:tournamentMachineId,
                                                   tournamentMachine:tournamentMachine}));                        
        };
    }
    
    pushToMachine(tournamentMachineId){
        console.log('push to machine id is '+tournamentMachineId)
        this.pssApi.getAllTournamentsAndMachines(this.eventId)            
          .subscribe(this.generateGetAllTournamentsAndMachinesAndQueuesProcessor(tournamentMachineId))
        
    }

}
