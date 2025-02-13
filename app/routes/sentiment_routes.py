"""
This module contains the routes for the sentiment endpoint.
"""
import json
from flask_restx import Namespace, Resource, fields
from flask import request

import app.models.deep_seek
# Services
from app.services.sentiment_service import SentimentService

service = SentimentService()

def process_transcript(transcript: str) -> str:
    json_transcript = json.loads(transcript)
    call_transcript = "\n".join(json_transcript.get("call_transcript", []))
    return str(call_transcript)

def register_routes(api):
    # Define the model for the sentiment analysis request body
    sentiment_analyze_request_model = api.model('SentimentAnalyzeRequestModel', {
        'text': fields.String(required=True, description='Input text for sentiment analysis.', example='I love this product!')
    })

    sentiment_analyze_bad_request_model = api.model('SentimentAnalyzeBadRequestModel', {
        'status': fields.String(required=True, description='The status of the response', example='error'),
        'error': fields.String(required=True, description='The error message', example='text is required'),
        'data': fields.Raw(description='Data field will be null for error responses', example=None)
    })

    sentiment_analyze_internal_server_error_model = api.model('SentimentAnalyzeInternalServerErrorModel', {
        'status': fields.String(required=True, description='The status of the response', example='error'),
        'error': fields.String(required=True, description='The error message', example='An unexpected error occurred during sentiment analysis.'),
        'data': fields.Raw(description='Data field will be null for error responses', example=None)
    })

    sentiment_analyze_success_model = api.model('SentimentAnalyzeSuccessModel', {
        'status': fields.String(required=True, description='The status of the response', example='success'),
        'data': fields.Nested(api.model('SentimentAnalyzeDataModel', {
            'label': fields.String(required=True, description='Predicted sentiment label.', enum=['POS', 'NEG', 'NEU'], example='POS'),
            'confidence': fields.Float(required=True, description='Confidence score of the prediction.', example=0.95)
        }))  # Embed the data model
    })

    # Define the endpoint for the summarize of a text.
    @api.route('/callquality')
    class CallQuality(Resource):
        @api.doc(description="Call Quality")
        @api.expect(sentiment_analyze_request_model)  # Use the model for request validation
        @api.response(200, 'Success', sentiment_analyze_success_model)
        @api.response(400, 'Bad Request', sentiment_analyze_bad_request_model)
        @api.response(500, 'Internal Server Error', sentiment_analyze_internal_server_error_model)
        def post(self):
            """
            Endpoint to analyze sentiment of a text.
                - text (str): Input text for sentiment analysis.
            """
            try:
                encoding = 'utf-8'
                # print(str(request.data,encoding))
                text = process_transcript(str(request.data, encoding))

                if not text:
                    return {
                        'status': 'error',
                        'error': 'text is required.',
                        'data': None
                    }, 400

                # Call the service to analyze the sentiment of the text
                result = app.models.deep_seek.transcript_quality_analyzer(text)

                if 'error' in result:
                    return {
                        'status': 'error',
                        'error': result['error'],
                        'data': None
                    }, 500  # Internal Server Error

                # Return the predicted label and confidence score
                return {
                    'status': 'success',
                    'data': {
                        'label': result,
                        # 'confidence': result['confidence']
                    }
                }

            except Exception as e:
                print(f"[error] [Route Layer] [SentimentAnalyze] [post] An error occurred: {str(e)}")
                return {
                    'status': 'error',
                    "error": 'An unexpected error occurred while processing the request.',  # Generic error message
                    'data': None
                }, 500  # Internal Server Error

    # Define the endpoint for the summarize of a text.
    @api.route('/callsummarize')
    class CallSummariser(Resource):
        @api.doc(description="Call Summariser")
        @api.expect(sentiment_analyze_request_model)  # Use the model for request validation
        @api.response(200, 'Success', sentiment_analyze_success_model)
        @api.response(400, 'Bad Request', sentiment_analyze_bad_request_model)
        @api.response(500, 'Internal Server Error', sentiment_analyze_internal_server_error_model)
        def post(self):
            """
            Endpoint to analyze sentiment of a text.
                - text (str): Input text for sentiment analysis.
            """
            try:
                # Parse the request body
                encoding = 'utf-8'
                #print(str(request.data,encoding))
                text = process_transcript(str(request.data,encoding))
                #data=request

                #text = #data['call_transcript']
                #text_1=process_transcript(text)
                #print(text)

                if text=='':
                    return {
                        'status': 'error',
                        'error': 'text is required.',
                        'data': None
                    }, 400

                # Call the service to analyze the sentiment of the text
                result = app.models.deep_seek.transcript_summariser(text)
                #print(result)

                if 'error' in result:
                    return {
                        'status': 'error',
                        'error': result['error'],
                        'data': None
                    }, 500  # Internal Server Error

                # Return the predicted label and confidence score
                return {
                    'status': 'success',
                    'data': {
                        'label': result,
                        #'confidence': result['confidence']
                    }
                }

            except Exception as e:
                print(f"[error] [Route Layer] [SentimentAnalyze] [post] An error occurred: {str(e)}")
                return {
                    'status': 'error',
                    "error": 'An unexpected error occurred while processing the request.',  # Generic error message
                    'data': None
                }, 500  # Internal Server Error
    # Define the endpoint for the Analyze sentiment of a text.
    @api.route('/analyze') 
    class SentimentAnalyze(Resource):
        @api.doc(description="Analyze sentiment of a text.")
        @api.expect(sentiment_analyze_request_model)  # Use the model for request validation
        @api.response(200, 'Success', sentiment_analyze_success_model)
        @api.response(400, 'Bad Request', sentiment_analyze_bad_request_model)
        @api.response(500, 'Internal Server Error', sentiment_analyze_internal_server_error_model)
        def post(self):
            """
            Endpoint to analyze sentiment of a text.
                - text (str): Input text for sentiment analysis.
            """
            try:
                # Parse the request body
                data = request.json

                text = data.get('text')


                if not text:
                    return {
                        'status': 'error',
                        'error': 'text is required.',
                        'data': None
                    }, 400
                
                # Call the service to analyze the sentiment of the text
                result = service.analyze(text)

                if 'error' in result:
                    return {
                        'status': 'error',
                        'error': result['error'],
                        'data': None
                    }, 500 # Internal Server Error
                
                # Return the predicted label and confidence score
                return {
                    'status': 'success',
                    'data': {
                        'label': result['label'],
                        'confidence': result['confidence']
                    }
                }
            
            except Exception as e:
                print(f"[error] [Route Layer] [SentimentAnalyze] [post] An error occurred: {str(e)}")
                return {
                    'status': 'error',
                    "error": 'An unexpected error occurred while processing the request.', # Generic error message
                    'data': None
                }, 500 # Internal Server Error
            
# Define the namespace for the sentiment endpoint
api = Namespace('Sentiment', description='Sentiment Operations')

# Register the routes
register_routes(api)