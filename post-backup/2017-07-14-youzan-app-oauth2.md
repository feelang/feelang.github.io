---
layout: single
title: 有赞自有 APP 的 OAuth2 授权模型分析
date: 2017-07-14
categories: Network
tags:
  - OAuth2
---

有赞自有 APP（微商城、微小店）的 OAuth2 类型是 **Resource Owner Password Credentials**。

```
The resource owner password credentials (i.e., username and password)
can be used directly as an authorization grant to obtain an access
token.  The credentials should only be used when there is a high
degree of trust between the resource owner and the client (e.g., the
client is part of the device operating system or a highly privileged
application), and when other authorization grant types are not
available (such as an authorization code).

Even though this grant type requires direct client access to the
resource owner credentials, the resource owner credentials are used
for a single request and are exchanged for an access token.  This
grant type can eliminate the need for the client to store the
resource owner credentials for future use, by exchanging the
credentials with a long-lived access token or refresh token.
```

其验证流程如下所示：

```
+----------+
| Resource |
|  Owner   |
|          |
+----------+
      v
      |    Resource Owner
      (A) Password Credentials
      |
      v
+---------+                                  +---------------+
|         |>--(B)---- Resource Owner ------->|               |
|         |         Password Credentials     | Authorization |
| Client  |                                  |     Server    |
|         |<--(C)---- Access Token ---------<|               |
|         |    (w/ Optional Refresh Token)   |               |
+---------+                                  +---------------+

      Figure 5: Resource Owner Password Credentials Flow
```


可以通过一个具体的请求来分析一下登录流程：

**第一步：** 用户（resource owner）通过 APP（client）向 SSO接入服务发起登录请求来获取 access token。

> https://uic.youzan.com/sso/yzApp/login

该请求必须是 POST 请求（Content-Type: application/x-www-form-urlencoded），请求参数如下：

```
grant_type
      REQUIRED.  Value MUST be set to "password".

username
      REQUIRED.  The resource owner username.

password
      REQUIRED.  The resource owner password.

scope
      OPTIONAL.  The scope of the access request.
```

除此之外还要带上客户端身份（client credentials）

```
client_id
      REQUIRED.

client_secret
      REQUIRED. 
```

**第二步：** SSO 接入服务拿到请求之后，先通过 username & password 去 Account服务验证用户身份，然后携带 Account 服务返回的 user_id 以及 client_id & client_secret 去 carmen-oauth 验证 client 身份，

![](/assets/imgs/auth-server.jpeg)

```
The authorization server MUST:

   o  require client authentication for confidential clients or for any
      client that was issued client credentials (or with other
      authentication requirements),

   o  authenticate the client if client authentication is included, and

   o  validate the resource owner password credentials using its
      existing password validation algorithm.
```

**第三步：** 如果 client 和 resource owner 的身份验证成功，authorization server（SSO接入服务 & carmen-oauth）就会签发 access_token 以及可选的 refresh_token。

Response 参数如下：

```
The authorization server issues an access token and optional refresh token, 
and constructs the response by adding the following parameters 
to the entity-body of the HTTP response with a 200 (OK) status code:

   access_token
         REQUIRED.  The access token issued by the authorization server.

   token_type
         REQUIRED.  The type of the token issued as described in
         Section 7.1.  Value is case insensitive.

   expires_in
         RECOMMENDED.  The lifetime in seconds of the access token.  For
         example, the value "3600" denotes that the access token will
         expire in one hour from the time the response was generated.
         If omitted, the authorization server SHOULD provide the
         expiration time via other means or document the default value.
   
   refresh_token
         OPTIONAL.  The refresh token, which can be used to obtain new
         access tokens using the same authorization grant as described
         in Section 6.

   scope
         OPTIONAL, if identical to the scope requested by the client;
         otherwise, REQUIRED.  The scope of the access token as
         described by Section 3.3.
```

时机可以的话，再来分析一下「AppSDK」和「微商城小程序」。 
