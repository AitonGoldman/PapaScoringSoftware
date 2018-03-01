import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { QueueDisplayPage } from './queue-display';

@NgModule({
  declarations: [
    QueueDisplayPage,
  ],
  imports: [
    IonicPageModule.forChild(QueueDisplayPage),
  ],
})
export class QueueDisplayPageModule {}
