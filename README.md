```
MIT License

Copyright (c) 2026 Diwas Khatri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

# Braintree Auth & Tokenization Script

> A Python-based automation script for Braintree payment gateway authentication, client token retrieval, and credit card tokenization on WooCommerce websites.

**Made By Diwas Khatri**

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Step-by-Step Guide](#step-by-step-guide)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Disclaimer](#disclaimer)
- [Author](#author)

---

## Overview

This script automates the complete Braintree payment method flow on WooCommerce-based websites. It performs:

1. **Login** to a WooCommerce account
2. **Fetch** the add-payment-method page
3. **Extract** the Braintree client token (JWT)
4. **Decode** the token to obtain the authorization fingerprint
5. **Tokenize** a credit card via Braintree GraphQL API
6. **Submit** the payment method to save the card

The script is designed to work with the **WooCommerce Braintree Gateway** plugin.

---

## Features

- Dynamic nonce extraction - No hardcoded nonces
- Session persistence - Uses `requests.Session()` for cookies
- Dynamic Bearer token - Fetches JWT from server, no hardcoding
- Base64 decoding - Extracts `authorizationFingerprint` from client token
- GraphQL tokenization - Direct Braintree API integration
- Decline detection - Parses real decline reasons from response
- Clean output - Only prints Auth Bearer, Token CC, and Decline message
- Raw implementation - Step-by-step, easy to modify

---

## How It Works

```
STEP 1: GET  /my-account/          -> Fetch login nonce
STEP 2: POST /my-account/          -> Submit login
STEP 3: GET  /add-payment-method/  -> Fetch nonces + form
STEP 4: POST /admin-ajax.php       -> Get client token
STEP 5: POST Braintree GraphQL     -> Tokenize card
STEP 6: POST /add-payment-method/  -> Submit payment method
```

### Detailed Flow

| Step | Request | Purpose |
|------|---------|---------|
| 1 | GET /my-account/ | Loads login page, extracts login nonce |
| 2 | POST /my-account/ | Submits credentials, establishes session |
| 3 | GET /add-payment-method/ | Fetches form, extracts nonces |
| 4 | POST /admin-ajax.php | Exchanges nonce for client token (JWT) |
| 5 | POST Braintree GraphQL | Tokenizes credit card |
| 6 | POST /add-payment-method/ | Submits tokenized nonce |

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.8 or higher |
| requests | 2.28+ |
| beautifulsoup4 | 4.11+ |
| Internet connection | Required |
| WooCommerce account | Valid credentials |

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/diwaskhatri07/braintree-auth.git
cd braintree-auth
```

### Step 2: Install Python

Make sure Python 3.8+ is installed. Verify with:

```bash
python --version
```

### Step 3: Create Virtual Environment (Recommended)

Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install requests beautifulsoup4
```

Or with requirements.txt:

```bash
pip install -r requirements.txt
```

### Step 5: Verify Installation

```bash
python -c "import requests, bs4; print('All dependencies installed')"
```

Expected output:

```
All dependencies installed
```

---

## Configuration

Open `b3.py` and update the following variables.

### 1. Target Website

```python
BASE_URL = 'https://www.your-target-site.com'
```

### 2. Login Credentials

```python
data_1 = {
    'username': 'your_username',
    'password': 'your_password',
    'rememberme': 'forever',
    'woocommerce-login-nonce': lnonce,
    '_wp_http_referer': '/my-account/',
    'login': 'Log in',
}
```

### 3. Card Details

```python
json_data = {
    'variables': {
        'input': {
            'creditCard': {
                'number': '4496130001514478',
                'expirationMonth': '05',
                'expirationYear': '2029',
                'cvv': '575',
            },
            'options': {'validate': False},
        },
    },
}
```

---

## Usage

### Basic Run

```bash
python b3.py
```

### Windows PowerShell (Path with Spaces)

```powershell
python "C:\Users\YourName\Desktop\b3 auth\tutorials\b3.py"
```

### With Output Saved to File

```bash
python b3.py > output.txt 2>&1
```

### Expected Output

```
200
Here is Token Nonce - tokencc_bh_7ts6wz_p3ywdp_wxwpny_qjpxqc_s62
Here is Woo Nonce - 3cd0d2b386
Here is barrer - eyJraWQiOiIyMDE4MDQyNjE2LXByb2R1Y3Rpb24i...
DECLINED: Status code 2047: Call Issuer
```

### Success Output

```
Here is Token Nonce - tokencc_bh_xxxxxxxxxxxxx
Here is Woo Nonce - xxxxxxxxxxxx
Here is barrer - eyJraWQiOiIyMDE4MDQyNjE2...
Payment method added successfully
```

---

## Project Structure

```
braintree-auth/
|
├── b3.py                  # Main script
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
|
├── tutorials/
│   └── b3.py             # Tutorial version with detailed comments
|
└── examples/
    ├── kaffn8.py         # SkyVerge plugin example
    └── boltlaundry.py    # Payment Plugins example
