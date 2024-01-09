# strict-CSP
 - by inspecting the csp we see that script-src is set as 'self' and 'strict-dynamic' and then a nonce is provided
 - hence we cannot do as before, we need to run our javascript code by providing it the nonce (impossible, it changes at every request) or by make it run by another js that has been already approved (with the right nonce)
 - we see that require.js is download and used by the app -> it is approved
 - When it is initialized it looks for a script element with the data-main attribute and use its value as a "pre-initialization" javascript script
 - We use base64 to encode inside it multiline javascript
 - we post the comment with the xss finilizing the exploit 
