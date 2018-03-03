import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the QueueDisplaySelectPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'qds/:eventId/:eventName'
})
@Component({
  selector: 'page-queue-display-select',
  templateUrl: 'queue-display-select.html',
})

export class QueueDisplaySelectPage extends PssPageComponent {
    tournamentMachines:any = [];
    tournaments:any = [];
    ionViewWillEnter() {
        this.pssApi.getAllTournamentsAndMachines(this.eventId)            
            .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor())
    }
    gotoQueueDisplay(){
        let selectedMachines=[];
        this.tournamentMachines.forEach((machine,index)=>{
            if(machine.selected==true){
                selectedMachines.push({tournamentMachineId:machine.tournament_machine_id})
            }
        })
        this.navCtrl.push('QueueDisplayPage',this.buildNavParams({selectedMachines:JSON.stringify(selectedMachines),cols:3,numPlayersPerQueue:8,fontSize:24}))
    }
    generateGetAllTournamentsAndMachinesAndEventPlayerProcessor(withPlayer=false){
        return (result) => {            
            if(result == null){
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
            this.tournaments.forEach((tournament)=>{
                tournament.tournament_machines.forEach((tournamentMachine)=>{
                    this.tournamentMachines.push(tournamentMachine);
                })
            })
        };
    }
}
