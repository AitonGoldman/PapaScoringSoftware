import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventSelectPage } from './event-select';

@NgModule({
  declarations: [
    EventSelectPage,
  ],
  imports: [
    IonicPageModule.forChild(EventSelectPage),
  ],
})
export class EventSelectPageModule {}
