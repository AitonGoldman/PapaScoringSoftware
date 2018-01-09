import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { PlayerHomePage } from './player-home';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    PlayerHomePage,
  ],
  imports: [
      IonicPageModule.forChild(PlayerHomePage),
      CustomComponentsModule,
  ],
})
export class PlayerHomePageModule {}
