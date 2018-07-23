import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';

/**
 * Generated class for the QueueSelectPlayerTournamentMachinePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-queue-select-player-tournament-machine',
  templateUrl: 'queue-select-player-tournament-machine.html',
})
export class QueueSelectPlayerTournamentMachinePage extends PssPageComponent {
    tournaments:any = [];
    eventPlayer:any={};
    player_id_for_event:number=null;    
    hideSearchbar:boolean=false;
    ticketCounts:any=null;
    queueMode:string="manage"
    role:string = null;
    loggedInPlayerId:number = null;
    round:any=Math.round
    
    generateGetEventPlayerProcessor(){
        return (result)=>{
            if(result==null){
                return
            }
            this.eventPlayer=result.data!=null?result.data:{};
            this.ticketCounts=result.tournament_counts;
        }
    }

    generateAddEventPlayerToQueueProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            let success_title_string=this.eventPlayer.player_full_name+' has been added to queue.';
            let success_line_one_string='Player position in the queue is '+result.data.position+'.';
            
            let success_line_two_string='';
            if(this.tournamentSettings.getKioskMode()==true){
                success_line_two_string='NOTE : You have been logged out.'
                this.eventAuth.logout(this.eventId);
            }
            let successSummary = new SuccessSummary(success_title_string,success_line_one_string,success_line_two_string);            
            successSummary.setCssColors('queue');
            let successButtonHome = new SuccessButton('Tournament Queues',
                                                      'QueueSelectPlayerTournamentMachinePage',
                                                      this.buildNavParams({}));
            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButtonHome]}));
            
        }
    }

    kioskGenerateAddEventPlayerToQueueProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            let success_title_string=result['player_name']+' has been added to queue.';
            let success_line_one_string='Player position in the queue is '+result.data.position+'.';
            
            let success_line_two_string='';
            let successSummary = new SuccessSummary(success_title_string,success_line_one_string,success_line_two_string);            
            if(this.tournamentSettings.getKioskMode()==true){
                //success_line_two_string='NOTE : You have been logged out.'
                console.log(result);
                successSummary.setAttentionString(result['removed_from'])
                this.eventAuth.logout(this.eventId);
            }

            successSummary.setCssColors('queue');
            let successButtonHome = new SuccessButton('Tournament Queues',
                                                      'QueueSelectPlayerTournamentMachinePage',
                                                      this.buildNavParams({}));
            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButtonHome]}));
            
        }
    }
    
    showKioskQueueAddConfirm(tournamentMachine){
        let msg = 'Confirm Queueing Up On '+tournamentMachine.tournament_machine_name;
        let title = 'Confirm Add To Queue'
        let confirm = this.alertCtrl.create({
            title: title,
            message: msg,
            inputs: [
                {
                name: 'player_id_for_event',
                placeholder: 'Player Number'
            },{
                name: 'player_pin_for_event',
                placeholder: 'Pin'
                
            }],
            buttons: [
                {
                text: 'Cancel'
            },
                {
                text: 'Ok',
                handler: (data) => {
                    this.kioskAddEventPlayerToQueue({event_player_id:data['player_id_for_event'],
                                                     pin:data['player_pin_for_event'],
                                                     tournament_machine_id:tournamentMachine.tournament_machine_id});
                }
            }
            ]
        });
        confirm.present();
    }
        
    showQueueAddConfirm(tournamentMachine){
        let msg = 'Confirm Queueing Up On '+tournamentMachine.tournament_machine_name;
        let title = 'Confirm Add To Queue'
        if(this.eventPlayer.queue_player_is_in!=null){
            msg = 'WARNING! Player is already queued on '+this.eventPlayer.queue_player_is_in.tournament_machine.tournament_machine_name+'.  Still queue on '+tournamentMachine.tournament_machine_name+'?'
            title = 'WARNING!'
        }
        let confirm = this.alertCtrl.create({
            title: title,
            message: msg,
            buttons: [
                {
                text: 'Cancel'
            },
                {
                text: 'Ok',
                handler: () => {
                    this.addEventPlayerToQueue(tournamentMachine.tournament_machine_id);
                }
            }
            ]
        });
        confirm.present();
    }

    kioskAddEventPlayerToQueue(payload){
        this.pssApi.kioskAddEventPlayerToQueue(payload,this.eventId)
            .subscribe(this.kioskGenerateAddEventPlayerToQueueProcessor())

    }
    
    addEventPlayerToQueue(tournament_machine_id){
        this.pssApi.addEventPlayerToQueue({'player_id':this.eventPlayer.player_id,'tournament_machine_id':tournament_machine_id},this.eventId)
            .subscribe(this.generateAddEventPlayerToQueueProcessor())

    }

    generateConfirmQueueRemove(playerName,queue,tournamentMachine){
        return ()=>{
            let actionSheet = this.actionSheetCtrl.create({title: 'Are you SURE you want to remove '+playerName+' from queue?',
                                                           buttons: [
                                                               {
                                                               text: 'Remove',
                                                               role: 'destructive',
                                                               handler: this.generateRemovePlayerFromQueue(queue,tournamentMachine)
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
    }
    generateRemovePlayerFromQueueProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            let success_title_string=result.data.player_full_name+' has been removed from queue.';            
            
            let successSummary = new SuccessSummary(success_title_string,null,null);            
            let successButtonHome = new SuccessButton('Tournament Queues',
                                                      'QueueSelectPlayerTournamentMachinePage',
                                                      this.buildNavParams({}));
            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButtonHome]}));
            
        }
    }
    
    generateRemovePlayerFromQueue(queue,tournament_machine){
        return ()=>{
            console.log(queue)
            this.pssApi.removePlayerFromQueue({player_id:queue.player.player_id,tournament_machine_id:tournament_machine.tournament_machine_id},this.eventId)            
                .subscribe(this.generateRemovePlayerFromQueueProcessor())
        }                
    }
    generateGetAllTournamentsAndMachinesAndEventPlayerProcessor(withPlayer=false){
        return (result) => {            
            if(result == null){
                return;
            }
            if(withPlayer==true){
                this.eventPlayer=result.player;
            }
            console.log('in getAllTournaments...')
            console.log(result)
            this.tournaments=result.data;
            //let role = null;
            //let loggedInPlayerId = null;
            //if(this.eventAuth.isEventUserLoggedIn(this.eventId)){
            //    role = this.eventAuth.getRoleName(this.eventId);
            //    if(role == 'player'){
                    this.loggedInPlayerId = this.eventAuth.getPlayerId(this.eventId);
            //    }
            //}
            this.tournaments.map((tournament)=>{
                tournament.expanded=false;
                tournament.tournament_machines.map((tournament_machine)=>{
                    tournament_machine.expanded=false;
                    
                    tournament_machine.queues.map((queue)=>{
                        queue.icon='person';
                        let player_name=queue.player!=null?queue.player.player_full_name:null;                        
                        if(this.role==null || this.role=='scorekeeper'){
                            queue.whatToDo=(x,y)=>{};
                        }
                        if(this.role=='player'){
                            console.log('in filter - found player..'+this.loggedInPlayerId)
                            if(queue.player != null && queue.player.player_id==this.loggedInPlayerId){
                                
                                queue.icon='remove-circle';
                                queue.allowedToRemove=true;
                                //queue.whatToDo=this.generateRemovePlayerFromQueue();
                                if(player_name!=null){
                                    queue.whatToDo=this.generateConfirmQueueRemove(player_name,queue,tournament_machine);
                                }                                
                            }
                        }
                        if(this.role=='tournament_director' || this.role=='deskworker'){
                            queue.icon='remove-circle';
                            queue.allowedToRemove=true;
                            //queue.whatToDo=this.generateRemovePlayerFromQueue();                            
                            if(player_name!=null){
                                queue.whatToDo=this.generateConfirmQueueRemove(player_name,queue,tournament_machine);
                            }
                        }
                    })
                })
            })
            this.tournaments.forEach((tournament)=>{
                tournament.tournament_machines=tournament.tournament_machines.sort((n1,n2)=>{
                    console.log(n1)
                    console.log(n2)
                    console.log('-------------')
                    if(n1.tournament_machine_name>n2.tournament_machine_name){
                        return 1;
                    } else {
                        return -1;
                    }
                })
            })
            this.tournaments=this.tournaments.sort((n1,n2)=>{
                if(n1.tournament_name > n2.tournament_name){
                    return 1
                } else {
                    return -1
                }
            })
        };
    }

    onReload(){
        if(this.player_id_for_event==null){                        
            this.pssApi.getAllTournamentsAndMachines(this.eventId)            
                .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor())
        } else {
            
            this.pssApi.getAllTournamentsAndMachinesAndEventPlayer(this.eventId,this.player_id_for_event)            
                .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor(true))
        }
    }
    ionViewDidEnter(){
        console.log('ionViewDidEnter QueueSelectPlayerTournamentMachinePage');
        //console.log(this.navCtrl.parent.getSelected().index)
    }
    ionViewWillEnter() {
            if(this.eventId==null){
                this.pushRootPage('EventSelectPage')
                return;
            }
        if(this.platform.is('core')){
            this.cssColors='desktop';
        } else {
            this.cssColors='queue';
        }

        //this.queueMode=this.navParams.get('queueMode');
        //console.log('ionViewDidLoad QueueSelectPlayerTournamentMachinePage');
        console.log('ionViewDidEnter QueueSelectPlayerTournamentMachinePage');
        //console.log(this.navCtrl.parent.getSelected().index);
        
        this.role=this.eventAuth.getRoleName(this.eventId);
        
        if(this.eventAuth.getRoleName(this.eventId)=='player'){            
            this.loggedInPlayerId = this.eventAuth.getPlayerId(this.eventId);
            this.player_id_for_event=this.eventAuth.getEventPlayerId(this.eventId);            
        }        
        
        if(this.player_id_for_event==null){                        
            this.pssApi.getAllTournamentsAndMachines(this.eventId)            
                .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor())
        } else {
            
            this.pssApi.getAllTournamentsAndMachinesAndEventPlayer(this.eventId,this.player_id_for_event)            
                .subscribe(this.generateGetAllTournamentsAndMachinesAndEventPlayerProcessor(true))
        }
        
        
        console.log(this.role);
  }

}
