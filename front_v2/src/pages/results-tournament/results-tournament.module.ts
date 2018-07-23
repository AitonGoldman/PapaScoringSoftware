import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ResultsTournamentPage } from './results-tournament';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    ResultsTournamentPage,
  ],
  imports: [
      CustomComponentsModule,
      IonicPageModule.forChild(ResultsTournamentPage),
  ],
})
export class ResultsTournamentPageModule {}
