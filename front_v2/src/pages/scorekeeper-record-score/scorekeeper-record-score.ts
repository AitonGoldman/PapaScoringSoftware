import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';


/**
 * Generated class for the ScorekeeperRecordScorePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-scorekeeper-record-score',
  templateUrl: 'scorekeeper-record-score.html',
})
export class ScorekeeperRecordScorePage extends PssPageComponent {
    tournamentId:any=null;
    tournamentMachine:any=null;
    tournamentMachineId:any=null;
    tournamentCounts:any=null;
    score:any=null;
    player_id_for_event:any=null;
    recordScoreSuccessButtons=['RE_ADD','RE_QUEUE','DEAL_WITH_PERSON_IN_QUEUE', 'DEAL_WITH_PERSON_IN_QUEUE_AND_HANDLE_CURRENT_PLAYER','GO_HOME','ADD_OR_QUEUE']
    generateSubmitScoreProcessor(successSummary){
        console.log('got results and success buttons are....');
        console.log(this.recordScoreSuccessButtons);
        return (result) => {
            if(result == null){
                return;
            }
            // console.log('in generateAddEventPlayerProcessor')
            console.log('in genrateSubmitScoreProcessor')
            console.log(result)
            let tournamentMachine=result.data;            
            if(result.tournament_counts!=0){
                successSummary.secondLine="Player has "+result.tournament_counts+" tickets left.";
            }            
            
            if(result.tournament_counts==0){
                this.recordScoreSuccessButtons=this.recordScoreSuccessButtons.filter((buttonLabel)=>{
                    if(buttonLabel=="RE_ADD" || buttonLabel=="RE_QUEUE" || buttonLabel=="DEAL_WITH_PERSON_IN_QUEUE_AND_HANDLE_CURRENT_PLAYER" || buttonLabel == "ADD_OR_QUEUE"){
                        return false;
                    } else {
                        return true;
                    }
                })
            }
            if(tournamentMachine.queues[0].player==null){
                this.recordScoreSuccessButtons=this.recordScoreSuccessButtons.filter((buttonLabel)=>{
                    if(buttonLabel=="RE_QUEUE" || buttonLabel=="DEAL_WITH_PERSON_IN_QUEUE"|| buttonLabel=="DEAL_WITH_PERSON_IN_QUEUE_AND_HANDLE_CURRENT_PLAYER"){
                        return false;
                    } else {
                        return true;
                    }
                })
            }
            if(tournamentMachine.queues[0].player!=null){
                this.recordScoreSuccessButtons=this.recordScoreSuccessButtons.filter((buttonLabel)=>{
                    if(buttonLabel=="RE_ADD" || buttonLabel=="GO_HOME" || buttonLabel=="ADD_OR_QUEUE"){
                        return false;
                    }
                    if(result.tournament_counts==0){                        
                        if(buttonLabel=="DEAL_WITH_PERSON_IN_QUEUE_AND_HANDLE_CURRENT_PLAYER"){
                            return false;
                        }                         
                    } else {
                        if(buttonLabel=="DEAL_WITH_PERSON_IN_QUEUE"){
                            return false;
                        }                         
                    }                    
                    return true;
                })
            }
            let navParams:any = {'successSummary':successSummary,
                                 'successButtons':[],
                                 'recordScoreSuccessButtons':this.recordScoreSuccessButtons,                                 
                                 'tournamentMachine':tournamentMachine,
                                 'tournamentId':this.tournamentId}
            if(this.recordScoreSuccessButtons.filter((buttonTitle)=>{
                if(buttonTitle=='THIS_IS_A_READD_OR_REQUEUE'){
                    return true;
                } else {
                    return false;
                }
            }).length==0){
                navParams['player']=this.tournamentMachine.player    
            }
            this.navCtrl.push("RecordScoreSuccessPage",            
                               this.buildNavParams(navParams));
        };
    }

    voidTicket(type){
        let actionSheet = this.actionSheetCtrl.create({
            title: 'Are you SURE you want to VOID the ticket?',
            buttons: [
                {
                text: 'VOID',
                role: 'destructive',
                handler: () => {
                    //this.onRemoveConfirmed(machine);
                    this.onVoid(type);
                    console.log('Destructive clicked');
                }
            },
                {
                text: 'Cancel',
                role: 'cancel',
                handler: () => {
                    console.log('Cancel clicked');
                }
            }
            ]
        });
        actionSheet.present();                
    }
    
    ionViewWillLoad() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

        console.log('ionViewDidLoad ScorekeeperRecordScorePage');
        this.tournamentId=this.navParams.get('tournamentId');
        this.tournamentMachineId=this.navParams.get('tournamentMachineId');
        this.tournamentMachine=this.navParams.get('tournamentMachine');
        this.tournamentCounts=this.navParams.get('tournamentCounts');
        if(this.tournamentMachine.player!=null && this.tournamentMachine.player.events != null){
            console.log('logging eventInfo');
            this.player_id_for_event = this.tournamentMachine.player.events.filter((eventInfo)=>{
                if(eventInfo.event_id==this.eventId){
                    return true
                }
            })[0].player_id_for_event;
        }
        console.log(this.tournamentMachine);
    }
    insertCommas(event){
        console.log('hi there');
        this.score = this.score.replace(/\,/g,'').replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
    }
    onVoid(type){
        let success_title_string='Ticket Voided';
        let success_line_one_string='Ticket for '+this.tournamentMachine.player.player_full_name + " has been voided on "+this.tournamentMachine.tournament_machine_name;        
        let success_line_two_string='';

        if(type=="void-requeue"){
            success_title_string=success_title_string+' And Player ReQueue on machine'
            success_line_one_string=success_line_one_string+'and requeued.';
            //let recordScoreSuccessButtons=['RE_ADD','RE_QUEUE','DEAL_WITH_PERSON_IN_QUEUE', 'DEAL_WITH_PERSON_IN_QUEUE_AND_HANDLE_CURRENT_PLAYER','GO_HOME','ADD_OR_QUEUE']
            this.recordScoreSuccessButtons = this.recordScoreSuccessButtons.filter((buttonLabel)=>{
                if(buttonLabel=="RE_ADD" || buttonLabel=="RE_QUEUE" || buttonLabel=="ADD_OR_QUEUE"){
                    return false;
                } else {
                    return true;
                }
            })
            this.recordScoreSuccessButtons.push('THIS_IS_A_READD_OR_REQUEUE');
        }
        if(type=="void-readd"){
            success_title_string=success_title_string+' And Player ReAdded to machine'            
            success_line_one_string=success_line_one_string+' and readded.';            
            this.recordScoreSuccessButtons = this.recordScoreSuccessButtons.filter((buttonLabel)=>{
                if(buttonLabel=="RE_ADD" || buttonLabel=="RE_QUEUE"  || buttonLabel=="ADD_OR_QUEUE"){
                    return false;
                } else {
                    return true;
                }
            })
            this.recordScoreSuccessButtons.push('THIS_IS_A_READD_OR_REQUEUE');
        }

        let successSummary = new SuccessSummary(success_title_string,success_line_one_string, success_line_two_string);            
        if(type=="void"){
            this.pssApi.voidTicket({tournament_id:this.tournamentId,tournament_machine_id:this.tournamentMachineId,player_id:this.tournamentMachine.player_id },this.eventId)
                .subscribe(this.generateSubmitScoreProcessor(successSummary))        

        }
        if(type!="void"){
            this.pssApi.voidTicketAndReaddOrQueue({tournament_id:this.tournamentId,tournament_machine_id:this.tournamentMachineId,player_id:this.tournamentMachine.player_id },this.eventId)
                .subscribe(this.generateSubmitScoreProcessor(successSummary))        
        }
    }
    
    onSubmit(){
        let success_title_string='Score recorded!';
        let success_line_one_string=null//this.tournamentMachine.player.player_full_name + " on machine "+this.tournamentMachine.tournament_machine_name;
        let success_line_two_string='Score of '+this.score+'.';
            
        let successSummary = new SuccessSummary(success_title_string,success_line_one_string, success_line_two_string);
        successSummary.setSummaryTable(['Score of '+this.score+'.',
                                        this.tournamentMachine.player.player_full_name + " on "+this.tournamentMachine.tournament_machine_name])
        successSummary.setCssColors('home');

        this.pssApi.submitScore({tournament_id:this.tournamentId,tournament_machine_id:this.tournamentMachineId,player_id:this.tournamentMachine.player_id, action:'record_score',score:this.score.replace(new RegExp(',', 'g'), "")},this.eventId)            
            .subscribe(this.generateSubmitScoreProcessor(successSummary))        
    }
}
