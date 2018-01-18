import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { PlayerInfoPage } from './player-info';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { CustomComponentsModule } from '../../components/custom-components.module';

//import { SimpleNotificationsModule } from 'angular2-notifications';
//import { ToastModule } from 'ng2-toastr/ng2-toastr';

@NgModule({
  declarations: [
    PlayerInfoPage,
  ],
  imports: [
      IonicPageModule.forChild(PlayerInfoPage),
      AutoCompleteModule,      
      CustomComponentsModule             
  //    ToastModule.forRoot(),
  //    SimpleNotificationsModule.forRoot(),
  ],
})
export class PlayerInfoPageModule {}
