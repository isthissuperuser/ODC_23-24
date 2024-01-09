# CSP
 - we see that in the csp header there is default-src with google and a a google cdn and unsafe eval
 - moreover we see that the input that we give is not escaped
 - we use this in order to download an unsafe version of angular from the google CDN an let it use eval to execute unintented js code
