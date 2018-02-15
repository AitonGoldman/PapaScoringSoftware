import { ViewChild, Component } from '@angular/core';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { AutoCompleteProvider } from '../../providers/auto-complete/auto-complete';
import { ModalController, Platform, App, NavParams, NavController } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { AlertController } from 'ionic-angular';
import { ToastController } from 'ionic-angular';
import { Events } from 'ionic-angular';
import { ActionSheetController } from 'ionic-angular'
import { PopoverController } from 'ionic-angular';
import { TournamentSettingsProvider } from '../../providers/tournament-settings/tournament-settings'
import { ListOrderStorageProvider } from '../../providers/list-order-storage/list-order-storage'
import { FcmTokenProvider } from '../../providers/fcm-token/fcm-token';
import { PssToastProvider } from '../../providers/pss-toast/pss-toast';

//import { IonicPage } from 'ionic-angular';

/**
 * Generated class for the AutoCompleteComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
@Component({
  selector: 'auto-complete',
  templateUrl: 'auto-complete.html'
})
export class AutoCompleteComponent extends PssPageComponent {

    text: string;
    autocompleteDoneEventHandler:any=null;
    autocompleteSkipEventHandler:any=null;
    ticketCounts:any=null;
    ticketCountsDict:any=null;
    ticketPriceLists:any=null;
    notFoundMessage:string=null;
    selectedPlayer:any=null;    
    @ViewChild('searchbar')  searchbar: any;    
    loading:boolean=false;    
    potentialPlayer:any={};
    addPlayerAutoComplete:boolean=false;
    results:any=null;
    
    constructor(public autoCompleteProvider:AutoCompleteProvider,
                public eventAuth: EventAuthProvider,
                public navParams: NavParams,
                public navCtrl: NavController,
                public appCtrl: App,
                public pssApi: PssApiProvider,
                public platform: Platform,                
                public actionSheetCtrl: ActionSheetController,                
                //public notificationsService: NotificationsService,
                public alertCtrl: AlertController,
                public modalCtrl: ModalController,
                //public toastCtrl: ToastController,
                public pssToast: PssToastProvider,
                public events: Events,
                public popoverCtrl: PopoverController,
                public tournamentSettings: TournamentSettingsProvider,
                public listOrderStorage: ListOrderStorageProvider,
                public fcmToken: FcmTokenProvider){
        super(eventAuth,navParams,
              navCtrl,appCtrl,
              pssApi,platform,
              //notificationsService,
              //toastCtrl,
              pssToast,
              actionSheetCtrl,
              modalCtrl,
              alertCtrl,
              popoverCtrl,
              tournamentSettings,
              listOrderStorage,
              events,
              fcmToken);
        this.autocompleteDoneEventHandler= (autocompleteInfo, time) => {
            // user and time are the same arguments passed in `events.publish(user, time)`
            this.loading=false;            
            if(autocompleteInfo.state=='DONE'){                
                if(autocompleteInfo.type=='SEARCH_SINGLE'){                    
                    
                    //this.selectedPlayer=autocompleteInfo.data.data.data;
                    this.selectedPlayer=autocompleteInfo.data.data;
                    console.log('found single player...');
                    console.log(this.selectedPlayer);
                    //this.ticketCounts=this.generateListFromObj(this.selectedPlayer.tournament_counts);
                    this.ticketCounts=this.generateListFromObj(this.selectedPlayer.tournament_counts);
                    //this.ticketCountsDict=this.selectedPlayer.tournament_counts;
                    this.ticketCountsDict=this.selectedPlayer.tournament_counts;
                    //if (this.selectedPlayer.tournament_calculated_lists!=null){
                    //    this.ticketPriceLists=this.selectedPlayer.tournament_calculated_lists;
                    //}
                    if (this.selectedPlayer.tournament_calculated_lists!=null){
                       this.ticketPriceLists=this.selectedPlayer.tournament_calculated_lists;
                    }
                    
                    console.log('single match...');
                    this.results=this.selectedPlayer.values;
                    console.log(this.selectedPlayer);
                    
                    
                }                
            }
            if(autocompleteInfo.state=='NONE'){
                console.log(autocompleteInfo);
                console.log(this.searchbar);
                this.notFoundMessage = "Player not found";
                if(this.addPlayerAutoComplete==false){
                    return;
                }
                if(this.selectedPlayer==null){
                    this.selectedPlayer={player_full_name:this.searchbar.keyword};
                }
                let nameElements=this.searchbar.keyword.split(' ');
                if(nameElements.length>0){
                    this.selectedPlayer.first_name=nameElements[0];
                }
                if(nameElements.length>1){
                    this.selectedPlayer.last_name=nameElements[1];
                }                
                
                //this.selectedPlayer = null;
            }                        
        }        
        this.events.subscribe('autocomplete:done', this.autocompleteDoneEventHandler);                
    }
    onKeyUp(event){        
        this.notFoundMessage=null        
        if(this.searchbar.keyword.length>2){
            this.loading=true;
        } else {
            this.loading=false;
        }
        if(this.searchbar.keyword.length==0){
            this.selectedPlayer=null;
        }        
    }
    ionViewWillLeave() {
        this.events.unsubscribe('autocomplete:done', this.autocompleteDoneEventHandler)                                 
    }
//    ionViewWillLoad() {
//    }
    
    
}
