import { NgModule } from '@angular/core';
import { PssPageComponent } from './pss-page/pss-page';
import { CustomHeaderComponent } from './custom-header/custom-header';
import { CreateEditEntityComponent } from './create-edit-entity/create-edit-entity';
import { EventComponent } from './event/event';
import { TournamentComponent } from './tournament/tournament';
import { TournamentMachinesComponent } from './tournament-machines/tournament-machines';
@NgModule({
	declarations: [
    PssPageComponent,    
    CustomHeaderComponent,
    CreateEditEntityComponent,
    EventComponent,
    TournamentComponent,
    TournamentMachinesComponent],
	imports: [],
	exports: [
    PssPageComponent,
    CustomHeaderComponent,
    CreateEditEntityComponent,
    EventComponent,
    TournamentComponent,
    TournamentMachinesComponent]
})
export class ComponentsModule {}
