import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule } from '@angular/core';
import { IonicApp, IonicErrorHandler, IonicModule } from 'ionic-angular';
import { SplashScreen } from '@ionic-native/splash-screen';
import { StatusBar } from '@ionic-native/status-bar';
import { HttpClientModule }    from '@angular/common/http';

import { MyApp } from './app.component';
import { TitleServiceProvider } from '../providers/title-service/title-service';
import { EventAuthProvider } from '../providers/event-auth/event-auth';
import { PssApiProvider } from '../providers/pss-api/pss-api';
import { FormsModule }   from '@angular/forms';
//import { ComponentsModule } from '../components/components.module'
//import { CustomHeaderComponent } from '../components/custom-header/custom-header';

@NgModule({
  declarations: [
      MyApp//,
      //CustomHeaderComponent
  ],
  imports: [
      BrowserModule,
      IonicModule.forRoot(MyApp),
      HttpClientModule,
      FormsModule//,
      //ComponentsModule
  ],
  bootstrap: [IonicApp],
  entryComponents: [
      MyApp      
  ],
  providers: [
    StatusBar,
    SplashScreen,
    {provide: ErrorHandler, useClass: IonicErrorHandler},
    TitleServiceProvider,
    EventAuthProvider,
    PssApiProvider
  ]
})
export class AppModule {}