```

### requirements.txt

```txt
requests>=2.28.0
beautifulsoup4>=4.11.0
```

---

## Step-by-Step Guide

### Step 1: Understand Braintree Flow

Braintree uses a client token (JWT) that contains the `authorizationFingerprint`. This fingerprint is required to call the GraphQL tokenization API.

```
Client Token (JWT, base64)
    -> decode
authorizationFingerprint
    -> use in Bearer header
Braintree GraphQL API
    -> returns
Payment Method Nonce
    -> submit to WooCommerce
Card saved
```

### Step 2: Login and Get Session

```python
session = requests.Session()
r1 = session.get(f'{BASE}/my-account/', headers=headers_1)
lnonce = BeautifulSoup(r1.text, 'html.parser').find(
    'input', {'name': 'woocommerce-login-nonce'}
)['value']
```

### Step 3: Extract Braintree Client Token

The client token is fetched via AJAX:

```python
data_4 = {
    'action': 'wc_braintree_credit_card_get_client_token',
    'nonce': client_token_nonce,
}
r4 = session.post(f'{BASE}/wp-admin/admin-ajax.php', headers=headers_4, data=data_4)
CLIENT_TOKEN = r4.json()['data']
```

### Step 4: Decode the Client Token

```python
token_data = json.loads(base64.b64decode(CLIENT_TOKEN))
AUTH_FINGERPRINT = token_data['authorizationFingerprint']
```

### Step 5: Tokenize Credit Card

```python
r5 = session.post(
    'https://payments.braintree-api.com/graphql',
    headers={'Authorization': f'Bearer {AUTH_FINGERPRINT}'},
    json=json_data,
)
token = r5.json()['data']['tokenizeCreditCard']['token']
```

### Step 6: Submit Payment Method

```python
data_6 = [
    ('payment_method', 'braintree_credit_card'),
    ('wc_braintree_credit_card_payment_nonce', token),
    ('woocommerce-add-payment-method-nonce', woo_nonce),
    # ...
]
r6 = session.post(f'{BASE}/my-account/add-payment-method/', data=data_6)
```

### Step 7: Parse Result

```python
if "payment method added" in r6.text.lower():
    print("Payment method added successfully")
else:
    m = re.search(r'Status code \d+:[^<."]+', r6.text)
    print(f"DECLINED: {m.group(0) if m else 'Unknown'}")
```

---

## Troubleshooting

### Issue: SyntaxError closing parenthesis does not match

Cause: Missing `)` in tuple.

Fix:

```python
# Wrong
('key', value,

# Correct
('key', value),
```

### Issue: Could not find login nonce

Cause: Site structure changed or blocked.

Fix: Update user-agent and check the login page HTML manually.

### Issue: Authentication credentials are invalid

Cause: Using raw client token instead of authorizationFingerprint in GraphQL.

Fix:

```python
# Wrong
'authorization': f'Bearer {CLIENT_TOKEN}',

# Correct
'authorization': f'Bearer {AUTH_FINGERPRINT}',
```

### Issue: Status code 2047 Call Issuer

Cause: Test card that always declines.

Fix: Use a real card or different test card.

### Issue: ModuleNotFoundError No module named requests

Fix:

```bash
pip install requests beautifulsoup4
```

### Issue: PowerShell Path Error with Spaces

Fix: Use quotes:

```powershell
cd "C:\Users\Diwas\Desktop\b3 auth\tutorials"
```

---

## FAQ

Q: Can I use this on any WooCommerce site?

A: Only sites using the WooCommerce Braintree Gateway plugin.

Q: Do I need a real card?

A: For testing, no. For actual card saving, yes.

Q: Why do I get Call Issuer decline?

A: That is a test card behavior. Try a different card.

Q: Is this legal?

A: Only use on your own accounts or with explicit permission.

Q: Which Braintree plugin does this support?

A: SkyVerge WooCommerce Braintree Gateway and Payment Plugins Braintree.

---

## Disclaimer

This project is for educational purposes only. The author is not responsible for any misuse, unauthorized access, or illegal activity performed with this tool.

Rules:

- Use on your own accounts
- Use for security research with permission
- Use for learning Braintree integration
- Do NOT use for unauthorized access
- Do NOT use for fraud
- Do NOT use to harm others

---

## Author

**Diwas Khatri**

- GitHub: https://github.com/diwaskhatri07
- Email: diwaskhatri935@gmail.com

---

## Contributing

1. Fork the repository
2. Create your feature branch

```bash
git checkout -b feature/AmazingFeature
```

3. Commit your changes

```bash
git commit -m "Add some AmazingFeature"
```

4. Push to branch

```bash
git push origin feature/AmazingFeature
```

5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgements

- Braintree for the payment API
- WooCommerce for the e-commerce platform
- Requests library
- BeautifulSoup for HTML parsing

---

## Show Your Support

If this project helped you, please give it a star on GitHub.

---

**Made with love by Diwas Khatri**
