import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventOwnerLoginPage } from './event-owner-login';

@NgModule({
  declarations: [
    EventOwnerLoginPage,
  ],
  imports: [
    IonicPageModule.forChild(EventOwnerLoginPage),
  ],
})
export class EventOwnerLoginPageModule {}
