import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { FinalsBootstrapResolveTiebreakerPage } from './finals-bootstrap-resolve-tiebreaker';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    FinalsBootstrapResolveTiebreakerPage,
  ],
  imports: [
      IonicPageModule.forChild(FinalsBootstrapResolveTiebreakerPage),
      CustomComponentsModule,      
  ],
})
export class FinalsBootstrapResolveTiebreakerPageModule {}
