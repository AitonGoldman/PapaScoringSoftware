import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';


/**
 * Generated class for the ScorekeeperStartPlayerPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'ScorekeeperStartPlayer/:eventId/:tournamentId/:tournamentMachineId'
})
@Component({
  selector: 'page-scorekeeper-start-player',
  templateUrl: 'scorekeeper-start-player.html',
})
export class ScorekeeperStartPlayerPage extends AutoCompleteComponent {
    tournamentMachineId:any=null;
    tournamentMachine:any=null;
    tournamentId:any = null;
    playerToBeDealtWith:any=null;
    
    playerHasTickets:boolean = false;
    onFocus(){
        console.log('in onFocus..')
        this.selectedPlayer=null;
        this.ticketCounts=null;
        this.playerHasTickets=false;        
        //this.selectedPlayer={player_full_name:null,player_id_for_event:null,first_name:null,last_name:null};
    }
    generateGetAllTournamentsAndMachinesAndQueuesProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }            
            this.tournamentMachine=result.data.map((tournament)=>{
                for(let tournamentMachine of tournament.tournament_machines){
                    if (tournamentMachine.tournament_machine_id==this.tournamentMachineId){
                        return tournamentMachine;
                    }
                }
            })[0];
            console.log(this.tournamentMachine);
        };
    }
    
    ionViewWillLoad() {
        console.log('ionViewWillLoad ScorekeeperStartPlayerPage');
        this.autoCompleteProvider.initializeAutoComplete(null,
                                                         null,
                                                         null,
                                                         this.eventId);      

        this.tournamentMachineId=this.navParams.get('tournamentMachineId')
        this.tournamentMachine=this.navParams.get('tournamentMachine')
        this.tournamentId=this.navParams.get('tournamentId')
        this.playerToBeDealtWith=this.navParams.get('playerToBeDealtWith')
        console.log(this.playerToBeDealtWith);
        if(this.tournamentMachine==null){
            console.log('found null tournamentMachine...')
            this.pssApi.getAllTournamentsAndMachines(this.eventId)            
                .subscribe(this.generateGetAllTournamentsAndMachinesAndQueuesProcessor())
        }
        console.log(this.tournamentMachine);
        if(this.tournamentMachine.queues[0].player!=null){
            console.log('we have some queues...')
            console.log(this.tournamentMachine);            
            this.selectedPlayer=this.tournamentMachine.queues[0].player;
            this.selectedPlayer.fromQueue=true;
        } 
      
  }

    generateBumpPlayerProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            this.tournamentMachine=result.data;            

            if(this.tournamentMachine.queues[0].player!=null){
                this.selectedPlayer=this.tournamentMachine.queues[0].player;
                this.selectedPlayer.fromQueue=true;
            } else {
                this.selectedPlayer=null;
            }
            console.log(result);            
        }
    }
    generateStartPlayerOnMachineProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            // console.log('in generateAddEventPlayerProcessor')
            
            let success_title_string='Player has started a game!';
            let success_line_one_string=this.selectedPlayer.player_full_name + " started on machine "+this.tournamentMachine.tournament_machine_name;
            // let success_line_two_string='Player Number is '+result.data[0].events[0].player_id_for_event;
            let successSummary = new SuccessSummary(success_title_string,success_line_one_string, null);            

            let successButtonHome = new SuccessButton('Machine List',
                                                      'ScorekeeperMachineSelectPage',
                                                      this.buildNavParams({tournamentId:this.tournamentId}));
            let successButtons:any = [];
            successButtons.push(successButtonHome)
            if(this.playerToBeDealtWith!=null){
                console.log('-----about to go to ssucceess----');
                console.log(this.playerToBeDealtWith);
                successButtons.push(new SuccessButton('Deal with previous player',
                                                      'AddOrQueuePlayerAfterScoreRecordPage',
                                                      this.buildNavParams({tournamentId:this.tournamentId,
                                                                           playerId:this.playerToBeDealtWith.player_id,
                                                                           playerName:this.playerToBeDealtWith.player_full_name}))
                    
                )
            }
            // let successButtonTickets = new SuccessButton('Purchase Tickets',
            //                                              'TicketPurchasePage',
            //                                              this.buildNavParams({player_id_for_event:result.data[0].events[0].player_id_for_event}));            
            
            this.navCtrl.push("SuccessPage",            
                               this.buildNavParams({'successSummary':successSummary,
                                                    'successButtons':successButtons}));
        };
    }
    onSubmit(){
        let action:string="start";
        if(this.tournamentMachine.queues[0].player != null && this.selectedPlayer.player_id==this.tournamentMachine.queues[0].player.player_id){
            action="start_from_queue"
        }
        this.pssApi.startPlayerOnMachine({action:action,
                                          player_id:this.selectedPlayer.player_id,
                                          tournament_machine_id:this.tournamentMachine.tournament_machine_id},
                                         this.eventId)
            .subscribe(this.generateStartPlayerOnMachineProcessor())                                                  
    }
    onBump(){
        this.pssApi.bumpPlayerDownQueue({action:"bump",
                                          player_id:this.selectedPlayer.player_id,
                                          tournament_id:this.tournamentId,
                                          tournament_machine_id:this.tournamentMachine.tournament_machine_id},
                                         this.eventId)
            .subscribe(this.generateBumpPlayerProcessor())                                                  

    }
    
}
