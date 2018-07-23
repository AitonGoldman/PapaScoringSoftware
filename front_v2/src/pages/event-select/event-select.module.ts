import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventSelectPage } from './event-select';
import { IonicImageLoader } from 'ionic-image-loader';

@NgModule({
  declarations: [
    EventSelectPage,
  ],
  imports: [
      IonicPageModule.forChild(EventSelectPage),
      IonicImageLoader
  ],
})
export class EventSelectPageModule {}
