import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { SuccessPage } from '../success/success'

/**
 * Generated class for the RecordScoreSuccessPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-record-score-success',
  templateUrl: '../success/success.html',
})
export class RecordScoreSuccessPage extends SuccessPage {
    recordScoreSuccess:boolean=false;
    recordScoreSuccessButtons:any = null;
    tournamentMachine:any=null;
    tournamentId:any=null;
    reAddSuccess:boolean=false;
    reQueueSuccess:boolean=false;
    handleCurrentPlayerLater:boolean=true;
    
    player:any=null;
    
    ionViewWillLoad() {
            if(this.eventId==null){
                this.pushRootPage('EventSelectPage')
                return;
            }

        super.ionViewWillLoad();
        this.recordScoreSuccess=true;

        console.log('ionViewDidLoad RecordScoreSuccessPage');
        this.recordScoreSuccessButtons=this.navParams.get('recordScoreSuccessButtons');        
        this.tournamentMachine=this.navParams.get('tournamentMachine');
        this.tournamentId=this.navParams.get('tournamentId');        
        this.player=this.navParams.get('player');
        
    }
    generatePlacePlayerOnMachineAgainProcessor(message){
        return (result)=>{
            if(result==null){
                return;
            }
            this.reAddSuccess=true;
            // let toast = this.toastCtrl.create({
            //     message: message,
            //     duration: 99000,
            //     position: 'top',
            //     showCloseButton: true,
            //     closeButtonText: " ",
            //     cssClass: "successToast"
            // });
            // toast.present();                    
            this.pssToast.showToast(message,
                                    4000,
                                    "successToast")
            
        }
    }
    reAddPlayerToMachine(){
        this.handleCurrentPlayerLater=false;
        this.pssApi.startPlayerOnMachine({action:"start",
                                          player_id:this.player.player_id,
                                          tournament_machine_id:this.tournamentMachine.tournament_machine_id},
                                          this.eventId)
            .subscribe(this.generatePlacePlayerOnMachineAgainProcessor("Player re-added to machine"))

    }
    reQueuePlayerOnMachine(){
        this.handleCurrentPlayerLater=false;
        this.pssApi.addEventPlayerToQueue({'player_id':this.player.player_id,'tournament_machine_id':this.tournamentMachine.tournament_machine_id},this.eventId)
            .subscribe(this.generatePlacePlayerOnMachineAgainProcessor("Player re-queued on machine"))
    }
    returnToStartPlayer(buttonLabel){
        let params:any = {tournamentMachineId:this.tournamentMachine.tournament_machine_id,tournamentMachine:this.tournamentMachine,tournamentId:this.tournamentId};
        if(buttonLabel=='DEAL_WITH_PERSON_IN_QUEUE_AND_HANDLE_CURRENT_PLAYER' && this.handleCurrentPlayerLater==true){
            params.playerToBeDealtWith=this.player;
        }
        this.pushPageWithNoBackButton('ScorekeeperStartPlayerPage',this.buildNavParams(params));        
    }
}
