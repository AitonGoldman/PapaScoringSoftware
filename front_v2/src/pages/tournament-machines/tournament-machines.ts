import { ViewChild, Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';
import { TakePicComponent } from '../../components/take-pic/take-pic'

/**
 * Generated class for the TournamentMachinesPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
    selector: 'page-tournament-machines',
    templateUrl: 'tournament-machines.html',
})

export class TournamentMachinesPage extends AutoCompleteComponent {
    destPageAfterSuccess:string;
    wizardMode:any=null;
    wizardEntity:any=null;        
    machines:any;    
    selectedMachine:any;
    sliding:boolean = true;
    selectedMachines:any = [];
    //@ViewChild('searchbar')  searchbar: any;
    @ViewChild('myform')  myform: any;    

    takePicture(machine){
        let profileModal = this.modalCtrl.create(TakePicComponent, { userId: 8675309 });
        profileModal.onDidDismiss(data => {
            console.log('in modal...');
            console.log(data);
            if(data!=null){
                machine.has_pic=true;
                machine.img_file=data;                
                this.pssApi.editTournamentMachine(machine,this.eventId)
                    .subscribe(this.generateAddEditTournamentMachineProcessor(machine.tournament_machine_name+" pic has been updated!","edit"))                            
            }
        });
        profileModal.present();
    }
    
    generateGetAllTournamentMachinesProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }            
            //this.autoCompleteProvider.setMachines(result.data.machines_list);
            this.autoCompleteProvider.initializeAutoComplete('machine_name',
                                                             result.data.machines_list);      
            
            this.selectedMachines=result.data.tournament_machines_list;            
        };
    }
    
    generateGetAllMachinesProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            // this.autoCompleteProvider.setMachines(result.data);
            this.autoCompleteProvider.initializeAutoComplete('machine_name',
                                                             result.data);      
            
        };
    }
    
    generateAddEditTournamentMachineProcessor(message_string,action){
        return (result) => {            
            if(result == null){
                return;
            }            
            let toast = this.toastCtrl.create({
                message:  message_string,
                duration: 99000,
                position: 'top',
                showCloseButton: true,
                closeButtonText: " ",
                cssClass: "successToast"
            });
            toast.present();                                                    

            //toast.present();
            // this.notificationsService.success("Success", message_string,{
            //     timeOut:0,
            //     position:["top","right"],
            //     theClass:'poop'
            // })
            
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
            let eventName:string = "";
            if(this.wizardEntity.event!=null){
                eventName=this.wizardEntity.event.name;
            }
            let tournamentName:string = this.wizardEntity.tournament.tournament.tournament_name;
            
            let successTitle:string="";
            if(eventName!=""){
                successTitle='Event and ';
            }
            successTitle=successTitle+"Tournament Created!";
            let summaryLineOne="Created ";
            if(eventName!=""){
                summaryLineOne=successTitle+'event '+eventName+' and ';
            }
            summaryLineOne=summaryLineOne+'tournament '+tournamentName;
            let successSummary = new SuccessSummary(successTitle,
                                                    summaryLineOne,
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
        console.log('in onSubmit...');
        console.log(this.wizardEntity);
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
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

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
