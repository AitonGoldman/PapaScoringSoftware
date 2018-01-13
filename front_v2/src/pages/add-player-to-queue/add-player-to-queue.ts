import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';

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
export class AddPlayerToQueuePage extends PssPageComponent {
    player_id_for_event:number=null;  
    eventPlayer:any=null;
    tournamentMachine:any=null;
    ionViewWillLoad() {
        this.tournamentMachine=this.navParams.get('tournamentMachine')
        console.log('ionViewDidLoad AddPlayerToQueuePage');
        console.log(this.tournamentMachine)
    }
    generateGetEventPlayerProcessor(){
        return (result)=>{
            if(result==null){
                return
            }
            this.eventPlayer=result.data!=null?result.data:{};
            //this.ticketPriceLists=result.tournament_calculated_lists;
            //this.ticketCounts=result.tournament_counts;
        }
    }
    
    onInput(event){        
        if(this.player_id_for_event != null && this.player_id_for_event > 99 && this.player_id_for_event < 1000){
            console.log('in onInput')
            this.pssApi.getEventPlayer(this.eventId,this.player_id_for_event)
                .subscribe(this.generateGetEventPlayerProcessor())                                                  

        } else {
            this.clearValues();
        }        
    }

    clearValues(){
        this.eventPlayer={};        
    }

    addEventPlayerToQueue(tournament_machine_id){
        this.pssApi.addEventPlayerToQueue({'player_id':this.eventPlayer.player_id,'tournament_machine_id':tournament_machine_id},this.eventId)
            .subscribe(this.generateAddEventPlayerToQueueProcessor())

    }
    generateAddEventPlayerToQueueProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            let success_title_string=this.eventPlayer.player_full_name+' has been added to queue.';
            let success_line_one_string='Player position in the queue is '+result.data.position+'.';
            
            let successSummary = new SuccessSummary(success_title_string,success_line_one_string,null);            
            let successButtonHome = new SuccessButton('Go Home',
                                                      this.getHomePageString(this.eventId),
                                                      this.buildNavParams({}));
            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButtonHome]}));
            
        }
    }
    
}
