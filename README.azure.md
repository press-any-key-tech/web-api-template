# Azure notes

## Configure Entra ID

### Configure an application

#### Register an application

- Log in to the Azure portal.
- Go to Microsoft Entra ID (Azure Active Directory) > App registrations > New registration.
- Set the name for the application (e.g. "web-template-api-app"), select who can use the application and the account type, and set the redirect URI if needed (this may not be needed for client_credentials).
- Register the application.

#### Configure permissions for your application

- Within the application you just registered, go to the API permissions section.
- Add a permission.
- Select the API you want to use: Microsoft Graph.
- Select the permissions you want to grant to the application:
  - Application permissions: GroupMember -> GroupMember.Read.All.
- Save the permissions (using the button at the bottom of the page).

#### Add security group to the application

- Within the application you just registered, go to Token configuration.
- Select "Add group claim".
- In the new tab, check "Security groups".
- Save the changes.

#### Set scope

- Within the application you just registered, go to Expose an API.
- Press "Add a Scope".
- Set the Application ID URI (default is valid).
- Press "save and continue".
- Set the parameters:
  - Scope name: access_as_user.
  - Who can consent: Admins and users.
  - Name: access as user.
  - Description: Access as a user.
- Press "Add scope".

#### Configure authentication

- Within the application you just registered, go to Authentication.
- Add a platform.
- Select the platform you want to use: Web.
- Set the redirect URI: http://localhost:4040.
- Set another redirect URI: http://localhost:4040/signIn-oidc
- Check the ID tokens and access tokens boxes.
- Save the platform.

#### Change manifest

- Within the application you just registered, go to Manifest.
- Change the "accessTokenAcceptedVersion" to 2.
- Save the changes.

#### Create a secret for the application (optional, for client_credentials)

- Within the application you just registered, go to Certificates & secrets.
- Create a new client secret.
- Set the description and the expiration date.
- Copy the value of the secret because you won't be able to see it again after leaving the page.
- Save the secret.

#### Create groups and assing to user

- Within the application you just registered, go to Groups.
- Create a new group.
- Set the name and the description.
- Save the group.
- Go to Members.
- Add a member.
- Select the user you want to add to the group.
- Save the changes.

## Auth URL

Request format:

```
https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/authorize?client_id={app-client-id}&response_type=id_token%20token&redirect_uri={redirect-uri}&scope=openid%20email%20profile&state={state}&nonce={nonce}
```

- state: A value included in the request that will also be included in the response.
- nonce: A value included in the request that will also be included in the response.

Request example:

```
https://login.microsoftonline.com/224cfe97-68ef-4e8c-a210-94031449aa66/oauth2/v2.0/authorize?client_id=f69dfe13-88bd-4777-98c2-a07f43c2ae55&response_type=id_token%20token&redirect_uri=http%3A%2F%2Flocalhost%3A4040%2FsignIn-oidc&scope=openid%20email%20profile&state=1234567890&nonce=9876543210
```

Response (example):

