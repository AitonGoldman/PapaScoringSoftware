import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AddPlayerPage } from './add-player';
import { CustomComponentsModule } from '../../components/custom-components.module';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { ImageUploadModule } from "angular2-image-upload";

@NgModule({
  declarations: [
    AddPlayerPage,
  ],
  imports: [
      IonicPageModule.forChild(AddPlayerPage),
      CustomComponentsModule,
      AutoCompleteModule,
      ImageUploadModule.forRoot()
  ],
})
export class AddPlayerPageModule {}
