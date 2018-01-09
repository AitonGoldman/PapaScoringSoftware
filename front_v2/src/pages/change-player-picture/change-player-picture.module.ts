import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ChangePlayerPicturePage } from './change-player-picture';

@NgModule({
  declarations: [
    ChangePlayerPicturePage,
  ],
  imports: [
    IonicPageModule.forChild(ChangePlayerPicturePage),
  ],
})
export class ChangePlayerPicturePageModule {}
