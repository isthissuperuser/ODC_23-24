Vue.config.devtools = true

var act = {
    addToCart: function(productId) {
        $.ajax({
            type: 'POST',
            url: '/api/add_to_cart.php',
            data: {
                state : app.state,
                product : productId
            }
        }).done(function(data) {
            app.state = data.state
            // refresh cart client-side
            $.ajax({
                url: '/api/cart.php',
                type: 'POST',
                data: {
                    state: app.state
                }
            }).done(function(data) {
                app.cart.length = 0;
                data.cart.forEach(function(x) {
                    app.cart.push(x)
                });
            });
        });
    },
    createSession: function(name, email, callback) {
        $.ajax({
            type: 'POST',
            url: '/api/new_session.php',
            data: {
                name : name,
                email : email
            }
        }).done(function(data) {
            app.state = data.state;
            app.session = data.session_id;
            app.name = name;
            app.email = email;
            callback();
        });
    },
    payment: function(payment, callbackSuccess, callbackFailure) {
        $.ajax({
            type: 'POST',
            url: '/api/purchase.php',
            data: {
                payment: payment,
                state: app.state
            }
        }).done(function(data) {
            app.state = data.state;
            app.cart.length = 0;
            callbackSuccess();
        }).fail(function(data) {
            callbackFailure();
        })
    },
    share: function(callbackSuccess, callbackFailure) {
        $.ajax({
            type: 'POST',
            url: '/api/cart.php',
            data: {
                state: app.state,
                save: true
            }
        }).done(function(data) {
            callbackSuccess(data.token);
        }).fail(function(data) {
            callbackFailure();
        })
    },
    logout: function() {
        app.state = null;
        app.session = null;
        app.name = null;
        app.email = null;
        app.cart.length = 0;
    }
}

Vue.component('shop-block', {
    props: ['item'],
    methods: {
        addToCart() {
            act.addToCart(this.$props.item.id);
        }
    },
    computed: {
        picture_data_uri() {
            return "data:image/jpeg;base64," + this.$props.item.picture;
        }
    },
    template: '#shop-block'
});

const Shop = {
    template: '#shop',
    data() {
        return {
            'products' : this.$root.$data.products
        }
    }
}

const CreateSession = {
    data() {
        return {
            'name' : '',
            'email' : ''
        }
    },
    methods: {
        btnSubmit : function() {
            act.createSession(this.name, this.email, function() {
                router.push('/');
            });
        }
    },
    template: '#create-session'
}

Vue.component('shopping-cart', {
    props: ['cart'],
    computed: {
        enrichedCart: function() {
            var out = [];
            let products = this.$root.$data.products;
            let findProductById = function(query) {
                return products.find(function(e) {
                    return e['id'] == query;
                })
            }
            this.cart.forEach(function(e) {
                let product = findProductById(e.product);
                if(product) {
                    out.push({
                        'qty' : e.quantity,
                        'name' : product.name,
                        'unitPrice' : product.price,
                        'linePrice' : product.price * e.quantity
                    })
                } else {
                    out.push({
                        'qty' : e.quantity,
                        'name' : 'N/D',
                        'unitPrice' : 'N/D',
                        'linePrice' : 'N/D'
                    })
                }
            });
            return out;
        },
    },
    template: '#shopping-cart'
});

Vue.component('shopping-cart-item', {
    props: ['line'],
    template: `
        <tr>
            <th scope="row">{{ line.qty }}</th>
            <td>{{ line.name }}</td>
            <td>{{ line.unitPrice }}</td>
            <td>{{ line.linePrice }}</td>
        </tr>
    `
});

