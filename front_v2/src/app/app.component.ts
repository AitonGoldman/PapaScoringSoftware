import { Component, ViewChild } from '@angular/core';
import { Nav, Platform } from 'ionic-angular';
import { StatusBar } from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';
import { TitleServiceProvider } from '../providers/title-service/title-service';
import { EventAuthProvider } from '../providers/event-auth/event-auth';
import { FCM } from '@ionic-native/fcm';
import { PssApiProvider } from '../providers/pss-api/pss-api';
import { FcmTokenProvider } from '../providers/fcm-token/fcm-token';
import { ImageLoaderConfig } from 'ionic-image-loader';

@Component({
    templateUrl: 'app.html'
})
export class MyApp {
    @ViewChild(Nav) nav: Nav;    
    constructor(platform: Platform, statusBar: StatusBar,
                splashScreen: SplashScreen, public titleService: TitleServiceProvider,
                public eventAuth: EventAuthProvider,public fcm: FCM,
                public pssApi: PssApiProvider,
                public fcmToken: FcmTokenProvider,
                private imageLoaderConfig: ImageLoaderConfig
               ) {
        platform.ready().then(() => {
            // Okay, so the platform is ready and our plugins are available.
            // Here you can do any higher level native things you might need.
            console.log('------------------')
            console.log('poop 2');
            this.imageLoaderConfig.enableDebugMode();
            statusBar.overlaysWebView(false);
            statusBar.styleDefault();
            splashScreen.hide();
            console.log('-------------')
            console.log('versions is....');            
            if(platform.is('cordova')){
                //this.fcm.subscribeToTopic('all');

                this.fcm.onTokenRefresh().subscribe(                    
                    token =>{
                        console.log('inside onTokenRefresh()');
                        if(token==null){
                            console.log('inside onTokenRefresh() - null token 1');
                            return;
                        }
                        //let sendToken=false;
                        if((fcmToken.getFcmToken()!=null && fcmToken.getFcmToken()!=token)||fcmToken.getFcmToken()==null){
                            console.log('inside onTokenRefresh() - non null token 1');
                            console.log(token)
                            fcmToken.setFcmToken(token);
                            //this.pssApi.recordTokens(token)
                        }                                                
                    }
                );
                this.fcm.getToken().then(                    
                    token =>{
                        console.log('inside getToken()');
                        if(token==null){
                            console.log('inside getToken() null token 2');
                            return;
                        }
                        if((fcmToken.getFcmToken()!=null && fcmToken.getFcmToken()!=token)||fcmToken.getFcmToken()==null){
                            console.log('inside getToken() non null token 2');
                            console.log(token)                            
                            fcmToken.setFcmToken(token);
                            //this.pssApi.recordTokens(token)
                        }                                                
                    }
                );
                

                this.fcm.onNotification().subscribe(data => {
                    
                    alert(data.aps.alert.body)
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

