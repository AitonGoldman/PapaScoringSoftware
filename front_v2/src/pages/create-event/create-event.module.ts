import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { CreateEventPage } from './create-event';
import { ImageUploadModule } from "angular2-image-upload";
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    CreateEventPage,
  ],
  imports: [
      IonicPageModule.forChild(CreateEventPage),
      ImageUploadModule.forRoot(),
      CustomComponentsModule
  ],
})
export class CreateEventPageModule {}
