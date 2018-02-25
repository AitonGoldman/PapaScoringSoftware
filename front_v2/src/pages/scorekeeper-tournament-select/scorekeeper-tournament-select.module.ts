import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ScorekeeperTournamentSelectPage } from './scorekeeper-tournament-select';
import { CustomComponentsModule } from '../../components/custom-components.module';
import { IonicImageLoader } from 'ionic-image-loader';

@NgModule({
  declarations: [
    ScorekeeperTournamentSelectPage,
  ],
  imports: [
      IonicPageModule.forChild(ScorekeeperTournamentSelectPage),
      CustomComponentsModule,
      IonicImageLoader
  ],
})
export class ScorekeeperTournamentSelectPageModule {}
