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
    segment:'login/:eventId'
})
@Component({
    selector: 'page-login',
    templateUrl: 'login.html',
})
export class LoginPage extends PssPageComponent {    
    loginInfo:any = {'username':null,'password':null}

    generateLoginUserProcessor(successButton?){
        return (result) => {
            if(result == null){
                return;
            }
            this.eventAuth.setEventUserLoggedIn(this.eventId,result.data);
            let successSummary = new SuccessSummary(result.data.username+' has logged in.',
                                                    null,
                                                    null);
            let targetPage=null;
            let targetTabIndex=null;
            if(this.platform.is('mobile')){
                console.log('going mobile')
                targetTabIndex=0;
            }            
            if(successButton==null){
                targetPage=this.getHomePageString();
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
        //this.eventAuth.setEventRole(1,{'roleName':'deskworker'});      
    }
}
