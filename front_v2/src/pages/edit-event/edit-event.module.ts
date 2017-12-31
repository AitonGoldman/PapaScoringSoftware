import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EditEventPage } from './edit-event';
import { ImageUploadModule } from "angular2-image-upload";
@NgModule({
  declarations: [
    EditEventPage,
  ],
  imports: [
      IonicPageModule.forChild(EditEventPage),      
      ImageUploadModule.forRoot()
  ],
})
export class EditEventPageModule {}
