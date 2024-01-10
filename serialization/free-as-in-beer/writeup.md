#free\_as\_in\_beer
 - the site is a manager for todos. if query parameter `source` is set the php source code of the current page is displayed.
 - It is printed by the class `GPLSourceBloater` via its variable `source`
 - `source` variable is set by the code to be `__file__` hence indicating this current file
 - we can see that we can upload todos both via input text and via cookies
 - each todo is first serialized and then it is computed the md5 digest and the concat of these two things is added to the cookies
 - we basically do the reverse process but with the GPLBlocaterClass so when it will be unserialized the code will think its a todo but instead it will be the class
 - before serializing we also set the variable `source` of the class to point to the file `flag.php`
 - we make a request with the cookie, the site reads it, computes it and prints it but actually the file `flag.php` will be printed granting us the flag.
