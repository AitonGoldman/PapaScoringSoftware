import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ResultsMachinePage } from './results-machine';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    ResultsMachinePage,
  ],
  imports: [
      CustomComponentsModule,
      IonicPageModule.forChild(ResultsMachinePage),
  ],
})
export class ResultsMachinePageModule {}