```
http://localhost:4040/signIn-oidc#access_token=eyJ0eXAiOiJKV1QiLCJub25jZSI6IjQtUnhlNVJCZWpjdk14SVhBZkhFa24yNXAzZVo2TG83aEhaUGhpMEhfQTAiLCJhbGciOiJSUzI1NiIsIng1dCI6InEtMjNmYWxldlpoaEQzaG05Q1Fia1A1TVF5VSIsImtpZCI6InEtMjNmYWxldlpoaEQzaG05Q1Fia1A1TVF5VSJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8yMjRjZmU5Ny02OGVmLTRlOGMtYTIxMC05NDAzMTQ0OWFhNjYvIiwiaWF0IjoxNzExNjYwNTA5LCJuYmYiOjE3MTE2NjA1MDksImV4cCI6MTcxMTY2NjA5MSwiYWNjdCI6MCwiYWNyIjoiMSIsImFjcnMiOlsidXJuOnVzZXI6cmVnaXN0ZXJzZWN1cml0eWluZm8iXSwiYWlvIjoiQVhRQWkvOFdBQUFBS21hRk42UE5Hby9PUHZSa3pCQ2JvRFRxSSt5Z1NPLzlQazZ3enBSeng2djZUQXM3OEZNcUtHT3BDcndjc0g4c1MyS1FwNDB2QUhTWkdXNm5nbkhrS203V0JKTjd5SmllaThxSDBxcUQxck9DUHVURE15eVFUUXJ3NHZ1aE5GVjhwSm9aSGxMQU05TkhlU2FuZmcveFhRPT0iLCJhbHRzZWNpZCI6IjE6bGl2ZS5jb206MDAwMzQwMDE5MzkyNTM0MyIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoid2ViLXRlbXBsYXRlLWFwaS1hcHAiLCJhcHBpZCI6ImY2OWRmZTEzLTg4YmQtNDc3Ny05OGMyLWEwN2Y0M2MyYWU1NSIsImFwcGlkYWNyIjoiMCIsImVtYWlsIjoiaW1wYWxhaEBnbWFpbC5jb20iLCJmYW1pbHlfbmFtZSI6IkZpZ3Vlcm9hIFZpbGxhciIsImdpdmVuX25hbWUiOiJMaW5vIiwiaGFzd2lkcyI6InRydWUiLCJpZHAiOiJsaXZlLmNvbSIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjgzLjU4LjEwMy4xNjEiLCJuYW1lIjoiTGlubyBGaWd1ZXJvYSBWaWxsYXIiLCJvaWQiOiIwMDQwNTQ3Yy04NjY2LTRhOTUtYWI1YS0zYWU2NTgwMGVlMzgiLCJwbGF0ZiI6IjUiLCJwdWlkIjoiMTAwMzdGRkVBQjU2NzkzMyIsInJoIjoiMC5BUzhBbF81TUl1OW9qRTZpRUpRREZFbXFaZ01BQUFBQUFBQUF3QUFBQUFBQUFBQ3dBRG8uIiwic2NwIjoiZW1haWwgb3BlbmlkIHByb2ZpbGUgVXNlci5SZWFkIiwic3ViIjoiMWhiS3VyTWllbWhzcnpvT0dOTFo2SjJabU5tTW1vVkl3SDlhamVGY2VGZyIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJFVSIsInRpZCI6IjIyNGNmZTk3LTY4ZWYtNGU4Yy1hMjEwLTk0MDMxNDQ5YWE2NiIsInVuaXF1ZV9uYW1lIjoibGl2ZS5jb20jaW1wYWxhaEBnbWFpbC5jb20iLCJ1dGkiOiJRZm5FZzF4RU8wV2pxa0Y0OVVFQ0FBIiwidmVyIjoiMS4wIiwieG1zX3N0Ijp7InN1YiI6IkRMTVZKYXN3UDhzQlpmZVdCaHBBSkFZejhKaklMNkw4US1tT1p5VEotaHcifSwieG1zX3RjZHQiOjE1Mjc5NTc2NTIsInhtc190ZGJyIjoiRVUifQ.SvTszNO9Z5HFFhaybGiFM1alQAmrgC614SpnNUdjxR0QwGJTUsMjrLQsQ4VWVOybnON3Zh4QM3SyjDeXAIMZty2NTdi-d_aRgUFV1obzmcpSxgiDJzoQ52uEn6wvpCfxME-IbHon8JDeuXjoXLtsbcy-dUFQHBJ3XZlTzkmjwv_sJKah5v2oP9OiDD_Ap7xP_YV0YpzPK7XSCZqtiEHyR0vBiq8tDKy4lNYD9TVOlS7LgYNZZ_wUVZJIJdWolEsQjvFm4a-SN6sBFXFOilPjBakEyWwwPh9NhHtsYpsq2NfWoAwOza7B2SRhXxAcHMiWi0IvFUCZi-ShlxBbRHEvVA&token_type=Bearer&expires_in=5281&scope=email+openid+profile+00000003-0000-0000-c000-000000000000%2fUser.Read&id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6InEtMjNmYWxldlpoaEQzaG05Q1Fia1A1TVF5VSJ9.eyJhdWQiOiJmNjlkZmUxMy04OGJkLTQ3NzctOThjMi1hMDdmNDNjMmFlNTUiLCJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vMjI0Y2ZlOTctNjhlZi00ZThjLWEyMTAtOTQwMzE0NDlhYTY2L3YyLjAiLCJpYXQiOjE3MTE2NjA1MDksIm5iZiI6MTcxMTY2MDUwOSwiZXhwIjoxNzExNjY0NDA5LCJhaW8iOiJBYVFBVy84V0FBQUFsdHc2QWZIc2JYd21PRlNUZlkyb3N2WkRzTUYxNUd1VkRqL0owaVNWVWlQaVFsRlhmaXpEaHQ1MzFzM2lxd0Q2eDV3cmp1R1dVVGQvMmhxMnFLbnJPSExiOFZVTEhIQTV2UFh5LzBDakJDTWZxUjJrNGtqY0FiVld3VU5UQlNjMlZqaEtlbHZ5bVhOVUpvTFM4dVFoOVFEWUJKcWtaVEFjTGFFeXUrL09rUkpPdjZwckRWaVZtZUpnOXhnKzBBM0paZktMWjYzVWRsRENBSFU2S0RCcFB3PT0iLCJhdF9oYXNoIjoic1U0bXNkX2ZNOE5XSGEzN19TZ25QUSIsImVtYWlsIjoiaW1wYWxhaEBnbWFpbC5jb20iLCJncm91cHMiOlsiMGU1NDNiODUtMTBmMy00Y2IwLTg1Y2EtZjcxYWI1NjAzZjdmIiwiNTY2YTZjMWEtZGUzMS00ZmEzLWEzMDYtNzJlYTMwOGQzMDhiIiwiMjQ3YjAzYzQtZWQ0Yi00Yjc0LWFhZjItY2MwMDc0NGJhMmY2Il0sImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzkxODgwNDBkLTZjNjctNGM1Yi1iMTEyLTM2YTMwNGI2NmRhZC8iLCJuYW1lIjoiTGlubyBGaWd1ZXJvYSBWaWxsYXIiLCJub25jZSI6Ijk4NzY1NDMyMTAiLCJvaWQiOiIwMDQwNTQ3Yy04NjY2LTRhOTUtYWI1YS0zYWU2NTgwMGVlMzgiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJpbXBhbGFoQGdtYWlsLmNvbSIsInJoIjoiMC5BUzhBbF81TUl1OW9qRTZpRUpRREZFbXFaaFAtbmZhOWlIZEhtTUtnZjBQQ3JsV3dBRG8uIiwic3ViIjoiRExNVkphc3dQOHNCWmZlV0JocEFKQVl6OEpqSUw2TDhRLW1PWnlUSi1odyIsInRpZCI6IjIyNGNmZTk3LTY4ZWYtNGU4Yy1hMjEwLTk0MDMxNDQ5YWE2NiIsInV0aSI6IlFmbkVnMXhFTzBXanFrRjQ5VUVDQUEiLCJ2ZXIiOiIyLjAifQ.n4PknI8DNhjJ9TGdRLe8CWIU5jzBGAkNnb9Khok7QHgpioMz6p_SWEdJFO2CsQBI57Fmzj_xiah9W_mKwhE2Fouv_ikTDbDj9gzFxAx1Pd14PxoWqBWavVrWRduIQdVT2-BkmxednpOoN-sqGmb6wUc_B5MwTPd7DgqTEziZUa13UITSozzfckPpXmmQa6bZN_dTXgmKEei05fo15oxQA6bub4d56hf8NG5A2YZxNCzxTJ6KxnWdDNSyVt6TFAoVbCsxDtQQdTTAnhwymaez5gww7RcN-ear5DMy8OX6PvY28X5g-9r7LpbtHZSa3cYjyqLwcLymcPvzImpszsXY7g&state=1234567890&session_state=9ed17b52-027e-40e0-acf5-84a79ecb767e
```

