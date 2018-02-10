import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { SuccessSummary } from '../../classes/success-summary';
import { SuccessButton } from '../../classes/SuccessButton';

/**
 * Generated class for the LoginPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'login/:eventId/:eventName'
})
@Component({
    selector: 'page-login',
    templateUrl: 'login.html',
})
export class LoginPage extends PssPageComponent {    
    loginInfo:any = {'username':null,'password':null,'player_id_for_event':null,'player_pin':null}
    loginType:string = 'player';
    generateLoginUserProcessor(successButton?){
        return (result) => {
            if(result == null){
                return;
            }
            console.log('in generateLoginUserProcessor');
            
            this.eventAuth.setEventUserLoggedIn(this.eventId,result.data);
            let name=null;
            if(result.data.full_user_name!=null){
                name=result.data.full_user_name;
            }
            if(result.data.player_full_name!=null){
                name=result.data.player_full_name;
            }
            
            let successSummary = new SuccessSummary(name+' has logged in.',
                                                    null,
                                                    null);
            let targetPage=null;
            let targetTabIndex=null;
            if(this.platform.is('mobile')){
                console.log('going mobile')
                if(this.loginInfo.player_id_for_event==null && this.loginInfo.player_pin==null && this.loginInfo.username!=null){
                    targetTabIndex=0;
                }                
            }            
            if(successButton==null){
                targetPage=this.getHomePageString();
                console.log('targetPage is...')
                console.log(this.buildNavParams({}))
                successButton = new SuccessButton('Go Home',
                                                  targetPage,
                                                  this.buildNavParams({}),
                                                  targetTabIndex);
                
            }
            //            this.appCtrl.getRootNav().push("SuccessPage",
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams({'successSummary':successSummary,
                                                   'successButtons':[successButton]}));
        };
    }    
    loginUser(){
        this.pssApi.loginUser(this.loginInfo,this.eventId)
            .subscribe(this.generateLoginUserProcessor())            
    }
    loginPlayer(){
        if(this.fcmToken.getFcmToken()!=null){
            this.loginInfo.token=this.fcmToken.getFcmToken();
        }
        
        this.pssApi.loginPlayer(this.loginInfo,this.eventId)
            .subscribe(this.generateLoginUserProcessor())            
    }    
    
    loginEventOwner(){
        let targetTabIndex=null;
        if(this.platform.is('mobile')){
            console.log('going mobile')
            targetTabIndex=0;
        }            

        let successButton = new SuccessButton('Go Home',
                                              'EventOwnerHomePage',
                                              this.buildNavParams({}),
                                              targetTabIndex);

        this.pssApi.loginEventOwner(this.loginInfo)
            .subscribe(this.generateLoginUserProcessor(successButton))            
    }
    
    ionViewWillLoad() {
        console.log('ionViewDidLoad LoginPage');
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

        //this.eventAuth.setEventRole(1,{'roleName':'deskworker'});      
    }
}
