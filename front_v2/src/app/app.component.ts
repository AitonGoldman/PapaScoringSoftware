import { Component } from '@angular/core';
import { Platform } from 'ionic-angular';
import { StatusBar } from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';
import { TitleServiceProvider } from '../providers/title-service/title-service';
import { EventAuthProvider } from '../providers/event-auth/event-auth';

@Component({
    templateUrl: 'app.html'
})
export class MyApp {   
    constructor(platform: Platform, statusBar: StatusBar,
                splashScreen: SplashScreen, public titleService: TitleServiceProvider,
                public eventAuth: EventAuthProvider) {
        platform.ready().then(() => {
            // Okay, so the platform is ready and our plugins are available.
            // Here you can do any higher level native things you might need.
            statusBar.styleDefault();
            splashScreen.hide();            
        });
    }
}