Decoded id_token (example):

```json

Header
{
  "typ": "JWT",
  "alg": "RS256",
  "kid": "XRvko8P7A3UaWSnU7bM9nT0MjhA"
}

Payload
{
  "aud": "f69dfe13-88bd-4777-98c2-a07f43c2ae55",
  "iss": "https://login.microsoftonline.com/224cfe97-68ef-4e8c-a210-94031449aa66/v2.0",
  "iat": 1711556370,
  "nbf": 1711556370,
  "exp": 1711560270,
  "aio": "AaQAW/8WAAAABFKB3Iry7EEOTlB9c7FyCdcy53VkE9BQw1hszMJbR5e1mW89pltOKLQhRe+s9Skap5RF2gXPlS7OiaxdYa6R8l4BxFmRrOO6OVs2tou23tPMjfhIHd5mM819Ws/HgVTaW+oyhwNDSGOsSQguUgI0mfa9pitKMRBUj+9BVF7JV+yjZEYI17nCP92x4cEi0YJIf/yh2xxi004uQrqJRcSUvw==",
  "at_hash": "5VMzw0D7AbGo5L-O36_zoA",
  "email": "xxxx@gmail.com",
  "groups": [
    "0e543b85-10f3-4cb0-85ca-f71ab5603f7f",
    "566a6c1a-de31-4fa3-a306-72ea308d308b",
    "247b03c4-ed4b-4b74-aaf2-cc00744ba2f6"
  ],
  "idp": "https://sts.windows.net/9188040d-6c67-4c5b-b112-36a304b66dad/",
  "name": "Name Surname Surname",
  "nonce": "9876543210",
  "oid": "0040547c-8666-4a95-ab5a-3ae65800ee38",
  "preferred_username": "xxxx@gmail.com",
  "rh": "0.AS8Al_5MIu9ojE6iEJQDFEmqZhP-nfa9iHdHmMKgf0PCrlWwADo.",
  "sub": "DLMVJaswP8sBZfeWBhpAJAYz8JjIL6L8Q-mOZyTJ-hw",
  "tid": "224cfe97-68ef-4e8c-a210-94031449aa66",
  "uti": "JVnG8wVf_kOtxnjP1uIjAA",
  "ver": "2.0"
}


```

## JWKS verification

Request format:

```http
GET https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration

GET https://login.microsoftonline.com/224cfe97-68ef-4e8c-a210-94031449aa66/v2.0/.well-known/openid-configuration

```
