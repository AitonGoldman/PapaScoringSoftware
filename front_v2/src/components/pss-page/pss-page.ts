import { Component } from '@angular/core';
import { Platform, App, NavParams, NavController } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { NotificationsService } from 'angular2-notifications';
import { SearchResults } from '../../classes/search-results';
import { ActionSheetController } from 'ionic-angular'
import { ToastController } from 'ionic-angular';
import { ModalController } from 'ionic-angular';
import { AlertController } from 'ionic-angular';
import { PopoverController } from 'ionic-angular';
import { TournamentSettingsProvider } from '../../providers/tournament-settings/tournament-settings'
import { ListOrderStorageProvider } from '../../providers/list-order-storage/list-order-storage'
import { Events } from 'ionic-angular';

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
    eventId:number = null;
    eventName:string = null;
    tournamentId:number = null;
    hideBackButton:boolean = false;
    constructor(public eventAuth: EventAuthProvider,
                public navParams: NavParams,
                public navCtrl: NavController,
                public appCtrl: App,
                public pssApi: PssApiProvider,
                public platform: Platform,                
                //public notificationsService: NotificationsService,
                public toastCtrl: ToastController,
                public actionSheetCtrl: ActionSheetController,
                public modalCtrl: ModalController,
                public alertCtrl: AlertController,
                public popoverCtrl: PopoverController,
                public tournamentSettings: TournamentSettingsProvider,
                public listOrderStorage: ListOrderStorageProvider,
                public eventsService: Events) {
        this.eventId = navParams.get('eventId');
        this.eventName = navParams.get('eventName');
        console.log('Hello PssPageComponent Component');
//        console.log(instance.constructor.name)
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
            return 'Player Home'
        }
       if(role=="scorekeeper"){
            return 'Scorekeeper Home'
       }
         
        if (role == null){
            return 'Home';
        }
        
    }
    
    getHomePageString(eventId?){
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
        if(role=="player"){
            return 'PlayerHomePage'
        }
       if(role=="scorekeeper"){
            return 'ScorekeeperTournamentSelectPage'
       }
         
        if (role == null){
            return 'HomePage';
        }
        
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
    expand(item){
        item.expanded=item.expanded==false?true:false;
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
