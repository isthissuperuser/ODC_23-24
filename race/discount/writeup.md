# discount
 - we need to buy the item flag and when we will have done it we will be able to see its description (the flag)
 - there is no way to load money so we need to send a lot of requests to `/apply_discount` in parallel in order to apply it as much as we can before it gets deleted
 - first we register an account and get the discount code
 - second we add to the cart the flag item, creating also a cart
 - third we bombard the server with parallel requests to `apply_discount` and we will get our disocunt
 - we buy the flag item at 0$ and read the flag

> *N.B.*: I found this challenge to be a little be bugged. In particular if you use requests.Session to handle the session it will be harder for the exploit to work with repsect
> if you manage yourselfyour session manually with the cookies. Why is that is still to me a mistery.
