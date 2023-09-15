import { Component, OnInit } from "@angular/core";
import { MatSnackBar } from "@angular/material/snack-bar";
import { HistoryService } from "src/app/services/history.service";

@Component({
    templateUrl: 'history.component.html'
})
export class HistoryComponent implements OnInit {
    constructor(private histSer: HistoryService, private snackbar: MatSnackBar) {}

    clustering_imgs: AppImage[] = []
    logistic_imgs: AppImage[] = []
    loading = false

    ngOnInit() {
        this.loading = true
        this.histSer.get_clustering_history().subscribe(
            (data: any) => {
                this.clustering_imgs = data
                this.loading = false
            },
            (err) => {
                console.log(err)
                this.loading = false
                return this.snackbar.open(`${err.error.message}`, null, { duration: 5000 })
            },
            () => this.loading = false
        )
        this.loading = true
        this.histSer.get_logistic_history().subscribe(
            (data: any) => {
                this.logistic_imgs = data
                this.loading = false
            },
            (err) => {
                console.log(err)
                this.loading = false
                return this.snackbar.open(`${err.error.message}`, null, { duration: 5000 })
            },
            () => this.loading = false
        )
    }

    async download(image: AppImage) {
        const base64Response = await fetch(`data:image/png;base64,${image.image}`);
        const blob = await base64Response.blob()
        const anchor = window.document.createElement('a');
        anchor.href = window.URL.createObjectURL(blob);
        anchor.download = `${image.title}.png`;
        document.body.appendChild(anchor);
        anchor.click();
        document.body.removeChild(anchor);
        window.URL.revokeObjectURL(anchor.href);
    }

}

export interface AppImage {
    id?: number
    title: string
    image: string
    date?: Date
    createdBy?: any
}