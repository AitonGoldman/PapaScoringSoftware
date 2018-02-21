import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ResultsPage } from './results';
import { CustomComponentsModule } from '../../components/custom-components.module';
import { IonicImageLoader } from 'ionic-image-loader';

@NgModule({
  declarations: [
    ResultsPage,
  ],
  imports: [
      IonicPageModule.forChild(ResultsPage),
      CustomComponentsModule,
      IonicImageLoader
  ],
})
export class ResultsPageModule {}
