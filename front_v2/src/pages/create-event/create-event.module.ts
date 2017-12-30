import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { CreateEventPage } from './create-event';

@NgModule({
  declarations: [
    CreateEventPage,
  ],
  imports: [
    IonicPageModule.forChild(CreateEventPage),
  ],
})
export class CreateEventPageModule {}
