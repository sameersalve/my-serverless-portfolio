import json
import boto3
import io
from botocore.client import Config
import zipfile
import mimetypes

def lambda_handler(event, context):
   
    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')
    
    topic = sns.Topic('arn:aws:sns:us-east-1:709484259773:deployPortfolioTopic')
    try:
        portfolio_bucket = s3.Bucket('portfolio.sameersalve.info')
        build_bucket = s3.Bucket('portfoliobuild.sameersalve.info')
        
        portfolio_zip = io.BytesIO()
        build_bucket.download_fileobj('portfoliobuild.zip',portfolio_zip)
        
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm,ExtraArgs={'ContentType':mimetypes.guess_type(nm )[0]},Callback=None, Config=None)
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
    
        print("Job Done")
        topic.publish(Subject="Portfolio Deployed",Message='Portfolio deployed succesfully')
        
        
    except:
        topic.publish(Subject='Portfolio Deployed Failed',Message='Portfolio was not deployed successfully')
        raise
    
    return "Hello from Lambda"