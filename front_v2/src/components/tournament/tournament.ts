import { Component } from '@angular/core';
import { EntityFields } from '../../classes/entity-fields'
import { PssPageComponent } from '../pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';

const tournamentDescriptions={
        'tournament_name':{
            'short':'Name of the tournament.',
            'long':'Name of the tournament (i.e. Classics I, Main A, etc).'
        },
        'multi_division_tournament':{
            'short':'Multiple divisions.',
            'long':'Create a tournament with multiple divisions (i.e. Main A, Main B, Main C, etc).'
        },
        'division_count':{
            'short':'Number of divisions in multi-division tournament',
            'long':'Number of divisions in multi-division tournament'
        },
        'queuing':{
            'short':'Queuing',
            'long':'Enable/Disable queues'
        },'manually_set_price':{
            'short':'Price of single ticket',
            'long':'Price of single ticket'
        },'number_of_qualifiers':{
            'short':'Top X players will qualify for finals',
            'long':'Top X players will qualify for finals'
        }        
}

/**
 * Generated class for the TournamentComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
@Component({
  selector: 'tournament',
  templateUrl: 'tournament.html'
})
export class TournamentComponent extends PssPageComponent{
    entityFields:EntityFields;    
    entity:any = {};
    wizardEntity:any;
    actionType:string;    
    destPageAfterSuccess:string;
    wizardMode:any=null;
    wizardModeNextPage:string;
    entityFieldsArray:any=null;
    advanced:boolean=false;
    
    ionViewWillLoad() {        
        this.actionType=this.navParams.get('actionType');        
        this.entityFields = new EntityFields("tournament");
        this.wizardMode = this.navParams.get('wizardMode');
        this.eventId = this.navParams.get('eventId');
        this.tournamentId = this.navParams.get('tournamentId');
        
        let wizardEntity = this.navParams.get('wizardEntity');
        if(wizardEntity != null){
            this.wizardEntity = wizardEntity;
        }

        this.entityFields.setField('tournament_name','text',true,false, tournamentDescriptions['tournament_name']);
        this.entityFields.setField('multi_division_tournament','boolean',true,false, tournamentDescriptions['multi_division_tournament']);
        this.entityFields.setField('division_count','text',true,false, tournamentDescriptions['division_count']);
        this.entityFields.setDependency('division_count','multi_division_tournament',true)
        this.entityFields.setField('queuing','boolean',true,false, tournamentDescriptions['queuing']);
        this.entityFields.setField('manually_set_price','text',true,false, tournamentDescriptions['manually_set_price']);
        this.entityFields.setField('number_of_qualifiers','text',true,false, tournamentDescriptions['number_of_qualifiers']);
        this.entityFieldsArray=this.entityFields.getFieldsArray(this.advanced);
        
        if (this.actionType=="edit"){
            this.pssApi.getTournament(this.eventId,this.tournamentId)
                .subscribe(this.generateGetTournamentProcessor())                
        }        
    }
    generateGetTournamentProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            this.entity=result.data;            
        };
        
    }
    
    onAdvancedChange(){
        this.entityFieldsArray=this.entityFields.getFieldsArray(this.advanced);        
    }
    generateEditTournamentProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            let success_title_string='Tournament '+result.data.tournament_name+' has been edited.';
            let successSummary = new SuccessSummary(success_title_string,null,null);            
            let successButton = new SuccessButton('Go Home',
                                                  this.destPageAfterSuccess,
                                                  this.buildNavParams({wizardMode:this.wizardMode}));            
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
            let successTitle='Tournament '+result.data[0].tournament_name+' has been created.';
            let successSummary = new SuccessSummary(successTitle,
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

    wizardCreateTournamentSubmit(){
        
        let success_title_string='Tournament '+this.entity['tournament_name']+' has been recorded.';
        let success_first_line='Click "Proceed" button to proceed.';
        
        let successSummary = new SuccessSummary(success_title_string,success_first_line,null);                    
        if(this.wizardEntity!=null){
            this.wizardEntity['tournament']=this.entity;
        } else {
            this.wizardEntity={tournament:this.entity};
        }
        this.wizardEntity['tournament']={tournament:this.entity,division_count:this.entity['division_count'],multi_division_tournament:this.entity['multi_division_tournament']}
        let successButton = new SuccessButton('Proceed',
                                              this.wizardModeNextPage,
                                              this.buildNavParams({wizardMode:this.wizardMode,
                                                                   wizardEntity:this.wizardEntity}));            
        this.navCtrl.push("SuccessPage",            
                          this.buildNavParams({'successSummary':successSummary,
                                               'successButtons':[successButton]}));
        
    }
    processEntity(){
        
        if(this.wizardMode!=null){
            this.wizardCreateTournamentSubmit();
            return
        }
        if (this.actionType=="create"){
            this.pssApi.createTournament({tournament:this.entity,division_count:this.entity['division_count'],multi_division_tournament:this.entity['multi_division_tournament']},this.eventId)                
                .subscribe(this.generateCreateTournamentProcessor())                    
        }
        if (this.actionType=="edit"){
            this.pssApi.editTournament(this.entity,this.eventId)
                .subscribe(this.generateEditTournamentProcessor())                                                  
        }                                    
    }
    onUploadFinished(event){
        this.entity.has_pic=true;
        this.entity.img_file=JSON.parse(event.serverResponse._body).data;        
    }
    
}
