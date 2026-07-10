#!/bin/sh
# Update Mi6 token in both .env and config.yaml
sed -i 's/^TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=8743263149:AAFr9ibTKi3VQ1o6xn-mNFn7QC4EzWKGhcA/' /root/.hermes/.env
sed -i 's/bot_token: .*/bot_token: 8743263149:AAFr9ibTKi3VQ1o6xn-mNFn7QC4EzWKGhcA/' /root/.hermes/config.yaml
echo TOKEN_UPDATED
grep TELEGRAM_BOT /root/.hermes/.env
grep bot_token /root/.hermes/config.yaml
