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
/*
"ios":{
 "num":11.2,
 "major":11
}
*/
export class LoginPage extends PssPageComponent {    
    loginInfo:any = {'username':null,'password':null,'player_id_for_event':null,'player_pin':null}
    loginType:string = 'player';
    generateLoginUserProcessor(successButton?,eventOwnerLogin?){
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
            let targetPageParams = {'successSummary':successSummary,
                                    'successButtons':[successButton]}
            if(eventOwnerLogin!=null){
                targetPageParams['ignoreEventId']=true;
            }
            this.navCtrl.push("SuccessPage",            
                              this.buildNavParams(targetPageParams));
        };
    }    
    loginUser(){
        let versions = this.platform.versions();
        if(versions.ios!=null && versions.ios.major>=11 && !this.platform.is('cordova')){
            // let toast = this.toastCtrl.create({
            //     message: "iOS 11 is not supported through the browser.  Please install the app - a link to the app store is on the home page.",
            //     duration: 99000,
            //     position: 'top',
            //     showCloseButton: true,
            //     closeButtonText: " ",
            //     cssClass: "dangerToast"
            // });
            // toast.present();
            this.pssToast.showToast("iOS 11 is not supported through the browser.  Please install the app - a link to the app store is on the home page.",
                                    99000,
                                    "dangerToast")

            //return
        }
        this.pssApi.loginUser(this.loginInfo,this.eventId)
            .subscribe(this.generateLoginUserProcessor())            
    }
    loginPlayer(){
        let versions = this.platform.versions();
        if(versions.ios!=null && versions.ios.major>=11 && !this.platform.is('cordova')){
            // let toast = this.toastCtrl.create({
            //     message: "iOS 11 is not supported through the browser.  Please install the app - a link to the app store is on the home page.",
            //     duration: 99000,
            //     position: 'top',
            //     showCloseButton: true,
            //     closeButtonText: " ",
            //     cssClass: "dangerToast"
            // });
            // toast.present();
            this.pssToast.showToast("iOS 11 is not supported through the browser.  Please install the app - a link to the app store is on the home page.",
                                    99000,
                                    "dangerToast")

            return
        }

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
            .subscribe(this.generateLoginUserProcessor(successButton,true))            
    }
    
    ionViewWillLoad() {
        console.log('ionViewDidLoad LoginPage');
        //this.eventAuth.setEventRole(1,{'roleName':'deskworker'});      
    }
}
