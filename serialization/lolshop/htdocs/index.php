<?php

header("Content-Security-Policy: default-src 'self'; object-src 'none'; base-uri 'none'; font-src https://stackpath.bootstrapcdn.com; style-src 'self' https://stackpath.bootstrapcdn.com; script-src 'self' https://ajax.googleapis.com https://cdnjs.cloudflare.com https://stackpath.bootstrapcdn.com https://cdn.jsdelivr.net https://unpkg.com 'unsafe-eval'; img-src 'self' data: ");

?>

<!DOCTYPE html>
<html lang="en">

<head>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>LOLSHOP - Buy yourself a pass grade for the exam!</title>

  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" crossorigin="anonymous">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" crossorigin="anonymous">

  <link href="css/custom.css" rel="stylesheet">

</head>

<body>
   <div id="app">

  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container">
      <router-link class="navbar-brand" href="#" to="/">LOLSHOP</router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <nav-bar></nav-bar>
    </div>
  </nav>

  <div class="container">
    <div class="row">
      <div class="col-lg-9">
            <router-view></router-view>
      </div>
    </div>
  </div>

  <footer class="py-5 bg-dark">
    <div class="container">
      <p class="m-0 text-center text-white">Copyright &copy; Advanced Cybersecurity Topics 2019</p>
    </div>
  </footer>

  </div>

  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/vue@2.6.11"></script>
  <script src="https://unpkg.com/vue-router/dist/vue-router.js"></script>
  
  <script type="module" src="js/main.js"></script>

  <script type="text/x-template" id="shop-block">
        <div class="col-lg-4 col-md-6 mb-4">
        <div class="card h-100">
        <img class="card-img-top" :src="picture_data_uri">
        <div class="card-body">
            <h4 class="card-title">
            {{ item.name }}
            </h4>
            <h5>{{ item.price }}</h5>
            <p class="card-text">{{ item.description }}</p>
        </div>
        <div class="card-footer">
            <button v-if="$root.$data.session" type="button" v-on:click="addToCart" v-on:submit.prevent class="add-to-cart-btn btn btn-danger">Add to cart</button>
        </div>
        </div>
    </div>
  </script>

  <script type="text/x-template" id="shop">
    <div>
        <div v-if="!$root.$data.session" class="alert alert-primary" role="alert">
            Hello stranger! To buy goods, you need to <route-link href="#" to="/session">create a session</route-link>.
        </div>
        <div v-else class="alert alert-success" role="alert">
            Please keep in mind that the real Answer to the Ultimate Question of Life, the Universe, and Everything lies in this server, and precisely in the file <b>/secret/flag.txt</b>.
        </div>
        <div class="row">
            <shop-block v-for="item in products" :item="item"></shop-block>
        </div>
    </div>
  </script>

  <script type="text/x-template" id="create-session">
        <form>
            <div class="form-group">
                <label for="name">Name</label>
                <input type="text" class="form-control" v-model="name" placeholder="Enter your name">
            </div>
            <div class="form-group">
                <label for="email">Email address</label>
                <input type="email" class="form-control" v-model="email" placeholder="Enter your email address">
            </div>
            <button type="submit" v-on:click="btnSubmit" v-on:submit.prevent="btnSubmit" class="btn btn-primary">Submit</button>
        </form>
  </script>

  <script type="text/x-template" id="shopping-cart">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">Qty</th>
                    <th scope="col">Name</th>
                    <th scope="col">Unit Price</th>
                    <th scope="col">Price</th>
                </tr>
            </thead>
            <tbody>
                <shopping-cart-item v-for="line in enrichedCart" :line="line"></shopping-cart-item>
            </tbody>
        </table>
  </script>

  <script type="text/x-template" id="payment">
  <div>
            <div v-if="shareError" class="alert alert-primary" role="alert">
                There was an error sharing your whishlist
            </div>
            <div v-if="shareCompleted" class="alert alert-primary" role="success">
                Your whishlist has been shared! Give this link to all your friends: <b>{{ shareURL }}</b>!
            </div>
            <shopping-cart :cart="$root.$data.cart"></shopping-cart>
            <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#paymentModal">
                Pay
            </button>
            <button type="button" class="btn btn-primary" v-on:click="share">
                Share as Wishlist
            </button>
            <payment-modal></payment-modal>
        </div>
  </script>

  <script type="text/x-template" id="wishlist">
      <div>
        <div v-if="failure" class="alert alert-primary" role="alert">
                    There was an error loading your whishlist
        </div>
        <span id="wishlistMessage" v-once></span>
        <div v-if="loaded">
            <shopping-cart :cart="cart"></shopping-cart>
        </div>
      </div>
</script>

<script type="text/x-template" id="nav-bar">
<div class="collapse navbar-collapse" id="navbarResponsive">
        <span v-if="$root.$data.session" class="navbar-text">
            Welcome, {{ $root.$data.name }}!
        </span>

        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <router-link class="nav-link" href="#" to="/">Shop</router-link>
          </li>
          <li v-if="!$root.$data.session" class="nav-item">
            <router-link class="nav-link" href="#" to="/session">Create Session</router-link>
          </li>
          <li v-if="$root.$data.session" class="nav-item">
            <router-link class="nav-link" href="#" to="/payment">Checkout ({{ cart_length }} items)</a>
          </li>
          <li v-if="$root.$data.session" class="nav-item">
            <a href="#" class="nav-link" v-on:click="logout">Clear Session</a>
          </li>
        </ul>
    </div>
</script>

<script type="text/x-template" id="payment-model">
<div class="modal fade" id="paymentModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Payment Details</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body" v-if="!paymentComplete">
        <div v-if="paymentError" class="alert alert-primary" role="alert">
            There was an error processing the form. Please check your data and try again.
        </div>
        <form role="form">
        <div class="form-group">
            <label for="cardNumber">Card Number</label>
            <div class="input-group">
                <input type="text" class="form-control" v-model="creditCard" placeholder="Card Number" required autofocus />
                <span class="input-group-addon"><span class="glyphicon glyphicon-lock"></span></span>
            </div>
        </div>
        <div class="row">
            <div class="col-xs-7 col-md-7">
                <div class="form-group">
                    <label for="expiryMonth">Expiry Date</label>
                    <div class="col-xs-6 col-lg-6 pl-ziro">
                        <input type="text" class="form-control" v-model="expiryMonth" placeholder="MM" required />
                    </div>
                    <div class="col-xs-6 col-lg-6 pl-ziro">
                        <input type="text" class="form-control" v-model="expiryYear" placeholder="YY" required /></div>
                    </div>
                </div>
                <div class="col-xs-5 col-md-5 pull-right">
                    <div class="form-group">
                        <label for="cvCode">
                            CVV</label>
                        <input type="password" class="form-control" v-model="cvv" placeholder="CVV" required />
                    </div>
                </div>
            </div>
        </form>
        </div>
        <div class="modal-body" v-if="paymentComplete">
            <p>Great news! Your payment was successful.</p>
        </div>
        <div class="modal-footer" v-if="!paymentComplete">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
          <button type="submit" v-on:click="btnSubmit" v-on:submit.prevent="btnSubmit" class="btn btn-primary">Submit</button>
        </div>
        <div class="modal-footer" v-if="paymentComplete">
          <button type="button" class="btn btn-primary" data-dismiss="modal">OK</button>
        </div>
      </div>
    </div>
    </div>      
</script>

</body>

</html>
