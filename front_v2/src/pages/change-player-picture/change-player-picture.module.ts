import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ChangePlayerPicturePage } from './change-player-picture';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    ChangePlayerPicturePage,
  ],
  imports: [
      IonicPageModule.forChild(ChangePlayerPicturePage),
      CustomComponentsModule
  ],
})
export class ChangePlayerPicturePageModule {}
