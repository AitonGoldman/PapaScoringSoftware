import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AddPlayerToQueuePage } from './add-player-to-queue';
import { AutoCompleteModule } from 'ionic2-auto-complete';

@NgModule({
  declarations: [
    AddPlayerToQueuePage,
  ],
  imports: [
      AutoCompleteModule,
      IonicPageModule.forChild(AddPlayerToQueuePage),
  ],
})
export class AddPlayerToQueuePageModule {}
