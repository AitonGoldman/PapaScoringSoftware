import { Component } from '@angular/core';
import { EntityFields } from '../../classes/entity-fields'
import { PssPageComponent } from '../pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';

/**
 * Generated class for the CreateEditEntityComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
const entityDescriptions={
    'event':{
        'name':{
            'short':'Name of the event.',
            'long':'Name of the event (i.e. PAPA 25, INDISC 2018, etc).',
            'type': 'text'
        },
        'number_unused_tickets_allowed':
        {
            'short':'Number of unused tickets allowed.',
            'long':'Number of unused tickets a player is allowed to have.  This takes into account any tickets the player is currently using.',
            'type': 'text'
        }
    },
    'tournament':{
        'tournament_name':{
            'short':'Name of the tournament.',
            'long':'Name of the tournament (i.e. Classics I, Main A, etc).',
            'type':'text'
        },
        'multi_division_tournament':{
            'short':'Multiple divisions.',
            'long':'Create a tournament with multiple divisions (i.e. Main A, Main B, Main C, etc).',
            'type':'boolean'            
        },
        'division_count':{
            'short':'Number of divisions in multi-division tournament',
            'long':'Number of divisions in multi-division tournament',
            'type':'text'            
        },
        'queuing':{
            'short':'Queuing',
            'long':'Enable/Disable queues',
            'type':'boolean'            
        },'manually_set_price':{
            'short':'Price of single ticket',
            'long':'Price of single ticket',
            'type':'text'            
        },'number_of_qualifiers':{
            'short':'Top X players will qualify for finals',
            'long':'Top X players will qualify for finals',
            'type':'text'            
        }        
    }
}
@Component({
  selector: 'create-edit-entity',
  templateUrl: 'create-edit-entity.html'
})
export class CreateEditEntityComponent extends PssPageComponent {
    
    entityFields:EntityFields;    
    entityDescriptions=entityDescriptions;
    entity = {};
    entityType:string;
    actionType:string;    
    destPageAfterSuccess:string='TournamentDirectorHomePage'
    wizardMode:boolean=false;
    wizardModeStack:string=null;
    wizardModeIndex:number=null;   
    
    ionViewWillLoad() {
        
        //this.entityType=this.navParams.get('entityType');
        this.actionType=this.navParams.get('actionType');
        this.eventId = this.navParams.get('eventId');
        this.entityFields = new EntityFields(this.entityType);
        this.wizardMode = this.navParams.get('wizardMode');
        this.wizardModeIndex = this.navParams.get('wizardModeIndex');
        this.wizardModeStack = this.navParams.get('wizardModeStack');
        
        
        
        if(this.entityType=="event"){            
            this.entityFields.setField('name','text',false,true,{short:"",long:""});
            this.entityFields.setField('number_unused_tickets_allowed','text',false,true,{short:"",long:""});
            if (this.actionType=="edit"){
                //get the entity
            }
        }
        if(this.entityType=="tournament"){
            console.log('in tournament create....')
            this.entityFields.setField('tournament_name','text',false,true, {short:"",long:""});
            this.entityFields.setField('multi_division_tournament','boolean',false,true, {short:"",long:""});
            this.entityFields.setField('division_count','text',false,true, {short:"",long:""});
            this.entityFields.setDependency('division_count','multi_division_tournament',true)
            this.entityFields.setField('queuing','boolean',false,true, {short:"",long:""});
            this.entityFields.setField('manually_set_price','text',false,true, {short:"",long:""});
            this.entityFields.setField('number_of_qualifiers','text',false,true, {short:"",long:""});
            
            if (this.actionType=="edit"){
                //get the entity
            }
        }
        
        
        console.log('ionViewDidLoad CreateEditEntity');        
    }
    
    generateCreateEventProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            let successSummary = new SuccessSummary('Event '+result.data.name+' has been created.',
                                                    null,
                                                    null);            
            let successButton = new SuccessButton('Go Home',
                                                  "EventOwnerHomePage",
                                                  this.buildNavParams({}));            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButton]}));
        };
    }

    generateCreateTournamentProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            console.log('in create tourney processor ...');            
            let successSummary = new SuccessSummary('Tournament '+result.data[0].tournament_name+' has been created.',
                                                    null,
                                                    null);            
            let successButton = new SuccessButton('Go Home',
                                                  this.destPageAfterSuccess,
                                                  this.buildNavParams({}));            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButton]}));
        };
    }
    
    processEntity(){
        if(this.entityType=="event"){
            if (this.actionType=="create"){
                console.log('in process entity....');
                
                if(this.wizardMode!=true){
                    this.pssApi.createEvent(this.entity)
                        .subscribe(this.generateCreateEventProcessor())                                      
                }
            }            
        }        
        if(this.entityType=="tournament"){
            if (this.actionType=="create"){
                console.log('in process entity....');
                this.entity['event_id']=this.eventId;
                if(this.wizardMode!=true){

                    this.pssApi.createTournament({tournament:this.entity,division_count:this.entity['division_count'],multi_division_tournament:this.entity['multi_division_tournament']},this.eventId)                
                    .subscribe(this.generateCreateTournamentProcessor())    
                }                            
            }            
        }
        if(this.wizardMode==true){
            
        }
    }
}
