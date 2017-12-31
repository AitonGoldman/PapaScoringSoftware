import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventOwnerConfirmPage } from './event-owner-confirm';

@NgModule({
  declarations: [
    EventOwnerConfirmPage,
  ],
  imports: [
    IonicPageModule.forChild(EventOwnerConfirmPage),
  ],
})
export class EventOwnerConfirmPageModule {}
