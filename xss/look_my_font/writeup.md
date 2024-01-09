# Look my font
 - `try_font` endpoint accepts 3 query string parameters: `font_url`, `font_name`, `text`
 - `font_url` is used for letting the client side javascript download a font but in order to let it do that, the server must modify csp
 - we see that our string in `font_url` gets injected without being checked or escaped direclty into the csp policy by the server
 - With this, we perform a csp injection and because we can overwrite previous values defined in csp only by going lower in the permissions, we can't exploit the ones that happen to be alreayd there
 - `form-action` and `script-src-elem` aren't still set so we can use them in order to run non-intended javascript
 - We use also 'unsafe-inline' so we can write javascript in inline javascript handlers
 - `text` field is also not escaped or checked, hence we use it to pu our attack vector finalizing the exploit
