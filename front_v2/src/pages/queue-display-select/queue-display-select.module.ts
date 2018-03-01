import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { QueueDisplaySelectPage } from './queue-display-select';

@NgModule({
  declarations: [
    QueueDisplaySelectPage,
  ],
  imports: [
    IonicPageModule.forChild(QueueDisplaySelectPage),
  ],
})
export class QueueDisplaySelectPageModule {}
