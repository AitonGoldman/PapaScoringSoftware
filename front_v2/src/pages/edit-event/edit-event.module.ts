import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EditEventPage } from './edit-event';
import { ImageUploadModule } from "angular2-image-upload";
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    EditEventPage,
  ],
  imports: [
      IonicPageModule.forChild(EditEventPage),      
      ImageUploadModule.forRoot(),
      CustomComponentsModule             
  ],
})
export class EditEventPageModule {}
