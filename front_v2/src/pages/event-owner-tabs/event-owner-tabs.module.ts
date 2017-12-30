import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventOwnerTabsPage } from './event-owner-tabs';

@NgModule({
  declarations: [
    EventOwnerTabsPage,
  ],
  imports: [
    IonicPageModule.forChild(EventOwnerTabsPage),
  ],
})
export class EventOwnerTabsPageModule {}
