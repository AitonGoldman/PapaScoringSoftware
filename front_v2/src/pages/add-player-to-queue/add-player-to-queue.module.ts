import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AddPlayerToQueuePage } from './add-player-to-queue';

@NgModule({
  declarations: [
    AddPlayerToQueuePage,
  ],
  imports: [
    IonicPageModule.forChild(AddPlayerToQueuePage),
  ],
})
export class AddPlayerToQueuePageModule {}
