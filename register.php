<!DOCTYPE html>
<html lang="en" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>REGISTER</title>
        <link rel="stylesheet" href="css/style.css">
        <link rel="stylesheet" href="css/bootstrap.min.css">
    </head>
    <body>
        <div class="center2">
            <h1>Create an account</h1>
            <form method="post">
              <div class="row">
                 <div class="col-lg-6">
                     <div class="txt_field">
                        <input type="text" required>
                        <span></span>
                        <label>First Name</label>
                     </div>
                  </div>
                  <div class="col-lg-6">
                    <div class="txt_field">
                        <input type="text" required>
                        <span></span>
                        <label>Last Name</label>
                    </div>
                 </div>
             </div>
              <div class="txt_field">
                <input type="text" required>
                <span></span>
                <label>Email address</label>
              </div>
              <div class="txt_field">
                <input type="text" required>
                <span></span>
                <label>Phone</label>
              </div>
              <div class="row">
              <div class="col-lg-6">
              <div class="txt_field">
                <input type="password" required>
                <span></span>
                <label>Enter Password</label>
              </div></div>
              <div class="col-lg-6">
              <div class="txt_field">
                <input type="password" required>
                <span></span>
                <label>Confirm Password</label>
              </div></div>
              </div>
              <input type="submit" value="Register">
              <div class="login_link">
                Already have an account? <a href="login.php">Login</a>
              </div>
            </form>
        </div>
    </body>
</html>