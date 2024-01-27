SELECT
   login,
   password
FROM storage.users
WHERE
    login = '$login'
    AND
    password = '$password'