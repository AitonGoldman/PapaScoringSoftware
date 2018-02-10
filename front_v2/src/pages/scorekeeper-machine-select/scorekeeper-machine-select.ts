import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { reorderArray } from 'ionic-angular';

/**
 * Generated class for the ScorekeeperMachineSelectPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-scorekeeper-machine-select',
  templateUrl: 'scorekeeper-machine-select.html',
})
export class ScorekeeperMachineSelectPage  extends PssPageComponent {
    tournamentId:any=null;
    tournamentName:any=null;
    tournamentMachines:any=null;
    reorderEnabled:boolean=false;
    undoMode:boolean=false;
    tournamentMachinesOrderList:any=null;;
    generateGetTournamentMachinesProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            let tournamentMachines=result.data;
            tournamentMachines.map((tournament)=>{
                tournament.expanded=false;
            })            
            this.tournamentMachines=tournamentMachines.sort((n1,n2)=>{
                if(n1.tournament_machine_name < n2.tournament_machine_name){
                    return -1;
                }
                if(n1.tournament_machine_name > n2.tournament_machine_name){
                    return 1;
                }
                return 0;                
            })
            this.tournamentMachinesOrderList = this.listOrderStorage.getList('ScorekeeperMachineSelect',this.tournamentId);
            if(this.tournamentMachinesOrderList!=null){
                this.tournamentMachines=this.tournamentMachines.sort((n1,n2)=>{
                    if(this.tournamentMachinesOrderList[n1.tournament_machine_id]!=null && this.tournamentMachinesOrderList[n2.tournament_machine_id]!=null){
                        return this.tournamentMachinesOrderList[n1.tournament_machine_id].index - this.tournamentMachinesOrderList[n2.tournament_machine_id].index;
                    } else {
                        return 1;
                    }                 
                })            
            }                                                
        };
    }

    generateForceStartProcessor(tournamentMachine){
        return (result)=>{
            if(result==null){
                return;
            }
            this.undoMode=false;
            tournamentMachine.player_id=result.data.player_id;
            tournamentMachine.player=result.data.player;
                        let toast = this.toastCtrl.create({
                            message:  "Player "+result.data.player.player_full_name+" added to  "+tournamentMachine.tournament_machine_name,
                            duration: 99000,
                            position: 'top',
                            showCloseButton: true,
                            closeButtonText: " ",
                            cssClass: "successToast"
                        });            
            toast.present();                                                    
            this.undoMode=false;            
        }
    }

    generateInsertIntoQueueProcessor(tournamentMachine){
        return (result)=>{
            if(result==null){
                return;
            }
            tournamentMachine.player_id=null;
            tournamentMachine.player=null;
            console.log(result);
            let toast = this.toastCtrl.create({
                message:  result.data.queues[0].player.player_full_name+" inserted into queue for "+tournamentMachine.tournament_machine_name,
                duration: 99000,
                position: 'top',
                showCloseButton: true,
                closeButtonText: " ",
                cssClass: "successToast"
            });
            this.undoMode=false;
            toast.present();                                                                
        }
    }
    
    generateRemovePlayerProcessor(tournamentMachine){
        return (result)=>{
            if(result==null){
                return;
            }
            tournamentMachine.player_id=null;
            tournamentMachine.player=null;
            let toast = this.toastCtrl.create({
                message:  "Player removed from "+tournamentMachine.tournament_machine_name,
                duration: 99000,
                position: 'top',
                showCloseButton: true,
                closeButtonText: " ",
                cssClass: "successToast"
            });
            this.undoMode=false;
            toast.present();                                                    
            
        }
    }
    
    generateInsertIntoQueue(tournamentMachine){
        return ()=>{
        let alert = this.alertCtrl.create({
            title: 'Force Start Player On Machine',
            inputs: [
                {
                name: 'player_id_for_event',
                placeholder: 'Player Number'
            }
            ],
            buttons: [
                {
                text: 'Cancel',
                role: 'cancel',
                handler: data => {
                    console.log('Cancel clicked');
                }
            },
                {
                text: 'Insert Player Into Queue',
                handler: (data) => {
                    console.log(data);
                    this.pssApi.bumpPlayerDownQueue({action:"insert",
                                                     player_id_for_event:data.player_id_for_event,
                                                     tournament_id:this.tournamentId,
                                                     tournament_machine_id:tournamentMachine.tournament_machine_id},
                                                    this.eventId)
                        .subscribe(this.generateInsertIntoQueueProcessor(tournamentMachine))                                                                          
                }
            }
            ]
        });
        alert.present();        
            
        }
    }
    
    generateForceAddPlayer(tournamentMachine){
        return ()=>{
        let alert = this.alertCtrl.create({
            title: 'Force Start Player On Machine',
            inputs: [
                {
                name: 'player_id_for_event',
                placeholder: 'Player Number'
            }
            ],
            buttons: [
                {
                text: 'Cancel',
                role: 'cancel',
                handler: data => {
                    console.log('Cancel clicked');
                }
            },
                {
                text: 'Force Start Player',
                handler: (data) => {
                    console.log(data);
                     this.pssApi.startPlayerOnMachine({action:'force_start',
                                                       player_id_for_event:data.player_id_for_event,
                                                       tournament_machine_id:tournamentMachine.tournament_machine_id},
                                                       this.eventId)
                        .subscribe(this.generateForceStartProcessor(tournamentMachine))                                                  

                }
            }
            ]
        });
        alert.present();        
            
        }
    }
    
    generateRemovePlayerFromMachine(tournamentMachine){
        return ()=>{
            this.pssApi.submitScore({tournament_machine_id:tournamentMachine.tournament_machine_id,
                                     action:'force_remove',
                                     tournament_id:this.tournamentId,
                                     player_id:tournamentMachine.player_id},this.eventId)            
            .subscribe(this.generateRemovePlayerProcessor(tournamentMachine))        
        }
    } 
       

    onOops(tournamentMachine){
        let buttons = []
        console.log(tournamentMachine);
        if(tournamentMachine.player_id!=null){
            buttons.push(
                {
                text: 'Remove Player From Machine',
                role: 'destructive',
                handler: this.generateRemovePlayerFromMachine(tournamentMachine)
            })
        } else {
            buttons.push(
                {
                text: 'Force Start Player on Machine',
                role: 'destructive',
                handler: this.generateForceAddPlayer(tournamentMachine)
            })
        }
        if(this.eventAuth.getRoleName(this.eventId)=="tournament_director"){
            buttons.push(
                {
                text: 'Insert Into Queue',
                role: 'destructive',
                handler: this.generateInsertIntoQueue(tournamentMachine)
            })            
        }
        buttons.push({
            text: 'Cancel',
            role: 'cancel',
            handler: () => {
                console.log('Cancel clicked');
            }
        })
        let actionSheetOptions = {title: tournamentMachine.tournament_machine_name.toUpperCase(),
                                  buttons: buttons// [
                                  //     {
                                  //     text: 'Remove Player From Machine',
                                  //     role: 'destructive',
                                  //     handler: this.generateRemovePlayerFromMachine(tournamentMachine)
                                  // },
                                  //     {
                                  //     text: 'Force Start Player on Machine',
                                  //     role: 'destructive',
                                  //     handler: this.generateForceAddPlayer(tournamentMachine)
                                  // },

                                  //     {
                                  //     text: 'Cancel',
                                  //     role: 'cancel',
                                  //     handler: () => {
                                  //         console.log('Cancel clicked');
                                  //     }
                                  // }
                                  // ]
                                 }        
        let actionSheet = this.actionSheetCtrl.create(actionSheetOptions);            
        actionSheet.present();                
    }
    
    reorderTournamentMachineItems(indexes) {
        
        this.tournamentMachines = reorderArray(this.tournamentMachines, indexes);
        
        let tournamentMachinesListToStore = {}
        this.tournamentMachines.forEach((item,index)=>{            
            tournamentMachinesListToStore[item.tournament_machine_id]={index:index+1,tournament_machine_id:item.tournament_machine_id};
        }) 
        this.listOrderStorage.updateList('ScorekeeperMachineSelect',this.tournamentId,tournamentMachinesListToStore)
    }

    ionViewWillLoad() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

        this.tournamentId=this.navParams.get('tournamentId');
        this.tournamentName=this.navParams.get('tournamentName');

        this.pssApi.getTournamentMachines(this.eventId,this.tournamentId)
            .subscribe(this.generateGetTournamentMachinesProcessor())    

      console.log('ionViewDidLoad ScorekeeperMachineSelectPage');
    }
    reorderItems(indexes) {
        this.tournamentMachines = reorderArray(this.tournamentMachines, indexes);
    }

    generateGetTournamentsMachineProcessor(tournamentMachineId){
        return (result) => {            
            if(result == null){
                return;
            }                        
            // let tournamentMachine=null;
            // result.data.forEach((tournament, index) => {
            //     tournament.tournament_machines.forEach((tournament_machine,machine_index)=>{
            //         if(tournament_machine.tournament_machine_id==tournamentMachineId){
            //             tournamentMachine=tournament_machine;
            //         }
            //     })
            // });
            let tournamentMachine=result.data;
            let nextPageString:string = "ScorekeeperStartPlayerPage"
            if(tournamentMachine.player_id!=null){
                nextPageString = "ScorekeeperRecordScorePage"
            } 
            this.navCtrl.push(nextPageString,            
                              this.buildNavParams({tournamentId:this.tournamentId,
                                                   tournamentMachineId:tournamentMachineId,
                                                   tournamentMachine:tournamentMachine,
                                                   tournamentCounts:tournamentMachine.tournament_counts}));                        
        };
    }
    
    pushToMachine(tournamentMachine){
        
        console.log('push to machine id is '+tournamentMachine.tournament_machine_id)
        if(this.undoMode==true){
            this.onOops(tournamentMachine)
        } else {
            this.pssApi.getTournamentMachine(this.eventId,this.tournamentId,tournamentMachine.tournament_machine_id)            
                .subscribe(this.generateGetTournamentsMachineProcessor(tournamentMachine.tournament_machine_id))
        }
        
    }

}
