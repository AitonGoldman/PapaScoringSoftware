import { NgModule } from '@angular/core';
import { PssPageComponent } from './pss-page/pss-page';
import { CustomHeaderComponent } from './custom-header/custom-header';
import { CreateEditEntityComponent } from './create-edit-entity/create-edit-entity';
import { EventComponent } from './event/event';
import { TournamentComponent } from './tournament/tournament';
import { ExpandableComponent } from './expandable/expandable';
import { TakePicComponent } from './take-pic/take-pic';
import { AutoCompleteComponent } from './auto-complete/auto-complete';
@NgModule({
	declarations: [
            PssPageComponent,    
            CustomHeaderComponent,
            CreateEditEntityComponent,
            EventComponent,
            TournamentComponent,            
            ExpandableComponent,
            TakePicComponent,        
    TakePicComponent,
    AutoCompleteComponent],
    imports: [],
    exports: [
        PssPageComponent,
        CustomHeaderComponent,
        CreateEditEntityComponent,
        EventComponent,
        TournamentComponent,        
        ExpandableComponent,                
        TakePicComponent,
    AutoCompleteComponent]
})
export class ComponentsModule {}
