import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventOwnerRequestPage } from './event-owner-request';

@NgModule({
  declarations: [
    EventOwnerRequestPage,
  ],
  imports: [
    IonicPageModule.forChild(EventOwnerRequestPage),
  ],
})
export class EventOwnerRequestPageModule {}
