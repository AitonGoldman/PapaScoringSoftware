import { Component } from '@angular/core';
import { App, IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { SuccessSummary } from '../../classes/success-summary';

/**
 * Generated class for the LoginPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-login',
  templateUrl: 'login.html',
})
export class LoginPage extends PssPageComponent {    
    loginInfo:any = {'username':null,'password':null}
    constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public appCtrl: App,
              public eventAuth: EventAuthProvider,
              public pssApi: PssApiProvider) {
      super(eventAuth,navParams);
      console.log('in login, event id is ... '+this.eventId);
  }

    generateLoginUserProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            console.log('got data back from loginUser...');
            console.log(result);
            let successSummary = new SuccessSummary(result.data.username+' has logged in',
                                                    null,
                                                    null);
            this.appCtrl.getRootNav().push("SuccessPage",
                                           this.buildNavParams({'successSummary':successSummary}));
        };
    }
    loginUser(){
        this.pssApi.loginUser(this.eventId,this.loginInfo)
            .subscribe(this.generateLoginUserProcessor())    
    }
  ionViewDidLoad() {
    console.log('ionViewDidLoad LoginPage');
    this.eventAuth.setEventRole(1,{'roleName':'deskworker'});      
  }
}
