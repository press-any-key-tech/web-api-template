# Azure notes

## Configure Google identity platform

### Configure a provider

- Log in into de Google Cloud portal.
- Go to Google Identity Platform.
- In the "providers" option, select "Add a provider"
- Select "Email/Password".
- Check "enabled" and select "save".

### Create a user

- Log in into de Google Cloud portal.
- Go to Google Identity Platform.
- Press "Add user", enter the details and Save.

### Groups

Google identity platform does not allow groups.


## Auth URL

Request format:

```
https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={{google_api_key}}

Google api key can be obtained in the providers tab.

```

Body
```json
{
  "email": "xxxx@gmail.com",
  "password": "the password",
  "returnSecureToken": true
}

```

Example response:

```json
{
    "kind": "identitytoolkit#VerifyPasswordResponse",
    "localId": "b34eNtqQskg1WaxtL6cbk347M1d2",
    "email": "xxxxx@gmail.com",
    "displayName": "",
    "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImJhNjI1OTZmNTJmNTJlZDQ0MDQ5Mzk2YmU3ZGYzNGQyYzY0ZjQ1M2UiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vbGludXMtdGVycmFmb3JtLTAwMSIsImF1ZCI6ImxpbnVzLXRlcnJhZm9ybS0wMDEiLCJhdXRoX3RpbWUiOjE3MTE3MTM2ODYsInVzZXJfaWQiOiJiMzRlTnRxUXNrZzFXYXh0TDZjYmszNDdNMWQyIiwic3ViIjoiYjM0ZU50cVFza2cxV2F4dEw2Y2JrMzQ3TTFkMiIsImlhdCI6MTcxMTcxMzY4NiwiZXhwIjoxNzExNzE3Mjg2LCJlbWFpbCI6ImltcGFsYWhAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImltcGFsYWhAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.fLfmnuEeoVps3zWPbfa1kytOqIrZm-DTPosHe7Qg437IqL8yzgbJq5pF3RHxBe6Hk2exo0sTwGA1S9m31xvXZ8818tHIYkVjw1IGlrcxMa_rCbRR6f6pd6JIR2wHUCQ5nrCM8x1X1tSzpNyNLkiUlYOti7P_zFyETlULmyZqw2AZix9Uc3WkhpUH3MR2QGlX7tLYXcHMCqDpp4FF2Ps7N4YvzZYVq_wUwXiNMHFLK8hKeE1d9rW2iprAMjQbchfDDZn57TiwNXGVeSRHabMppoTF_NqzlHa3pV62l6lZSxCbNOnGIkI4_KDLr3gRNkC80YYIAE--YCzX_mM9PdDBbg",
    "registered": true,
    "refreshToken": "AMf-vBwtrRU20VSOe7LdlRnN_DPM0S-j8ejK7_UKRv7Dw02z7r2kI0VFoAWOqsGmlKMhKTd_yrgiMHnA6SElWzZc-FZuOWL-O-LDPi9kQDYCcPCgIgH0EJgyhunPZPXVDXn_HNC_1EzsnYvb2PN-_UsVUNmSXedh51fzIYI1EC9tpRWPzOuS80yXK4cBaU7M1ANqwGHF9EqYK-DKzmGve1DNo5h0BaXMsQ",
    "expiresIn": "3600"
}
```


Decoded id_token (example):

```json

header

{
  "alg": "RS256",
  "kid": "ba62596f52f52ed44049396be7df34d2c64f453e",
  "typ": "JWT"
}

payload

{
  "iss": "https://securetoken.google.com/google-project-id",
  "aud": "google-project-id",
  "auth_time": 1711713686,
  "user_id": "b34eNtqQskg1WaxtL6cbk347M1d2",
  "sub": "b34eNtqQskg1WaxtL6cbk347M1d2",
  "iat": 1711713686,
  "exp": 1711717286,
  "email": "xxxxx@gmail.com",
  "email_verified": false,
  "firebase": {
    "identities": {
      "email": [
        "xxxxx@gmail.com"
      ]
    },
    "sign_in_provider": "password"
  }
}

```

## JWKS verification

