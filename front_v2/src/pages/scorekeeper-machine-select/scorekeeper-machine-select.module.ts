import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ScorekeeperMachineSelectPage } from './scorekeeper-machine-select';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
      ScorekeeperMachineSelectPage,
        ],
  imports: [
      IonicPageModule.forChild(ScorekeeperMachineSelectPage),
      CustomComponentsModule
  ],
})
export class ScorekeeperMachineSelectPageModule {}
