import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { HomePage } from './home';
import { CustomComponentsModule } from '../../components/custom-components.module';


@NgModule({
  declarations: [
      HomePage     
  ],
  imports: [
    IonicPageModule.forChild(HomePage),
      CustomComponentsModule,
  ],
})
export class HomePageModule {}
