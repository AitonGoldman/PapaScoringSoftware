import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { HomePage } from './home';
import { CustomHeaderComponent } from '../../components/custom-header/custom-header';

@NgModule({
  declarations: [
      HomePage,
      CustomHeaderComponent
  ],
  imports: [
    IonicPageModule.forChild(HomePage),
  ],
})
export class HomePageModule {}
