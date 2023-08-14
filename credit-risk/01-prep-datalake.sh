#! /bin/bash

mkdir -p data

#download data
kaggle competitions download -c home-credit-default-risk -p data

#unzip
unzip data/home-credit-default-risk.zip -d data
rm data/home-credit-default-risk.zip 

#create bucket
BUCKET_NAME=bpk-credit-risk-demo
aws s3 mb "s3://$BUCKET_NAME"

#upload bureau data
aws s3 cp data/bureau.csv "s3://$BUCKET_NAME/bureau/bureau.csv"
aws s3 cp data/bureau_balance.csv "s3://$BUCKET_NAME/bureau/bureau_balance.csv"

#upload applications
aws s3 cp data/application_train.csv "s3://$BUCKET_NAME/applications/application.csv"
aws s3 cp data/previous_application.csv "s3://$BUCKET_NAME/applications/previous_application.csv"

#pos payments
aws s3 cp data/POS_CASH_balance.csv "s3://$BUCKET_NAME/payments/POS_CASH_balance.csv"
aws s3 cp data/installments_payments.csv "s3://$BUCKET_NAME/payments/installments_payments.csv"
aws s3 cp data/credit_card_balance.csv "s3://$BUCKET_NAME/payments/credit_card_balance.csv"
