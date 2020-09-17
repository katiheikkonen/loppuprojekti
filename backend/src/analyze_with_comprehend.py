import json

#  S3 laukaisee tämän Lambdan
#  Lambda lähettää saadun palautteen Amazon Comprehendille analysoitavaksi Sentimental Analysis-työkalun kautta
import boto3

#s3 = boto3.client("s3")
comprehend = boto3.client("comprehend")

def sentimental_analysis(event, context):
    message = "The end of the cord broke off in my phone after the 4th use." \
    "Thought it might be a just a defective plug, but I looked at recent reviews and others are having same issues."\
     "I am sending the cords back and buy different brand."

    # paragraph-kohtaan vielä muutos, että haetaan asiakaspalaute s3:sta, alla yksi esimerkki

    # bucket = "bucket-name"
    # key = "filename.txt"
    # file = s3.get_object(Bucket=bucket, Key=key)
    # paragraph = str(file['Body'].read())

    # Extracting sentiments using comprehend
    reply = comprehend.detect_sentiment(Text=message, LanguageCode="en")

    #Poimitaan Comprehendista tulleesta datasta halutut datakentät:
    sentiment = reply['Sentiment']
    positive = reply['SentimentScore']['Positive']
    negative = reply['SentimentScore']['Negative']
    neutral = reply['SentimentScore']['Neutral']
    mixed = reply['SentimentScore']['Mixed']
    time = mixed = reply['ResponseMetadata']['HTTPHeaders']['date']

    # + potentiaalista debugausta varten retry-attemps kenttä:
    retry_attemps = reply['ResponseMetadata']['RetryAttempts']

    analysis = {
        "sentiment":sentiment,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "mixed":mixed,
        "time":time
    }

    return {"body":json.dumps(analysis)}