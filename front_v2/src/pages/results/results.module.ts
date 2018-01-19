import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ResultsPage } from './results';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    ResultsPage,
  ],
  imports: [
      IonicPageModule.forChild(ResultsPage),
      CustomComponentsModule,      
  ],
})
export class ResultsPageModule {}
