import { ViewChild, Component } from '@angular/core';
import { Platform, App, NavParams, NavController, Content } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { SearchResults } from '../../classes/search-results';
import { ActionSheetController } from 'ionic-angular'
//import { ToastController } from 'ionic-angular';
import { ModalController } from 'ionic-angular';
import { AlertController } from 'ionic-angular';
import { PopoverController } from 'ionic-angular';
import { TournamentSettingsProvider } from '../../providers/tournament-settings/tournament-settings'
import { ListOrderStorageProvider } from '../../providers/list-order-storage/list-order-storage'
import { Events } from 'ionic-angular';
import { FcmTokenProvider } from '../../providers/fcm-token/fcm-token';
import { PssToastProvider } from '../../providers/pss-toast/pss-toast';
import { ImageLoader } from 'ionic-image-loader';

import { LoadingController } from 'ionic-angular';


/**
 * Generated class for the TopNavComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
@Component({
    selector: 'pss-page',
    templateUrl: 'pss-page.html'
})
export class PssPageComponent {
    @ViewChild(Content) content: Content;
    eventId:number = null;
    eventName:string = null;
    tournamentId:number = null;
    hideBackButton:boolean = false;
    imgBaseUrl:string="";
    contentWidth:string='100%'
    loadingMessage:string='initialMessage'
    loadingInstance:any=null;
    cssColors:string=null;
    kioskModeEnabled: boolean = false;
    constructor(public eventAuth: EventAuthProvider,
                public navParams: NavParams,
                public navCtrl: NavController,
                public appCtrl: App,
                public pssApi: PssApiProvider,
                public platform: Platform,                
                //public notificationsService: NotificationsService,
                //public toastCtrl: ToastController,
                public pssToast: PssToastProvider,
                public actionSheetCtrl: ActionSheetController,
                public modalCtrl: ModalController,
                public alertCtrl: AlertController,
                public popoverCtrl: PopoverController,
                public tournamentSettings: TournamentSettingsProvider,
                public listOrderStorage: ListOrderStorageProvider,
                public eventsService: Events,
                public fcmToken: FcmTokenProvider,
                public imageLoader: ImageLoader,
                public loadingCtrl: LoadingController) {
        this.eventId = navParams.get('eventId');
        this.eventName = navParams.get('eventName');
        if(!platform.is('mobile')){
            this.contentWidth="50%"
        }
        if(platform.is('tablet')){
            this.contentWidth="75%"
        }
        this.imgBaseUrl=pssApi.getBackendHostUrl();
        console.log('Hello PssPageComponent Component');
        this.kioskModeEnabled=tournamentSettings.getKioskMode()
        
//        console.log(instance.constructor.name)
    }
    showLoading(message){
        // setTimeout(()=>{
        //     console.log('pooping')
        //     this.loadingMessage='poop';
        //     this.testLoader.data.content="poop";
        // },5000)
        this.loadingInstance = this.loadingCtrl.create({
            content: message
        });
        this.loadingInstance.present();        
    }
    updateLoadingMessage(message){
        if(this.loadingInstance!=null&&this.loadingInstance.data!=null){
            this.loadingInstance.data.content=message;
        }
        
    }
    hideLoading(){        
        if(this.loadingInstance!=null&&this.loadingInstance.data!=null){
            this.loadingInstance.dismiss();
        }            
    }
    loadPlayerPicsCache(event_players,loadMessage=false,clearCache=false){
        if(loadMessage==true){
            this.showLoading("Loading Player Images....")
        }
        
        if(clearCache==true){
            this.imageLoader.clearCache();
        }
        
        event_players.forEach((eventPlayer,index)=>{
            this.imageLoader.preload(this.pssApi.getBackendHostUrl()+eventPlayer.img_url).then((data)=>{                        
                console.log('loading image '+index)
                this.updateLoadingMessage('Loading Images '+index)
                if(index==event_players.length-1){
                    setTimeout(()=>{
                        this.hideLoading()
                    },1000)
                }
            }).catch((error)=>{
                if(index==event_players.length-1){
                    setTimeout(()=>{
                        this.hideLoading()
                    },1000)
                }
            });
        })
    }
    buildNavParams(params){
        if(this.eventId!=null&&this.eventId!=undefined){            
            params['eventId'] = this.eventId;
            params['eventName'] = this.eventName;            
        }        
        return params;
    }

    getHomePageDisplayString(eventId?){
        if(eventId==null){
            eventId=this.eventId;
        }
        let role = this.eventAuth.getRoleName(eventId);
        //console.log('in getHomePageString...')
        
        if(role=="tournament_director"){
                return 'TD Home'            
        }
        if(role=="eventowner"){
                return 'Event Owner Home'            
        }
        if(role=="player"){
            return 'Help'
        }
       if(role=="scorekeeper"){
            return 'Scorekeeper Home'
       }
       if(role=="scorekeeper"){
            return 'Deskworker Home'
       }
         
        if (role == null){
            return 'Home';
        }
        
    }
    
    getHomePageString(eventId?,fromTab?){
        if(eventId==null){
            eventId=this.eventId;
        }
        let role = this.eventAuth.getRoleName(eventId);
        //console.log('in getHomePageString...')
        
        if(role=="tournament_director"){
                return 'TournamentDirectorHomePage'            
        }
        if(role=="eventowner"){
                return 'EventOwnerHomePage'            
        }
        if(role=="player" && fromTab==null){
            if(this.platform.is("mobile")){
                return 'QuickLinksPage'
            } else {
                return 'HomePage'
            }
            
        }
        if(role=="player" && fromTab!=null){
            return 'HomePage'
        }        
       if(role=="scorekeeper"){
            return 'ScorekeeperTournamentSelectPage'
       }
        if(role=="deskworker"){            
            return 'DeskworkerHomePage'
       }
         
        if (role == null){
            return 'HomePage';
        }
        
    }
    gotoParentTab(){
        console.log(this.navCtrl.parent.parent.pop())
    }    
    pushRootPage(page,params={}) {        
        this.appCtrl.getRootNav().push(page, params);
    }
    returnToEventSelect(){
        this.appCtrl.getRootNav().popToRoot({});
    }
    pushPageWithNoBackButton(pageName,navParams,tabIndex?):void{
        console.log('in push page with no back button...');
        if(tabIndex!=null){            
                       
            // this.navCtrl.parent.getByIndex(tabIndex).setRoot(pageName,navParams,{animate:false});
            // let currentTab = this.navCtrl.parent.getSelected();
            // this.navCtrl.parent.select(tabIndex).then(()=>{
            //     currentTab.popToRoot({animate:false});
            // });

            //this.navCtrl.parent.getByIndex(tabIndex).popToRoot({}).then(()=>{
                let currentTab = this.navCtrl.parent.getSelected();
                this.navCtrl.parent.select(tabIndex).then(()=>{
                    this.navCtrl.parent.getByIndex(tabIndex).push(pageName,this.buildNavParams(navParams)).then((data)=>{
                        this.navCtrl.parent.getByIndex(tabIndex).last().showBackButton(false);
                        let viewsLength = this.navCtrl.parent.getByIndex(tabIndex).getViews().length
                        if(viewsLength>1){
                            this.navCtrl.parent.getByIndex(tabIndex).remove(0,viewsLength-1);
                        }
                        currentTab.popToRoot({animate:false});
                    })                    
                });
            
            //});
            
            return;
        }
        
        this.navCtrl.getActive().willLeave.subscribe(
            ()=>{
                this.navCtrl.last().showBackButton(false);
            }
        )        
        this.navCtrl.push(pageName,this.buildNavParams(navParams));
    }

    scrollTo(elementId:string) {
        let yOffset = document.getElementById(elementId).offsetTop;
        console.log('yoffset is '+yOffset)
        this.content.scrollTo(0, yOffset, 500)
    }

    expand(item,elementId?){
        item.expanded=item.expanded==false?true:false;
        //if(elementId!=null){
        //    this.scrollTo(elementId);
        //}
    }
    generateEditTournamentProcessor(message_string){
        return (result) => {            
            if(result == null){
                return;
            }
        };
        
    }
    
    onTournamentToggle(eventId,tournament){
        tournament.active=tournament.active!=true;
        let stringDescription=tournament.active!=true?"deactivated":"activated"
        this.pssApi.editTournament(tournament,eventId)
            .subscribe(this.generateEditTournamentProcessor(tournament.tournament_name+" has been "+stringDescription))                
    }

    // auto complete stuff
    generateAutoCompleteGetEventPlayerProcessor(){
        return (result)=>{
            if(result==null){                
                return
            }
            //this['selectedPlayer']=result.data.data;
            this['selectedPlayer']=result.data;
            
            //this['ticketCounts']=this.generateListFromObj(this['selectedPlayer'].tournament_counts);
            console.log('selectedplayer thing...');
            console.log(this['selectedPlayer']);
            this['ticketCounts']=this.generateListFromObj(result.data.tournament_counts);
            //this['ticketCounts']=[]
            //this['ticketCountsDict']=this['selectedPlayer'].tournament_counts;
            this['ticketCountsDict']=result.data.tournament_counts;

            if (result.tournament_calculated_lists!=null){
                this['ticketPriceLists']=result.tournament_calculated_lists;
            }
            this['results']=result.data.values
            console.log('multi match......');
            console.log(this['results']);
        }
    }
    onAutoCompletePlayerSelected(){        
        //this.pssApi.getEventPlayer(this.eventId,this['selectedPlayer'].player_id_for_event)
        this.pssApi.getEventPlayerResultsHidden(this.eventId,this['selectedPlayer'].player_id_for_event)
            .subscribe(this.generateAutoCompleteGetEventPlayerProcessor())
    }
    generatePlayerLoadingFunction(){
        return (searchResults:SearchResults)=>{                        
            if(searchResults.typeOfSearch=="single"){                
                this['selectedPlayer']=searchResults.individualResult.data;                
                this['ticketCounts']=this.generateListFromObj(this['selectedPlayer'].tournament_counts);
            }
            
            setTimeout(()=>{this['loading']=false;},500)            
        }
    }
    generateItemsLoadingFunction(){
        return (input?)=>{            
            setTimeout(()=>{this['loading']=false;},500)            
        }
    }
    
    generateListFromObj(obj){
        if(obj==null){
            return []
        }
        return Object.keys(obj).map(function(key){
            let objValue =obj[key];
            // do something with person
            return objValue
        });
    }
    onAutocompleteInput(event){        
        console.log('in oninput...')
        if(this['searchbar'].suggestions.length==0){            
            this['displayExistingUserNotFound']=true;
            //this.newUserName=event;
        } else {
            this['displayExistingUserNotFound']=false;
        }
        
    }
    nth(d) {
        if(d>3 && d<21) return 'th'; // thanks kennebec
        switch (d % 10) {
        case 1:  return "st";
        case 2:  return "nd";
        case 3:  return "rd";
        default: return "th";
        }
    }     

}
