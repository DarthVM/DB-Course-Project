SELECT
    users.group
FROM storage.users
WHERE
    login = '$login'
    AND
    password = '$password'