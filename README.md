# Cryptocurrency-API

Backend app for cryptocurrency transactions built with Django and Django REST Framework.  
It's using Coingecko`s API for checking current prices of cryptocurrencies.  
Contains documentation created with Swagger on endpoint:
```
/api/docs/
```
Superuser:
```
user: matt
psw: 1234
```
Register endpoint:
```
api/register/
```
Users have their own Wallet and Balance which are created with POST requests on endpoints:
```
/api/walletid/
/api/balance/
```
Users are able to buy/sell/send cryptos with POST requests on endpoints:
```
api/cryptocurrency/
api/cryptocurrencybuy/
api/cryptocurrencysell/
```
If everything is valid there are automatically created Transactions model with all details of transaction.
