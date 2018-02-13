import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { FinalsBootstrapPage } from './finals-bootstrap';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    FinalsBootstrapPage,
  ],
  imports: [
      IonicPageModule.forChild(FinalsBootstrapPage),
      CustomComponentsModule,      
  ],
})
export class FinalsBootstrapPageModule {}
