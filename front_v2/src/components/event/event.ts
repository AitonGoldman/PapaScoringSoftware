import { Component } from '@angular/core';
import { EntityFields } from '../../classes/entity-fields'
import { PssPageComponent } from '../pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';
import { TakePicComponent } from '../../components/take-pic/take-pic'

/**
 * Generated class for the EventComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */

const eventDescriptions={
    'name':{
        'short':'Name of the event.',
        'long':'Name of the event (i.e. PAPA 25, INDISC 2018, etc).',        
    },
    'number_unused_tickets_allowed':
    {
        'short':'Number of unused tickets allowed.',
        'long':'Number of unused tickets a player is allowed to have.  This takes into account any tickets the player is currently using.',        
    },
    'stripe_api_key':
    {
        'short':'Stripe Api key.',
        'long':'The private Stripe Api key.',        
    },
    'stripe_public_key':
    {
        'short':'Stripe public Api key.',
        'long':'The public Stripe Api Key.',        
    },
    'force_ifpa_lookup':
    {
        'short':'Force IFPA ranking lookup.',
        'long':'When registering player for events, force an IFPA ranking lookup.  This ranking will be used for IFPA ranking restrictions.',        
    },
    'active':
    {
        'short':'Make event active/inactive',
        'long':'Make event active/inactive',        
    }


}


@Component({
  selector: 'event',
  templateUrl: 'event.html'
})
export class EventComponent  extends PssPageComponent {
    entityFields:EntityFields;    
    entity:any = {};
    actionType:string;    
    destPageAfterSuccess:string;
    wizardMode:any=null;
    wizardModeNextPage:string;        
    advanced:boolean=false;
    entityFieldsArray:any=null;
    
    ionViewWillLoad() {        
        // if(this.eventId==null){
        //     this.pushRootPage('EventSelectPage')
        //     return;
        // }
        this.actionType=this.navParams.get('actionType');                
        this.eventId = this.navParams.get('eventId');
        this.wizardMode = this.navParams.get('wizardMode');
        this.entityFields = new EntityFields("event");        
        this.entityFields.setField('name','text',true,false,eventDescriptions['name']);        
        this.entityFields.setField('number_unused_tickets_allowed','number',true,false,eventDescriptions['number_unused_tickets_allowed']);
        this.entityFields.setField('active','boolean',true,false,eventDescriptions['active']);        
        this.entityFields.setField('stripe_api_key','text',false,true,eventDescriptions['stripe_api_key']);
        this.entityFields.setField('stripe_public_key','text',false,true,eventDescriptions['stripe_public_key']);
        this.entityFields.setField('force_ifpa_lookup','boolean',false,true,eventDescriptions['force_ifpa_lookup']);
        
        this.entityFieldsArray=this.entityFields.getFieldsArray(this.advanced);
        if (this.actionType=="edit"){
            this.pssApi.getEvent(this.eventId)
                .subscribe(this.generateGetEventProcessor())    

        }        
    }
    onAdvancedChange(){
        this.entityFieldsArray=this.entityFields.getFieldsArray(this.advanced);        
    }
    generateGetEventProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            this.entity=result.data;            
        };
        
    }
    takePicture(){
        let profileModal = this.modalCtrl.create(TakePicComponent, { userId: 8675309 });
        profileModal.onDidDismiss(data => {
            console.log('in modal...');
            console.log(data);
            if(data!=null){                
                this.entity.img_file=data;
                this.entity.has_pic=true;                
            }
        });
        profileModal.present();
    }

    generateEditEventProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            let success_title_string='Event '+result.data.name+' has been edited.';
            let successSummary = new SuccessSummary(success_title_string,null,null);            
            let successButton = new SuccessButton('Go Home',
                                                  this.destPageAfterSuccess,
                                                  this.buildNavParams({wizardMode:this.wizardMode}));            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButton]}));
        };
    }
    
    generateCreateEventProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            let success_title_string='Event '+result.data.name+' has been created.';
            let successSummary = new SuccessSummary(success_title_string,null,null);            
            let successButton = new SuccessButton('Go Home',
                                                  this.destPageAfterSuccess,
                                                  this.buildNavParams({wizardMode:this.wizardMode}));            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'ignoreEventId':true,
                                                   'successSummary':successSummary,
                                                   'successButtons':[successButton]}));
        };
    }

    wizardCreateEventSubmit(){        
        let success_title_string='Event '+this.entity['name']+' has been recorded.';
        let success_first_line='Click "Proceed" button to proceed.';
        
        let successSummary = new SuccessSummary(success_title_string,success_first_line,null);            
        let successButton = new SuccessButton('Proceed',
                                              this.wizardModeNextPage,
                                              this.buildNavParams({wizardMode:this.wizardMode,
                                                                   wizardEntity:{'event':this.entity},
                                                                   actionType:'create'}));            
        this.navCtrl.push("SuccessPage",            
                          this.buildNavParams({'ignoreEventId':true,
                                               'successSummary':successSummary,
                                               'successButtons':[successButton]}));
        
    }
    
    processEntity(){
        
        if(this.wizardMode!=null && this.wizardMode==true){
            this.wizardCreateEventSubmit();
            return
        }
        if (this.actionType=="create"){
            this.pssApi.createEvent(this.entity)
                .subscribe(this.generateCreateEventProcessor())                                                  
        }
        if (this.actionType=="edit"){
            this.pssApi.editEvent(this.entity)
                .subscribe(this.generateEditEventProcessor())                                                  
        }                            
    }

    //FIXME : needs to be shared between tourney and event
    onUploadFinished(event){
        this.entity.has_pic=true;
        this.entity.img_file=JSON.parse(event.serverResponse._body).data;        
    }
    onSubmit(){

    }
}
