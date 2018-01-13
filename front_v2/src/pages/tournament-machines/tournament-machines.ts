import { ViewChild, Component } from '@angular/core';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { AutoCompleteProvider } from '../../providers/auto-complete/auto-complete';
import { List, Platform, App, NavParams, NavController } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { ActionSheetController } from 'ionic-angular'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';
import { NotificationsService } from 'angular2-notifications';
import { IonicPage } from 'ionic-angular';

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
    templateUrl: '../../components/tournament-machines/tournament-machines.html',
})

export class TournamentMachinesPage extends PssPageComponent {
    destPageAfterSuccess:string;
    wizardMode:any=null;
    wizardEntity:any=null;        
    machines:any;    
    selectedMachine:any;
    sliding:boolean = true;
    selectedMachines:any = [];
    @ViewChild('searchbar')  searchbar: any;
    @ViewChild('myform')  myform: any;

    @ViewChild(List)  list: List;
    
    constructor(public autoCompleteProvider:AutoCompleteProvider,
                public eventAuth: EventAuthProvider,
                public navParams: NavParams,
                public navCtrl: NavController,
                public appCtrl: App,
                public pssApi: PssApiProvider,
                public platform: Platform,
                
                public actionSheetCtrl: ActionSheetController,
                public notificationsService: NotificationsService ){
        super(eventAuth,navParams,
              navCtrl,appCtrl,
              pssApi,platform,
              notificationsService)
    }
    generateGetAllTournamentMachinesProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }            
            this.autoCompleteProvider.setMachines(result.data.machines_list);
            this.selectedMachines=result.data.tournament_machines_list;            
        };
    }
    
    generateGetAllMachinesProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            this.autoCompleteProvider.setMachines(result.data);            
        };
    }
    
    generateAddEditTournamentMachineProcessor(message_string,action){
        return (result) => {            
            if(result == null){
                return;
            }
            //toast.present();
            this.notificationsService.success("Success", message_string,{
                timeOut:0,
                position:["top","right"],
                theClass:'poop'
            })
            
            if(action=="add"){
                this.selectedMachines[this.selectedMachines.length-1]=result.data;
            }
        };
        
    }

    generateCreateWizardProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            let successTitle='Fix This Message';
            let successSummary = new SuccessSummary(successTitle,
                                                    null,
                                                    null);            
            let successButton = new SuccessButton('Go Home',
                                                  this.getHomePageString(),
                                                  this.buildNavParams({}));            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButton]}));
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
        if(this.wizardMode!=null){
            return;
        }        
        this.pssApi.editTournamentMachine(machine,this.eventId)
            .subscribe(this.generateAddEditTournamentMachineProcessor(machine.tournament_machine_name+" has been removed!","edit"))            

    }
    onInput(event){        
    }
    onItemsShown(event){
        
    }
    onDisable(machine){
        machine.active=machine.active==false;
        if(this.wizardMode!=null){
            return;
        }
        let stringDescription = machine.active==true ? "enabled" : "disabled"
        this.pssApi.editTournamentMachine(machine,this.eventId)
            .subscribe(this.generateAddEditTournamentMachineProcessor(machine.tournament_machine_name+" has been "+stringDescription,"edit"))            
    }
    onSelect(event){
        
        this.selectedMachine.tournament_id=this.tournamentId;
        this.selectedMachine.tournament_machine_name=this.selectedMachine.machine_name;        
        //this.selectedMachine=result.data;
        this.selectedMachines.push(this.selectedMachine);
        if(this.wizardMode!=null){
            return;
        }
        this.pssApi.addTournamentMachine(this.selectedMachine,this.eventId)
            .subscribe(this.generateAddEditTournamentMachineProcessor(this.selectedMachine.tournament_machine_name+" has been added","add"))            

    }
    onSubmit(){
        this.wizardEntity['tournament_machines']=this.selectedMachines;
        if('event' in this.wizardEntity){
            this.pssApi.createWizardEvent(this.wizardEntity)
                .subscribe(this.generateCreateWizardProcessor())            
        } else {
            this.wizardEntity['tournament']['tournament']['event_id']=this.eventId
            this.pssApi.createWizardTournament(this.wizardEntity)
                .subscribe(this.generateCreateWizardProcessor())            
        }
        
    }
    onFocus(){
        this.selectedMachine=null;
    }
    ionViewWillLoad() {
        //this.targetEventId=this.navParams.get('eventId');
        this.tournamentId=this.navParams.get('tournamentId');
        this.eventId=this.navParams.get('eventId');
        this.wizardMode=this.navParams.get('wizardMode');
        this.wizardEntity=this.navParams.get('wizardEntity');
        
        if(this.wizardMode==null){
            this.pssApi.getAllTournamentMachines(this.eventId,this.tournamentId)
                .subscribe(this.generateGetAllTournamentMachinesProcessor())    
        } else {
            this.pssApi.getAllMachines()
                .subscribe(this.generateGetAllMachinesProcessor())                
        }
        
        console.log('ionViewDidLoad TournamentMachinesPage');
        
    }    
}
