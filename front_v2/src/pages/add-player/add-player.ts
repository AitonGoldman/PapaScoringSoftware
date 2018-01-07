import { ViewChild, Component } from '@angular/core';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { AutoCompleteProvider } from '../../providers/auto-complete/auto-complete';
import { Platform, App, NavParams, NavController } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { AlertController } from 'ionic-angular';

import { ActionSheetController } from 'ionic-angular'
import { NotificationsService } from 'angular2-notifications';
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';
import { IonicPage } from 'ionic-angular';



/**
 * Generated class for the AddPlayerPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'AddPlyer/:eventId'
})
@Component({
  selector: 'page-add-player',
  templateUrl: 'add-player.html',
})
export class AddPlayerPage extends PssPageComponent {
    selectedPlayer:any={};
    loading:boolean=false;
    existingPlayerFound:boolean=true;
    @ViewChild('searchbar')  searchbar: any;    
    constructor(public autoCompleteProvider:AutoCompleteProvider,
                public eventAuth: EventAuthProvider,
                public navParams: NavParams,
                public navCtrl: NavController,
                public appCtrl: App,
                public pssApi: PssApiProvider,
                public platform: Platform,                
                public actionSheetCtrl: ActionSheetController,
                public notificationsService: NotificationsService,
                public alertCtrl: AlertController){
        super(eventAuth,navParams,
              navCtrl,appCtrl,
              pssApi,platform,
              notificationsService);
    }

    ionViewDidLoad() {
        console.log('ionViewDidLoad AddPlayerPage');
    }

    generateAddEventPlayersProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            console.log('in generateAddEventPlayerProcessor')
            console.log(result);
            let success_title_string='Player '+result.data[0].player_full_name+' has been added to event.';
            let success_line_one_string='Player Pin is '+result.data[0].pin;
            let success_line_two_string='Player Number is '+result.data[0].events[0].player_id_for_event;
            let successSummary = new SuccessSummary(success_title_string,success_line_one_string,success_line_two_string);            
            let successButton = new SuccessButton('Go Home',
                                                  this.getHomePageString(this.eventId),
                                                  this.buildNavParams({}));            
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButton]}));
        };
    }
    
    generateSearchPlayerProcessor(){
        return (result)=>{
            console.log('in generateSearchPlayerProcessor')
            console.log(result);
        }
    }
    generateGetIfpaRankingProcessor(){
        return (result)=>{
            console.log('in generateGetIfpaRankingProcessor')
            if(result==null){
                return;
            }            
            console.log(result);
            if(result.ifpa_ranking.search.length==0){
                let alert = this.alertCtrl.create();
                alert.setTitle('No IFPA Players Found');
                alert.setMessage('No players found with the name specified.  Please change the name and try again.')
                alert.addButton('Ok');
                alert.present();                                
            }
            if(result.ifpa_ranking.search.length==1){
                this.selectedPlayer.ifpa_ranking=result.ifpa_ranking.search[0].wppr_rank
            }
            if(result.ifpa_ranking.search.length>1){
                let alert = this.alertCtrl.create();
                alert.setTitle('Multiple IFPA Players Found');
                alert.setSubTitle('Select Correct Player');
                for(let ifpaPlayer of result.ifpa_ranking.search){
                    alert.addInput({
                        type: 'radio',
                        label: ifpaPlayer.first_name+" (rank : "+ifpaPlayer.wppr_rank+")",
                        value: ifpaPlayer.wppr_rank                        
                    });

                }

                alert.addButton('Cancel');
                alert.addButton({
                    text: 'OK',
                    handler: data => {
                        this.selectedPlayer.ifpa_ranking=data;                        
                    }
                });
                alert.present();                                
            }
        }
    }
    
    onFocus(){
        this.selectedPlayer={first_name:null,last_name:null};
    }

    onSelected(){
        this.existingPlayerFound=false;
        this.getIfpaRanking(this.selectedPlayer.first_name+" "+this.selectedPlayer.last_name)
    }
    
    getIfpaRanking(playerName){
        this.pssApi.getIfpaRanking(playerName)
            .subscribe(this.generateGetIfpaRankingProcessor())                    
    }

    onChange(event){
        console.log('in onChange...')
        console.log(event)
    }
    
    onInput(event){        
        console.log('in onInput...')
        this.loading=true;
        console.log(this.searchbar)
    }
    
    onItemsShown(event){
        console.log('onItemsShown...')
        //this.loading=true;
    }

    generateLoadingFunction(){
        return (input)=>{
            console.log('in loading function');
            console.log(input);
            if (input.length==0){
                if(this.searchbar.keyword.length > 2){                
                    console.log(this.searchbar.suggestions.length);
                    this.existingPlayerFound=false;
                    let nameElements=this.searchbar.keyword.split(' ');
                    if(nameElements.length>0){
                        this.selectedPlayer.first_name=nameElements[0];
                    }
                    if(nameElements.length>1){
                        this.selectedPlayer.last_name=nameElements[1];
                    }
                }
            } else {
                this.existingPlayerFound=true;            
            }
            this.loading=false;            
        }
    }
  ionViewWillLoad() {
      console.log('ionViewDidLoad AddPlayerPage');
      this.eventId = this.navParams.get('eventId')
      this.autoCompleteProvider.setPlayerSearchType("allPlayers",
                                                    this.generateLoadingFunction());      
      //this.autoCompleteProvider.setPlayers(true);
      //this.pssApi.searchPlayers('poop2')
      //    .subscribe(this.generateSearchPlayerProcessor())            
      
  }
    onUploadFinished(event){
        this.selectedPlayer.has_pic=true;
        this.selectedPlayer.img_file=JSON.parse(event.serverResponse._body).data;        

        console.log(JSON.parse(event.serverResponse._body).data);
    }
    onSubmit(){
        this.pssApi.addEventPlayers({players:[this.selectedPlayer]},this.eventId)
            .subscribe(this.generateAddEventPlayersProcessor())                                                  

    }
    
}
