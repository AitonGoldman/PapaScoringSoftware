import { Component } from '@angular/core';
import { Platform, App, NavParams, NavController } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { NotificationsService } from 'angular2-notifications';

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
                public notificationsService: NotificationsService) {
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
        
    getHomePageString(eventId?){
        if(eventId==null){
            eventId=this.eventId;
        }
        let role = this.eventAuth.getRoleName(eventId);
        console.log('in getHomePageString...')
        
        if(role=="tournamentdirector"){
                return 'TournamentDirectorHomePage'            
        }
        if(role=="eventowner"){
                return 'EventOwnerHomePage'            
        }
        if(role=="player"){
            return 'PlayerHomePage'
        }
       if(role=="scorekeeper"){
            return 'ScorekeeperHomePage'
       }
         
        if (role == null){
            return 'HomePage';
        }
        
    }
    pushRootPage(page,params={}) {
        this.appCtrl.getRootNav().push(page, params);
    }
    
    pushPageWithNoBackButton(pageName,navParams,tabIndex?):void{
        console.log('in push page with no back button...');
        if(tabIndex!=null){            
            
            
            this.navCtrl.parent.getByIndex(tabIndex).setRoot(pageName,navParams,{animate:false});
            
            this.navCtrl.parent.select(tabIndex);
            
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
            this.notificationsService.success("Success", message_string,{
                timeOut:0,
                position:["top","right"],
                theClass:'poop'
            })            
        };
        
    }
    
    onTournamentToggle(eventId,tournament){
        tournament.active=tournament.active!=true;
        let stringDescription=tournament.active!=true?"deactivated":"activated"
        this.pssApi.editTournament(tournament,eventId)
            .subscribe(this.generateEditTournamentProcessor(tournament.tournament_name+" has been "+stringDescription))                
    }
}
