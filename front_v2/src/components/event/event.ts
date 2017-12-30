import { Component } from '@angular/core';
import { EntityFields } from '../../classes/entity-fields'
import { PssPageComponent } from '../pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';

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

    ionViewWillLoad() {        
        this.actionType=this.navParams.get('actionType');        
        this.entityFields = new EntityFields("event");
        this.wizardMode = this.navParams.get('wizardMode');
        
        this.entityFields.setField('name','text',false,true,eventDescriptions['name']);
        this.entityFields.setField('number_unused_tickets_allowed','text',false,true,eventDescriptions['number_unused_tickets_allowed']);
        if (this.actionType=="edit"){
            //get the entity
        }        
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
                              this.buildNavParams({'successSummary':successSummary,
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
                          this.buildNavParams({'successSummary':successSummary,
                                               'successButtons':[successButton]}));
        
    }
    
    processEntity(){
        console.log('process entity...'+this.wizardMode);
        if(this.wizardMode!=null){
            this.wizardCreateEventSubmit();
            return
        }
        if (this.actionType=="create"){
            this.pssApi.createEvent(this.entity)
                .subscribe(this.generateCreateEventProcessor())                                                  
        }                    
    }
}
