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
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { AutoCompleteProvider } from '../providers/auto-complete/auto-complete';
import { ExpandableModule } from '../components/expandable/expandable.module'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { SimpleNotificationsModule } from 'angular2-notifications';

@NgModule({
  declarations: [
      MyApp      
  ],
  imports: [
      BrowserModule,
      IonicModule.forRoot(MyApp),
      HttpClientModule,
      FormsModule,
      AutoCompleteModule,
      ExpandableModule,
      BrowserAnimationsModule, 
      SimpleNotificationsModule.forRoot()
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
    PssApiProvider,
    AutoCompleteProvider
  ]
})
export class AppModule {}
