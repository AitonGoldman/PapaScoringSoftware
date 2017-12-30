import { ViewChild, Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { AutoCompleteProvider } from '../../providers/auto-complete/auto-complete';
import { List, Platform, App, NavParams, NavController } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { ToastController } from 'ionic-angular';
import { ActionSheetController } from 'ionic-angular'

/**
 * Generated class for the TournamentMachinesPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'TournamentMachines/:eventId/:tournamentId'
})
@Component({
  selector: 'page-tournament-machines',
  templateUrl: 'tournament-machines.html',
})
export class TournamentMachinesPage extends PssPageComponent {
    machines:any;    
    selectedMachine:any;
    sliding:boolean = true;
    selectedMachines:any = [];
    @ViewChild('searchbar')  searchbar: AutoCompleteProvider;
    @ViewChild(List)  list: List;
    
    constructor(public autoCompleteProvider:AutoCompleteProvider,
                public eventAuth: EventAuthProvider,
                public navParams: NavParams,
                public navCtrl: NavController,
                public appCtrl: App,
                public pssApi: PssApiProvider,
                public platform: Platform,
                private toastCtrl: ToastController,
                public actionSheetCtrl: ActionSheetController){
        super(eventAuth,navParams,
              navCtrl,appCtrl,
              pssApi,platform)
    }
    generateGetAllMachinesProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            this.autoCompleteProvider.setMachines(result.data.machines_list);
            this.selectedMachines=result.data.tournament_machines_list;
        };
    }
    generateAddEditTournamentMachineProcessor(message_string,action){
        return (result) => {            
            if(result == null){
                return;
            }
                            let toast = this.toastCtrl.create({
                                message: message_string,
                                duration: 99000,
                                position: 'top',
                                showCloseButton: true                    
                });
            toast.present();
            console.log(this.list)            
            if(action=="add"){
                this.selectedMachine=result.data;
                this.selectedMachines.push(this.selectedMachine);
            }
        };
        
    }
    onRemove(machine){
        let actionSheet = this.actionSheetCtrl.create({
            title: 'Are you SURE you want to remove '+machine.tournament_machine_name+'?',
            buttons: [
                {
                text: 'Remove',
                role: 'destructive',
                handler: () => {
                    this.onRemoveConfirmed(machine);
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
    
    onRemoveConfirmed(machine){
        machine.removed=true;        
        this.pssApi.editTournamentMachine(machine,this.eventId)
            .subscribe(this.generateAddEditTournamentMachineProcessor(machine.tournament_machine_name+" has been removed!","edit"))            

    }
        
    onDisable(machine){
        machine.active=machine.active==false;
        let stringDescription = machine.active==true ? "enabled" : "disabled"
        this.pssApi.editTournamentMachine(machine,this.eventId)
            .subscribe(this.generateAddEditTournamentMachineProcessor(machine.tournament_machine_name+" has been "+stringDescription,"edit"))            
    }
    onSelect(){        
        console.log(this.selectedMachine);
        this.selectedMachine.tournament_id=this.tournamentId;
        this.selectedMachine.tournament_machine_name=this.selectedMachine.machine_name;        
        this.pssApi.addTournamentMachine(this.selectedMachine,this.eventId)
            .subscribe(this.generateAddEditTournamentMachineProcessor(this.selectedMachine.tournament_machine_name+" has been added","add"))            

    }
    onFocus(){
        this.selectedMachine=null;
    }
    ionViewWillLoad() {
        //this.targetEventId=this.navParams.get('eventId');
        this.tournamentId=this.navParams.get('tournamentId');
        this.pssApi.getAllMachines(this.eventId,this.tournamentId)
            .subscribe(this.generateGetAllMachinesProcessor())    
        
        console.log('ionViewDidLoad TournamentMachinesPage');
    }

}
