import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { PlayerHomePage } from './player-home';

@NgModule({
  declarations: [
    PlayerHomePage,
  ],
  imports: [
    IonicPageModule.forChild(PlayerHomePage),
  ],
})
export class PlayerHomePageModule {}
