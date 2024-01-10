# metactf
 - the site lets you see chalenges, download users and also upload users
 - the challenges are expressed with a class `Challenge` that has a destruct method. If the method is called the challenge is run.
 - We just serialize the class Challenge with the the command that we want (the one to display the flag) and upload it as a user
 - it will get unserialized and the `__destruct` method will be called actually running what we want
