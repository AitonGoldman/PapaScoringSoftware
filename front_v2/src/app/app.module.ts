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
import { ImageUploadModule } from "angular2-image-upload";
import { CookieModule } from 'ngx-cookie';
import { CustomComponentsModule } from '../components/custom-components.module';
import { TakePicComponent } from '../components/take-pic/take-pic'
import { TopThreePopoverComponent } from '../components/top-three-popover/top-three-popover'
import { ListOrderStorageProvider } from '../providers/list-order-storage/list-order-storage';
import { QuickLinksProvider } from '../providers/quick-links/quick-links';
import { TournamentSettingsProvider } from '../providers/tournament-settings/tournament-settings';
import { FCM } from '@ionic-native/fcm';
import { FcmTokenProvider } from '../providers/fcm-token/fcm-token';

//import {ToastModule} from 'ng2-toastr/ng2-toastr';

@NgModule({
  declarations: [
      MyApp,
      TakePicComponent,
      TopThreePopoverComponent
  ],
  imports: [
      BrowserModule,
      IonicModule.forRoot(MyApp,{
          backButtonText: '',
      }),
      HttpClientModule,
      FormsModule,
      AutoCompleteModule,
      ExpandableModule,
      BrowserAnimationsModule, 
      SimpleNotificationsModule.forRoot(),
      ImageUploadModule.forRoot(),
      CookieModule.forRoot(),
      CustomComponentsModule,
  //    ToastModule.forRoot(),
  ],
  bootstrap: [IonicApp],
  entryComponents: [
      MyApp,
      TakePicComponent,
      TopThreePopoverComponent
  ],
  providers: [
    StatusBar,
    SplashScreen,
    {provide: ErrorHandler, useClass: IonicErrorHandler},
    TitleServiceProvider,
    EventAuthProvider,
    PssApiProvider,
    AutoCompleteProvider,
    ListOrderStorageProvider,
    QuickLinksProvider,
      TournamentSettingsProvider,
      FCM,
    FcmTokenProvider
  ]
})
export class AppModule {}
