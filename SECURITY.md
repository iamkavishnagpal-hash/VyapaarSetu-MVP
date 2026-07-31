# Security Policy — VyapaarSetu

## Reporting Security Vulnerabilities
If you discover a potential security vulnerability in VyapaarSetu, please report it immediately to security@vyapaarsetu.io.

## Security Practices
- All mock payment transactions utilize sandbox escrow APIs.
- API webhook endpoints enforce HMAC-SHA256 signature verification.
- Zero PII (Personally Identifiable Information) is included in synthetic CSV data layers.
