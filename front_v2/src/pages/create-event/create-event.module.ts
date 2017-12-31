import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { CreateEventPage } from './create-event';
import { ImageUploadModule } from "angular2-image-upload";

@NgModule({
  declarations: [
    CreateEventPage,
  ],
  imports: [
      IonicPageModule.forChild(CreateEventPage),
      ImageUploadModule.forRoot()
  ],
})
export class CreateEventPageModule {}
