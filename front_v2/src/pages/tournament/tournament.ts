import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { EntityFields } from '../../classes/entity-fields'
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';
import { TakePicComponent } from '../../components/take-pic/take-pic'

/**
 * Generated class for the TournamentPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

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
        },'use_stripe':{
            'short':'Use Stripe',
            'long':'Use Stripe'
        },'stripe_sku':{
            'short':'Single Ticket Stripe SKU',
            'long':'Single Ticket Stripe SKU'
        },'discount_stripe_sku':{
            'short':'Discount Ticket Stripe SKU',
            'long':'Discount Ticket Stripe SKU'
        },'discount':{
            'short':'Discount',
            'long':'Offer a discount on X number of tickets. '
        },'number_of_tickets_for_discount':{
            'short':'Discount Ticket Amount',
            'long':'Number of tickets to offer a discount on.'            
        },'number_of_signifigant_scores':{
            'short':'Number of signifigant scores',
            'long':'Number of top scores that will be used to calculate player rankings in a tournament'            
        },'allow_phone_purchases':{
            'short':'Allow phone purchases',
            'long':'If disabled, players will be prevented from buying tickets on their phones'            
        },'finals_style':{
            'short':'Finals Style',
            'long':'Finals Style : either PAPA or PPO'            
        },'number_of_qualifiers_for_a_when_finals_style_is_ppo':{
            'short':'Top X players will qualify for A finals',
            'long':'Top X players will qualify for A finals'
        },'number_of_qualifiers_for_b_when_finals_style_is_ppo':{
            'short':'Top X players will qualify for B finals',
            'long':'Top X players will qualify for B finals'
        }
}


@IonicPage()
@Component({
  selector: 'page-tournament',
  templateUrl: '../../components/create-edit-entity/create-edit-entity.html',
})
export class TournamentPage extends PssPageComponent {

    entityFields:EntityFields;
    //FIXME : this should not be hardcoded here
    entity:any = {use_stripe:false};
    wizardEntity:any;
    actionType:string;    
    destPageAfterSuccess:string;
    wizardMode:any=null;
    wizardModeNextPage:string='TournamentMachinesPage';
    entityFieldsArray:any=null;
    advanced:boolean=false;
    
    ionViewWillLoad() {        
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

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
        this.entityFields.setField('division_count','number',true,false, tournamentDescriptions['division_count']);
        this.entityFields.setDependency('division_count','multi_division_tournament',true)
        this.entityFields.setField('queuing','boolean',true,false, tournamentDescriptions['queuing']);
        this.entityFields.setField('discount','boolean',true,false, tournamentDescriptions['discount']);
        this.entityFields.setField('number_of_tickets_for_discount','number',true,false, tournamentDescriptions['number_of_tickets_for_discount']);
        this.entityFields.setDependency('number_of_tickets_for_discount','discount',true)

        this.entityFields.setField('manually_set_price','number',true,false, tournamentDescriptions['manually_set_price']);
        this.entityFields.setDependency('manually_set_price','use_stripe',false)
        this.entityFields.setField('number_of_qualifiers','number',true,false, tournamentDescriptions['number_of_qualifiers']);
        this.entityFields.setDependency('number_of_qualifiers','finals_style','PAPA')

        this.entityFields.setField('number_of_qualifiers_for_a_when_finals_style_is_ppo','number',true,false, tournamentDescriptions['number_of_qualifiers_for_a_when_finals_style_is_ppo']);
        this.entityFields.setField('number_of_qualifiers_for_b_when_finals_style_is_ppo','number',true,false, tournamentDescriptions['number_of_qualifiers_for_b_when_finals_style_is_ppo']);

        this.entityFields.setDependency('number_of_qualifiers_for_a_when_finals_style_is_ppo','finals_style','PPO')
        this.entityFields.setDependency('number_of_qualifiers_for_b_when_finals_style_is_ppo','finals_style','PPO')
        
        this.entityFields.setField('number_of_qualifiers','number',true,false, tournamentDescriptions['number_of_qualifiers']);
        this.entityFields.setDependency('number_of_qualifiers','finals_style','PAPA')
        
        this.entityFields.setField('use_stripe','boolean',false,true, tournamentDescriptions['use_stripe']);
        this.entityFields.setField('allow_phone_purchases','boolean',false,true, tournamentDescriptions['allow_phone_purchases']);

        this.entityFields.setField('stripe_sku','text',false,true, tournamentDescriptions['stripe_sku']);
        this.entityFields.setDependency('stripe_sku','use_stripe',true)
        this.entityFields.setField('discount_stripe_sku','text',false,true, tournamentDescriptions['discount_stripe_sku']);
        this.entityFields.setDependency('discount_stripe_sku','use_stripe',true)
        this.entityFields.setField('number_of_signifigant_scores','number',false,true, tournamentDescriptions['number_of_signifigant_scores']);
        this.entityFields.setField('finals_style','text',false,true, tournamentDescriptions['finals_style']);

        
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
                                                  this.getHomePageString(),
                                                  this.buildNavParams({wizardMode:this.wizardMode}));            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButton]}));
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
                                                  this.getHomePageString(),
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
        console.log('process entity...'+this.wizardMode);
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
