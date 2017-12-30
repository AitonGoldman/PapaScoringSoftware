import { Component } from '@angular/core';
import { Platform, App, NavParams, NavController } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';

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
                public platform: Platform) {
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
    getHomePageString(){        
        let role = this.eventAuth.getRoleName(this.eventId);
        if(role=="tournamentdirector"){
                return 'TournamentDirectorHomePage'            
        }
        //if(role=="eventowner"){
        //        return 'EventOwnerHomePage'            
        //}        
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
            console.log(tabIndex);
            console.log('in push page with no back button...2');
            this.navCtrl.parent.getByIndex(tabIndex).setRoot(pageName,navParams,{animate:false});
            console.log('in push page with no back button...3');
            this.navCtrl.parent.select(tabIndex);
            console.log('in push page with no back button...4');
            return;
        }
        console.log('page name is ...'+pageName);
        this.navCtrl.getActive().willLeave.subscribe(
            ()=>{
                this.navCtrl.last().showBackButton(false);
            }
        )        
        this.navCtrl.push(pageName,this.buildNavParams(navParams));
    }

}
