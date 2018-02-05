import { Component, ViewChild } from '@angular/core';
import { Nav, Platform } from 'ionic-angular';
import { StatusBar } from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';
import { TitleServiceProvider } from '../providers/title-service/title-service';
import { EventAuthProvider } from '../providers/event-auth/event-auth';
import { FCM } from '@ionic-native/fcm';
import { PssApiProvider } from '../providers/pss-api/pss-api';

@Component({
    templateUrl: 'app.html'
})
export class MyApp {
    @ViewChild(Nav) nav: Nav;    
    constructor(platform: Platform, statusBar: StatusBar,
                splashScreen: SplashScreen, public titleService: TitleServiceProvider,
                public eventAuth: EventAuthProvider,public fcm: FCM,
                public pssApi: PssApiProvider) {
        platform.ready().then(() => {
            // Okay, so the platform is ready and our plugins are available.
            // Here you can do any higher level native things you might need.
            statusBar.styleDefault();
            splashScreen.hide();
            if(platform.is('cordova')){
                this.fcm.subscribeToTopic('all');

                this.fcm.onTokenRefresh().subscribe(
                    token =>{
                        this.pssApi.recordTokens(token)                                       
                        // backend.registerToken(token);
                    }
                );
                this.fcm.getToken().then(
                    token =>{
                        this.pssApi.recordTokens(token)                                       
                        // backend.registerToken(token);
                    }
                );
                

                this.fcm.onNotification().subscribe(data => {
                    alert('message received')
                    if(data.wasTapped) {
                        console.info("Received in background");
                    } else {
                        console.info("Received in foreground");
                    };
                });            
            }
        });        
    }
    openPage(page) {
        // Reset the content nav to have just this page
        // we wouldn't want the back button to show in this scenario
        this.nav.setRoot(page);
  }    
}

