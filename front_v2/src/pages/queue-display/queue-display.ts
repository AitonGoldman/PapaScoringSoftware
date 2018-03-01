import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the QueueDisplayPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'qd/:eventId/:eventName/:cols/:numPlayersPerQueue/:selectedMachines'
})
@Component({
  selector: 'page-queue-display',
  templateUrl: 'queue-display.html',
})
export class QueueDisplayPage extends PssPageComponent {
    selectedQueues:any=[];
    selectedMachines:any=[];
    cols:any=4;
    numPlayersPerQueue:any=8;
    reload:boolean=true;
    urlString:string="url('/assets/imgs/small_backglass.jpeg')";
    tournaments:any=[];
    generateGetAllTournamentsAndMachinesAndEventPlayerProcessor(withPlayer=false){
        return (result) => {            
            if(result == null){
                setTimeout(()=>{
                    if(this.reload!=true){
                        return;
                    }
                    this.pssApi.getAllTournamentsAndMachines(this.eventId)            
                        .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor())
                },5000)
                return;
            }
            this.tournaments=result.data;
            
            this.tournaments.forEach((tournament)=>{
                tournament.tournament_machines=tournament.tournament_machines.sort((n1,n2)=>{                    
                    if(n1.tournament_machine_name>n2.tournament_machine_name){
                        return 1;
                    } else {
                        return -1;
                    }
                })
            })
            this.selectedQueues=[];
            this.tournaments.forEach((tournament)=>{
                tournament.tournament_machines.forEach((tournamentMachine)=>{
                    let matchMachine = this.selectedMachines.filter((machine)=>{
                        if(machine.tournamentMachineId==tournamentMachine.tournament_machine_id){
                            return true;
                        }
                    }).length > 0;
                    console.log(matchMachine);
                    if(matchMachine==true){
                        tournamentMachine.avgPlayTime=Math.round(tournamentMachine.total_play_time/tournamentMachine.total_number_of_players);
                        if(tournamentMachine.avgPlayTime>100){
                            tournamentMachine.avgPlayTime=0;
                        }
                        this.selectedQueues.push(tournamentMachine);
                    }
                })
            })
            console.log(this.selectedQueues);
            setTimeout(()=>{
                if(this.reload!=true){
                    return;
                }
                this.pssApi.getAllTournamentsAndMachines(this.eventId)            
                    .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor())
            },15000)
            
        };
    }
    ionViewWillLeave() {
        this.reload=false;
    }
    
    ionViewWillEnter() {
        this.selectedMachines = JSON.parse(this.navParams.get('selectedMachines'));
        this.cols = this.navParams.get('cols');
        this.numPlayersPerQueue = this.navParams.get('numPlayersPerQueue')?this.navParams.get('numPlayersPerQueue'):8;
        console.log(this.selectedMachines);
        this.pssApi.getAllTournamentsAndMachines(this.eventId)            
            .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor())
    }

}
