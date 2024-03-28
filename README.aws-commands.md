# AWS CLI commands



## Localstack access

Add enpoint-url modifier to aws cli commands to indicate the endpoint API.

Localstack Community does not persists data :-(

Every instance of a container is assigned to a region.


## S3

### Create bucket

By now only can be created on us-east-1

'''
aws --endpoint-url=http://localhost:4566 --region us-east-1 s3api create-bucket --bucket test-bucket
'''

### View buckets

'''
aws --endpoint-url=http://localhost:4566 --region eu-west-1 s3 ls
'''


## SQS

### View queues

'''
aws --endpoint-url=http://localhost:4566 --region eu-west-1 sqs list-queues
'''

### Create queue

'''
aws --endpoint-url=http://localhost:4566 --region eu-west-1 sqs create-queue --queue-name CaffeineHub
'''

Response:

'''
{
    "QueueUrls": [
        "http://sqs.eu-west-1.localhost.localstack.cloud:4566/000000000000/CaffeineHub"
    ]
}
'''


## DynamoDB

Do not needed. Table created authomatically if it does not exists.


### Create table

Celery table

'''
aws --endpoint-url=http://localhost:4566 --region eu-west-1 dynamodb create-table \
    --table-name celery \
    --attribute-definitions AttributeName=id,AttributeType=N \
    --key-schema AttributeName=id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
'''

### List tables

'''
aws --endpoint-url=http://localhost:4566 --region eu-west-1 dynamodb list-tables
'''


### Delete table

'''
aws --endpoint-url=http://localhost:4566 --region eu-west-1 dynamodb delete-table --table-name my_table
'''

### Scan table

'''
aws --endpoint-url=http://localhost:4566 --region eu-west-1 dynamodb scan --table-name my_table
'''

### Describe table

'''
aws --endpoint-url=http://localhost:4566 dynamodb describe-table --table-name my_table
'''



## MACOS

### Problems with pycurl

Macos does not include openssl by default and it is needed to installing manually and reinstall Pycurl.
'''
pip remove pipcurl
brew install openssl
brew info openssl
* Get path
PYCURL_SSL_LIBRARY=openssl LDFLAGS="-L/opt/homebrew/opt/openssl@3/lib" CPPFLAGS="-I/opt/homebrew/opt/openssl@3/include" pip install --no-cache-dir pycurl
'''


https://github.com/celery/celery/issues/4654

Extract from: https://cscheng.info/2018/01/26/installing-pycurl-on-macos-high-sierra.html

Apparently, pip (version 10.0.1) installing the latest version of PycURL (version 7.43.0.2) will immediately fail on macOS High Sierra:

__main__.ConfigurationError: Curl is configured to use SSL, but we have not been able to determine which SSL backend it is using. Please see PycURL documentation for how to specify the SSL backend manually.
Use the following command to install PycURL correctly:

$ PYCURL_SSL_LIBRARY=openssl LDFLAGS="-L/usr/local/opt/openssl/lib" CPPFLAGS="-I/usr/local/opt/openssl/include" pip install --no-cache-dir pycurl

If you already have installed OpenSSL earlier via Homebrew, you can find out the paths for LDFLAGS and CPPFLAGS via:

$ brew info openssl



## Cognito

### Login

Response

```
http://localhost:4200/#id_token=eyJraWQiOiJZbEFQcjZiRzNaZk82b1o2YUFvc295aCtTd1dYMEJON3M5V0JjNG5qbTJvPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiTGdGOFFCcmVQTkE0UWs2U2ZUeGFLUSIsInN1YiI6IjJmNGJkOTFhLWY0NWEtNDYzOS1hMzkzLTRhYWYxOGE1MDk4MSIsImNvZ25pdG86Z3JvdXBzIjpbImN1c3RvbWVyIl0sImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS13ZXN0LTEuYW1hem9uYXdzLmNvbVwvZXUtd2VzdC0xX1N0dk5xbnVMdiIsImNvZ25pdG86dXNlcm5hbWUiOiJ0ZXN0ZXIiLCJhdWQiOiI1cDZ2bG50OHU4czFsMWI2YjdoYzJ2bnVsdiIsImV2ZW50X2lkIjoiZWEzNDU2ZmUtZGQwNi00YTJlLWJlOGYtNjgwMDYyYzgwMTFjIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3MTE2NjM3MTEsImV4cCI6MTcxMTY2NzMxMSwiaWF0IjoxNzExNjYzNzExLCJqdGkiOiIxODAzNzkyZS1lOThhLTQwMzEtYjhhOC1iNmEzYzVlODY0OTkiLCJlbWFpbCI6InRlc3RlckBtYWlsLmNvbSJ9.N9DZyZYCnfFS9eeIyHUiscrsn5Yce168rUeD28eVRu3Hg_ucea_VIC3COnBFe1rSgOjZZ-evWyYVYsxS-IFzWTGCAAbrOkCivZTQ85vTpjlStwDVLQ0rUjqIC5JEkRyqAc_Dj2jHPL3emV2Y9rti7PWs_0FZ3vxwCzf-ndtqDLSvGGGhC8cZPX8B5FLH4ZERAdTPhkXUAtO4Tovsho0JSieWn58vlIbwmtPD0Aov2CX415cYwxtrIpbAZQj6KLLbx6TDcUPGMByzDNWMPni6tdirfSjI5ShM_P_IpPOoAFGIz74fo5JNxorCwdfwQ2UBhtbE9LXWVXbfV5ZOKkljlQ&access_token=eyJraWQiOiI1YlJPR0g4S1V2U3JnRU85VXh1MGdyekJtT1c2RlpMVW5WdjcyczI2VXdBPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIyZjRiZDkxYS1mNDVhLTQ2MzktYTM5My00YWFmMThhNTA5ODEiLCJjb2duaXRvOmdyb3VwcyI6WyJjdXN0b21lciJdLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9TdHZOcW51THYiLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiI1cDZ2bG50OHU4czFsMWI2YjdoYzJ2bnVsdiIsImV2ZW50X2lkIjoiZWEzNDU2ZmUtZGQwNi00YTJlLWJlOGYtNjgwMDYyYzgwMTFjIiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJwaG9uZSBvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImF1dGhfdGltZSI6MTcxMTY2MzcxMSwiZXhwIjoxNzExNjY3MzExLCJpYXQiOjE3MTE2NjM3MTEsImp0aSI6IjM1ZmVjMjhmLTA3YTctNDFjNi04YzNjLWQ0MzFhNjAyOTliOSIsInVzZXJuYW1lIjoidGVzdGVyIn0.pMuWJAbK4JUnRdpSaDP6ohnb0goHzAed1qZc6krejvEHPLzd63MUtn1OorCEhO92Gl0NRj9nEc2i4_8V_rUsAbX4j_JXowd09HtQkEGzie4jJzdQH6xolSOKMmRv6LQjWW9iA6G6vDGvI_3w247t1feOCm5mZJIMXGZl5qoz7eQhBGlN1lRQm5F2-Inuw9VKyH5VzxjN74p9eYNtrOkJQE9-jH2aSAYfrMP36Z60iCs0z4H0pYD3YvOMZ9iidXlfwXNy0mdavVmb1Ex9yiurt-merjHLUH0wY804mQ0ps6KR6v4xOF7IWmubCZ_zi2GzGvXFz7rNWxmJfN2qNscDAg&expires_in=3600&token_type=Bearer
```