const Payment = {
    data() {
        return {
            'shareError' : false,
            'shareCompleted' : false,
            'shareToken' : null
        }
    },
    computed: {
        shareURL: function() {
            return window.location.origin + window.location.pathname + this.$router.resolve('/wishlist').href + '/' + this.shareToken;
        }
    },
    methods: {
        share: function() {
            let that = this;
            that.shareError = false;
            that.shareCompleted = false;
            act.share(function(token) {
                that.shareCompleted = true;
                that.shareToken = token;
                that.shareError = false;
            }, function() {
                that.shareError = true;
                that.shareCompleted = false;
            });
        }
    },
    template: '#payment' 
}

const Wishlist = {
    data() {
        return {
            name: '',
            email: '',
            cart: [],
            failure: false,
            loaded: false
        }
    },
    created () {
        this.fetchData()
      },
      watch: {
        '$route': 'fetchData'
      },
      methods: {
        fetchData () {
            var that = this;
            this.failure = false;
            $.ajax({
                url: '/api/cart.php',
                type: 'POST',
                data: {
                    token: this.$route.params.token
                }
            }).done(function(data) {
                that.cart.length = 0;
                data.cart.forEach(function(x) {
                    that.cart.push(x)
                });
                that.loaded = true;
                $('#wishlistMessage').html('<p>Hey! <b>' + data.name + '</b> shared his/her wishlist with you!');
            }).fail(function(data) {
                that.failure = true;
            });
        }
      },
      template: '#wishlist'
}

Vue.component('nav-bar', {
    computed: {
        cart_length : function() {
            return this.$root.$data.cart.reduce(function(acc, el) {
                return acc + el.quantity
            }, 0);
        }
    },
    methods: {
        logout : function() {
            act.logout();
            router.push('/');
        }
    },
    template: '#nav-bar'
});

Vue.component('payment-modal', {
    data() {
        return {
            'creditCard' : '',
            'expiryMonth' : '',
            'expiryYear' : '',
            'cvv' : '',
            'paymentComplete' : false,
            'paymentError' : false
        }
    },
    methods: {
        btnSubmit : function() {
            let payment = {
                credit_card : this.creditCard,
                expiry_month : this.expiryMonth,
                expiry_year : this.expiryYear,
                cvv : this.cvv
            }
            let that = this;
            act.payment(payment, function() {
                /* success */
                that.paymentComplete = true;
                that.paymentError = false;
            }, function() {
                /* error */
                that.paymentError = true;
                that.paymentComplete = false;
            });
        }
    },
    template: '#payment-model'
})

const router = new VueRouter({
    routes: [
        { path: '/', component: Shop },
        { path: '/session', component: CreateSession },
        { path: '/payment', component: Payment },
        { path: '/wishlist/:token', component: Wishlist }
    ]
})

const app = new Vue({
    el: '#app',
    router: router,
    data: {
        state : null,
        session: null,
        name : null,
        email : null,
        products : [],
        cart : []
    },
    mounted() {
        this.state = localStorage.getItem('state');
        this.session = localStorage.getItem('session');
        this.name = localStorage.getItem('name');
        this.email = localStorage.getItem('email');

        let that = this;

        $.ajax({
            url: '/api/products.php'
        }).done(function(data) {
            data.products.forEach(function(x) {
                that.products.push(x);
            });
        });

        if(this.state) {
            $.ajax({
                url: '/api/cart.php',
                type: 'POST',
                data: {
                    state: this.state
                }
            }).done(function(data) {
                data.cart.forEach(function(x) {
                    that.cart.push(x)
                });
            });
        }

    },
    watch: {
        state(newState) {
            if(newState) {
                localStorage.state = newState;
            } else {
                localStorage.removeItem('state');
            }
        },
        session(newSession) {
            if(newSession) {
                localStorage.session = newSession;
            } else {
                localStorage.removeItem('session');
            }
        },
        name(newName) {
            if(newName) {
                localStorage.name = newName;
            } else {
                localStorage.removeItem('name');
            }
        },
        email(newEmail) {
            if(newEmail) {
                localStorage.email = newEmail;
            } else {
                localStorage.removeItem('email');
            }
        },
    }
})
