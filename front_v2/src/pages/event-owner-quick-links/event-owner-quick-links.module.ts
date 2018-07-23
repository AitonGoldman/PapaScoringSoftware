import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventOwnerQuickLinksPage } from './event-owner-quick-links';

@NgModule({
  declarations: [
    EventOwnerQuickLinksPage,
  ],
  imports: [
    IonicPageModule.forChild(EventOwnerQuickLinksPage),
  ],
})
export class EventOwnerQuickLinksPageModule {}
