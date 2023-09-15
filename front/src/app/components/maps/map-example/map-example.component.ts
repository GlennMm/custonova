import { Component, OnInit } from "@angular/core";
import { FormBuilder } from "@angular/forms";
import { MatSnackBar } from "@angular/material/snack-bar";
import { HttpService } from "src/app/services/http.service";

declare const google: any;

@Component({
  selector: "app-map-example",
  templateUrl: "./map-example.component.html",
})
export class MapExampleComponent implements OnInit {
  
  file: File = null
  test_file: File = null

  loading = false
  test_loading = false

  train_result = null
  test_result = null

  
  constructor(private http: HttpService, private fb: FormBuilder, private snackbar: MatSnackBar) {}

  ngOnInit(): void {}
  
  selectFile(event: any) {
    this.file = event.target.files[0]
  }

  selectTestFile(event: any) {
    this.test_file = event.target.files[0]
  }

  uploadDataset() {
    this.loading = true
    const form = new FormData();
    form.append('dataset',this.file)
    this.http.train_logostic(form).subscribe(
      (data) => {
        console.log('Perfomance', data)
        this.train_result = data
      },
      (err) => {
        console.log(err)
        this.loading = false
        this.snackbar.open(err.message, null, { duration: 5000 })
      },
      () => this.loading = false
    )
  }

  uploadTestDataset() {
    this.test_loading = true
    const form = new FormData();
    form.append('dataset',this.file)
    this.http.test_logositic(form).subscribe(
      (data) => {
        console.log('Perfomance', data)
        this.test_result = data
      },
      (err) => {
        console.log(err)
        this.test_loading = false
        this.snackbar.open(err.message, null, { duration: 5000 })
      },
      () => this.test_loading = false
    )
  }

}
