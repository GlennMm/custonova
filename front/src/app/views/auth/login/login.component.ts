import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormControl, FormGroup, Validators } from "@angular/forms";
import { MatSnackBar, MatSnackBarModule } from "@angular/material/snack-bar";
import { Router } from "@angular/router";
import { AuthService } from "src/app/services/auth.service";

@Component({
  selector: "app-login",
  templateUrl: "./login.component.html",
})
export class LoginComponent implements OnInit {

  loginForm: FormGroup;
  loading = false

  constructor(
    private snackbar: MatSnackBar,
    private authSer: AuthService,
    private router: Router,
    private fb: FormBuilder) {
    this.loginForm = this.fb.group({
      'username': new FormControl('', Validators.required),
      'password': new FormControl('', Validators.required),
      'remember': new FormControl(false),
    })
  }

  ngOnInit(): void {}

  login() {
    this.loading = true
    if (this.loginForm.invalid) {
      console.log(this.loginForm.get('username').hasError('required'))
      console.log(this.loginForm.get('password').hasError('required'))
      return this.snackbar.open('Please fill the form correctly', null, { duration: 5000 })
    }
    const form = new FormData()
    form.append('username', this.loginForm.controls.username.value)
    form.append('password', this.loginForm.controls.password.value)
    
    this.authSer.login(form).subscribe(
      (data) => {
        this.loading = false
        if (!data['refresh'] || !data['access']) {
          return this.snackbar.open('Seems like the tokens are not there. Try again', null, { duration: 5000 })  
        }
        this.authSer.setRefreshToken(data['refresh'])
        this.authSer.setToken(data['access'])
        this.snackbar.open('Login successful', null, { duration: 5000 })
        return this.router.navigate(['/admin']);
      },
      err => {
        this.loading = false
        return this.snackbar.open('Login failed', null, { duration: 5000 })
      },
      () => {
        this.loading = false
      }
    )
    this.loading = false
    
  }
}
