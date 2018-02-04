import { Component } from '@angular/core';
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete'
import { IonicPage } from 'ionic-angular';


/**
 * Generated class for the AdminEditScoresPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'AdminEditTokens/:eventId/:eventName'
})
@Component({
  selector: 'page-admin-edit-scores',
  templateUrl: 'admin-edit-scores.html',
})
export class AdminEditScoresPage extends AutoCompleteComponent {
    scores:any = [];
    tournamentMachines:any={};
    showNewScoreForm:boolean=false;
    newScore:any={};
    generateGetScoresProcessor(){
        return ((result)=>{
            if(result==null){
                return;
            }
            this.scores=result.data;
        })
    }

    generateEditScoreProcessor(score){
        return ((result)=>{
            if(result==null){
                return;
            }
            score.voided = score.voided==false            
            this.showNewScoreForm=false;
            this.newScore={};            
            let toast = this.toastCtrl.create({
                message:  score.voided==true?"Score voided!":"Score UnVoided!",
                duration: 99000,
                position: 'top',
                showCloseButton: true,
                closeButtonText: " ",
                cssClass: "successToast"
            });
            toast.present();                    
            
        })
    }

    generateAddScoreProcessor(){
        return ((result)=>{
            if(result==null){
                return;
            }            
            this.showNewScoreForm=false;
            this.newScore={};
            let toast = this.toastCtrl.create({
                message: 'New score added!',
                duration: 99000,
                position: 'top',
                showCloseButton: true,
                closeButtonText: " ",
                cssClass: "successToast"
            });
            toast.present();                    
            
        })
    }
    
    generateGetAllTournamentsAndMachinesProcessor(){
        return ((result)=>{
            if(result==null){
                return;
            }
            let tournaments = result.data            
            tournaments.forEach((tournament,index)=>{
                tournament.tournament_machines.forEach((tournament_machine,machine_index)=>{
                    this.tournamentMachines[tournament_machine.tournament_machine_id]=tournament_machine;
                })
            })                        
        })
    }
    

    ionViewWillLoad() {
       this.autoCompleteProvider.initializeAutoComplete(null,
                                                        null,
                                                        null,
                                                        this.eventId);      
       console.log('ionViewDidLoad AdminVoidTokensPage');
       this.pssApi.getAllTournamentsAndMachines(this.eventId)
           .subscribe(this.generateGetAllTournamentsAndMachinesProcessor())                
       
    }
    onFocus(){
        console.log('in onFocus..')
        this.selectedPlayer=null;
        this.showNewScoreForm=false;
        this.newScore={};
    }
    onGetScores(){
        this.pssApi.getScores(this.eventId,this.selectedPlayer.player_id)
            .subscribe(this.generateGetScoresProcessor())                

    }
    onVoidScore(score){        
        this.pssApi.adminEditScore({}, this.eventId,this.selectedPlayer.player_id,score.score_id)
            .subscribe(this.generateEditScoreProcessor(score))                

    }
    onAddScore(){        
        this.pssApi.adminAddScore({}, this.eventId,this.selectedPlayer.player_id,this.newScore.tournament_machine_id,this.newScore.score)
            .subscribe(this.generateAddScoreProcessor())                

    }
 
}
