import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';

/**
 * Generated class for the AddOrQueuePlayerAfterScoreRecordPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-add-or-queue-player-after-score-record',
  templateUrl: 'add-or-queue-player-after-score-record.html',
})
export class AddOrQueuePlayerAfterScoreRecordPage extends PssPageComponent {
    tournament:any=null;
    tournamentMachines:any=null;
    tournamentId:number=null;
    playerId:any=null;
    playerName:any=null;
    playerImg:any=null;
    
    generateStartPlayerOnMachineProcessor(typeOfStart,tournamentMachineName, playerName){
        return (result) => {
            if(result == null){
                return;
            }
            // console.log('in generateAddEventPlayerProcessor')

            
            let success_title_string=""
            if(typeOfStart=="queue"){
                success_title_string='Player has been queued on machine';
            } else {
                success_title_string='Player has been started on machine';
            }
                                                
            let success_line_one_string=""
            if(typeOfStart=="queue"){
                success_line_one_string=playerName+' has been queued on '+tournamentMachineName;                
            } else {
                success_line_one_string=playerName+' has been started on '+tournamentMachineName;
            }
            
            
            // let success_line_two_string='Player Number is '+result.data[0].events[0].player_id_for_event;
            let successSummary = new SuccessSummary(success_title_string,success_line_one_string, null);            
            successSummary.setCssColors('home');
            let successButtonHome = new SuccessButton('Machine List',
                                                      'ScorekeeperMachineSelectPage',
                                                      this.buildNavParams({tournamentId:this.tournamentId}));
            let successButtons:any = [];
            successButtons.push(successButtonHome)
            this.navCtrl.push("SuccessPage",            
                               this.buildNavParams({'successSummary':successSummary,
                                                    'successButtons':successButtons}));
        };
    }
    
    addOrQueuePlayer(tournamentMachine){
        let alertMsg="";
        let type="";
        if(tournamentMachine.queue_length==0){
            alertMsg="Add player to "+tournamentMachine.tournament_machine_name+"?"            
            type="start";

        } else {
            alertMsg="Queue player on "+tournamentMachine.tournament_machine_name+"?"
            type="queue";
        }
        let alert = this.alertCtrl.create({
            title: 'Confirm ',
            message: alertMsg,
            buttons: [
                {
                text: 'Cancel',
                role: 'cancel',
                handler: () => {
                    console.log('Cancel clicked');
                }
            },
                {
                text: 'Ok',
                handler: () => {
                    this.pssApi.startPlayerOnMachine({action:"start_or_queue",
                                                      player_id:this.playerId,
                                                      tournament_machine_id:tournamentMachine.tournament_machine_id},
                                                     this.eventId)
                        .subscribe(this.generateStartPlayerOnMachineProcessor(type,tournamentMachine.tournament_machine_name,this.playerName))                                                  

                }
            }
            ]
        });
        alert.present();
    }

    
    generateGetAllTournamentsAndMachinesProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            console.log('in getAllTournaments...')            
            let tournaments=result.data;
            this.tournament=tournaments.filter((tournament)=>{
                if(tournament.tournament_id==this.tournamentId){
                    return true;
                }
                return false;
            })[0]
            this.tournament.tournament_machines.map((machine)=>{
                if(machine.player_id!=null){
                    machine.queue_length=1;                    
                } else {
                    machine.queue_length=0;
                }
                machine.queues.map((queue)=>{
                    if(queue.player!=null){
                        machine.queue_length=machine.queue_length+1;
                    }
                    return queue;
                })
                return machine;
            })
            this.tournamentMachines=this.tournament.tournament_machines;
            console.log(this.tournament);
        }
    }
        
  ionViewWillLoad() {
      console.log('ionViewDidLoad AddOrQueuePlayerAfterScoreRecordPage');
      if(this.eventId==null){
          this.pushRootPage('EventSelectPage')
          return;
      }
      this.tournamentId=this.navParams.get('tournamentId');
      this.playerId=this.navParams.get('playerId');
      this.playerName=this.navParams.get('playerName');
      this.playerImg=this.navParams.get('playerImg');
      
      this.pssApi.getAllTournamentsAndMachines(this.eventId)            
          .subscribe(this.generateGetAllTournamentsAndMachinesProcessor())      
  }
}
  
