import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ScorekeeperMachineSelectPage } from './scorekeeper-machine-select';
import { CustomComponentsModule } from '../../components/custom-components.module';
import { IonicImageLoader } from 'ionic-image-loader';

@NgModule({
  declarations: [
      ScorekeeperMachineSelectPage,
        ],
  imports: [
      IonicPageModule.forChild(ScorekeeperMachineSelectPage),
      CustomComponentsModule,
      IonicImageLoader

  ],
})
export class ScorekeeperMachineSelectPageModule {}
