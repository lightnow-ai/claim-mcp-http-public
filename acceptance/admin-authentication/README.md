# Public metadata for local Admin authentication intake

These six secret-free `server.json` files are exact copies of the operator-owned
HTTP fixture definitions in the private implementation repository
[`lightnow-ai/claim-mcp-http`](https://github.com/lightnow-ai/claim-mcp-http),
commit `8b2aa8f9462fed4527609a4d678429d0c0044e1d`, at the same subfolder paths.
Only these public start definitions are mirrored here; no implementation,
private repository history, credentials or captured scan results are copied.

The manifest's `repository.url` and `repository.subfolder` deliberately retain
the actual private implementation/definition source. This public repository is
the metadata intake source. The normal SYSTEM repository-import path records
that source ref separately from the declared implementation URL.

The existing local TLS edge `https://mcp-auth.lightnow.local` forwards to the
owned HTTP fixture on port 8017. Its running implementation is commit
`5e0756732b738752cd615c3ba5e5da795c3394c7`; the later definition commit changes
only metadata. No new endpoint or authentication implementation is provided by
this public repository. Each protected route exposes `discovery_fixture`.
The public repository's own unauthenticated `identify` server is unchanged.

Use the reviewed public commit SHA as `<ref>` for normal Admin repository intake:

```text
https://github.com/lightnow-ai/claim-mcp-http-public/tree/<ref>/acceptance/admin-authentication/api-key
https://github.com/lightnow-ai/claim-mcp-http-public/tree/<ref>/acceptance/admin-authentication/basic
https://github.com/lightnow-ai/claim-mcp-http-public/tree/<ref>/acceptance/admin-authentication/bearer
https://github.com/lightnow-ai/claim-mcp-http-public/tree/<ref>/acceptance/admin-authentication/pat
https://github.com/lightnow-ai/claim-mcp-http-public/tree/<ref>/acceptance/admin-authentication/api-key-or-oidc
https://github.com/lightnow-ai/claim-mcp-http-public/tree/<ref>/acceptance/admin-authentication/oauth-pkce
```

Configure missing, incorrect and correct credentials through the existing Admin
Version Operations and manual scan controls. OAuth registration behavior is
read from the actual fixture metadata; its definition declares authorization
code with PKCE. These definitions preload neither credentials, capabilities,
authentication observations nor publication exceptions.

## Definition integrity

SHA-256 of each `server.json`, identical in both repositories at the source
commit above:

| Profile | SHA-256 |
| --- | --- |
| `api-key` | `ddff8fecaa8aa0d9370bb354ac0d7be584fd7d8cf82ebe868be5b1469075c644` |
| `basic` | `a25ada44df2ea9941ecfaf53883bb172af19e35d9a974c3a451b4386746381d0` |
| `bearer` | `2adaaa2b4db654aa176ab4901146e3b62bc68f578db3f3bb94a84c352d212638` |
| `pat` | `4566fa32a5722785f76a0c4723def57bd917caf331ef7b49053498402997dbb0` |
| `api-key-or-oidc` | `07fc8d3b02e72102b7a9653f146f3588811cb041760f5fa8b28049f08384a6b5` |
| `oauth-pkce` | `fab06f001b21fa68084c3aed80ab89256c70c41d7b159ae2ab028eb42626f9c7` |
