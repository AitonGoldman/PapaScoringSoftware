import { ViewChild, Component } from '@angular/core';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { TakePicComponent } from '../../components/take-pic/take-pic'

import { AutoCompleteProvider } from '../../providers/auto-complete/auto-complete';
import { ModalController, Platform, App, NavParams, NavController } from 'ionic-angular';
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
    segment:'AddPlayer/:eventId'
})
@Component({
  selector: 'page-add-player',
  templateUrl: 'add-player.html',
})
export class AddPlayerPage extends PssPageComponent {
    selectedPlayer:any={};
    loading:boolean=false;
    ifpaLookup:boolean=false;
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
                public alertCtrl: AlertController,
                public modalCtrl: ModalController){
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
            
            let success_title_string='Player '+result.data[0].player_full_name+' has been added to event.';
            let success_line_one_string='Player Pin is '+result.data[0].pin;
            let success_line_two_string='Player Number is '+result.data[0].events[0].player_id_for_event;
            let successSummary = new SuccessSummary(success_title_string,success_line_one_string,success_line_two_string);            
            let successButtonHome = new SuccessButton('Go Home',
                                                  this.getHomePageString(this.eventId),
                                                      this.buildNavParams({}));
            let successButtonTickets = new SuccessButton('Purchase Tickets',
                                                         'TicketPurchasePage',
                                                         this.buildNavParams({player_id_for_event:result.data[0].events[0].player_id_for_event}));            
            
            this.navCtrl.push("PostPlayerAddSuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButtonHome,successButtonTickets]}));
        };
    }
    
    generateSearchPlayerProcessor(){
        return (result)=>{
            console.log('in generateSearchPlayerProcessor')
            
        }
    }
    takePicture(){
        let profileModal = this.modalCtrl.create(TakePicComponent, { userId: 8675309 });
        profileModal.onDidDismiss(data => {
            console.log('in modal...');
            console.log(data);
            if(data!=null){
                this.selectedPlayer.has_pic=true;
                this.selectedPlayer.img_file=data;
            }
        });
        profileModal.present();
    }
    
    generateGetIfpaRankingProcessor(){
        return (result)=>{
            console.log('in generateGetIfpaRankingProcessor')
            if(result==null){
                return;
            }            
            this.ifpaLookup=true;
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
        this.ifpaLookup=true;
        this.pssApi.getIfpaRanking(playerName)
            .subscribe(this.generateGetIfpaRankingProcessor())                    
    }

    getIfpaRankingMobile(playerName,slidingItem){
        slidingItem.close();
        this.getIfpaRanking(playerName);
    }
    
    onChange(event){
        console.log('in onChange...')
        
    }
    
    onInput(event){        
        console.log('in onInput...')
        this.loading=true;
        
    }
    
    onItemsShown(event){
        console.log('onItemsShown...')
        //this.loading=true;
    }

    generateLoadingFunction(){
        return (input)=>{
            console.log('in loading function');
            
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
            setTimeout(()=>{this.loading=false;},500)
            
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
    // onUploadFinished(event){
    //     this.selectedPlayer.has_pic=true;        
    //     console.log(event.serverResponse._body);
    //     this.selectedPlayer.img_file=JSON.parse(event.serverResponse._body).data;        
    // }
    onSubmit(){
        if(this.selectedPlayer.ifpa_ranking=='not ranked'){
            this.selectedPlayer.ifpa_ranking=99999;
        }
        this.pssApi.addEventPlayers({players:[this.selectedPlayer]},this.eventId)
            .subscribe(this.generateAddEventPlayersProcessor())                                                  

    }
    
}
