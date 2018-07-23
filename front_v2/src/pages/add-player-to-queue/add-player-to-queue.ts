import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete'

/**
 * Generated class for the AddPlayerToQueuePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-add-player-to-queue',
  templateUrl: 'add-player-to-queue.html',
})
export class AddPlayerToQueuePage extends AutoCompleteComponent {
    player_id_for_event:number=null;  
    selectedPlayer:any=null;
    ticketCounts:any=null;
    tournamentMachine:any=null;
    autocompleteEventHandler:any=null;
    
    ionViewWillLeave() {
        this.events.unsubscribe('autocomplete:done', this.autocompleteEventHandler) 
                                
    }
        
    ionViewWillLoad() {
        //this.tournamentMachine=JSON.parse(this.navParams.get('tournamentMachine'))
        if(this.platform.is('core')){
            this.cssColors='desktop';
        } else {
            this.cssColors='queue';
        }

        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

        this.tournamentMachine=this.navParams.get('tournamentMachine')
        console.log('ionViewDidLoad AddPlayerToQueuePage');
        console.log(this.tournamentMachine.constructor.name)
        this.autoCompleteProvider.initializeAutoComplete(null,
                                                         null,
                                                         this.generatePlayerLoadingFunction(),
                                                         this.eventId);      
        //this.events.subscribe('autocomplete:done', this.generateAutocompleteEventHandler());
        
    }
    generateGetEventPlayerProcessor(){
        return (result)=>{
            if(result==null){
                return
            }
            this.selectedPlayer=result.data!=null?result.data:{};
            //this.ticketPriceLists=result.tournament_calculated_lists;
            //this.ticketCounts=result.tournament_counts;
        }
    }
    
    // onInput(event){        
    //     if(this.player_id_for_event != null && this.player_id_for_event > 99 && this.player_id_for_event < 1000){
    //         console.log('in onInput')
    //         this.pssApi.getEventPlayer(this.eventId,this.player_id_for_event)
    //             .subscribe(this.generateGetEventPlayerProcessor())                                                  

    //     } else {
    //         this.clearValues();
    //     }        
    // }

    showQueueAddConfirm(){
        let msg = 'Confirm Queueing Up On '+this.tournamentMachine.tournament_machine_name;
        if(this.selectedPlayer.queue_player_is_in==null){
            this.addEventPlayerToQueue(this.tournamentMachine.tournament_machine_id);
            return;
        }
        msg = 'Warning! Player is already queued on '+this.selectedPlayer.queue_player_is_in.tournament_machine.tournament_machine_name+'.  Still queue on '+this.tournamentMachine.tournament_machine_name+'?'
        let confirm = this.alertCtrl.create({
            title: 'Confirm Add To Queue',
            message: msg,
            buttons: [
                {
                text: 'Cancel'
            },
                {
                text: 'Ok',
                handler: () => {
                    this.addEventPlayerToQueue(this.tournamentMachine.tournament_machine_id);
                }
            }
            ]
        });
        confirm.present();
    }
    
    clearValues(){
        this.selectedPlayer={};        
    }

    addEventPlayerToQueue(tournament_machine_id){        
        console.log(this.selectedPlayer)
        this.pssApi.addEventPlayerToQueue({'player_id':this.selectedPlayer.player_id,'tournament_machine_id':tournament_machine_id},this.eventId)
            .subscribe(this.generateAddEventPlayerToQueueProcessor())

    }
    onFocus(){
        console.log('in onFocus..')
        this.selectedPlayer=null;
        this.ticketCounts=null;
    }
    generateAddEventPlayerToQueueProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            let success_title_string=this.selectedPlayer.player_full_name+' has been added to queue.';
            let success_line_one_string='Player position in the queue is '+result.data.position+'.';
            
            let successSummary = new SuccessSummary(success_title_string,success_line_one_string,null);
            successSummary.setCssColors('queue');
            let successButtonHome = new SuccessButton('Tournament Queues',
                                                      'QueueSelectPlayerTournamentMachinePage',
                                                      this.buildNavParams({}));
            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButtonHome]}));
            
        }
    }
    
    }
