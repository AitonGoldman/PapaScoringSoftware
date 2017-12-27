export class SuccessSummary  {    
    //title:string = null;
    //firstLine:string = null;
    //secondLine:string = null;
    constructor(public title:string,
                public firstLine:string,
                public secondLine:string) {
    }
    getTitle():string {
        return this.title;
    }
    getFirstLine():string {
        return this.firstLine;
    }
    getSecondLine():string {
        return this.secondLine;
    }    
}
