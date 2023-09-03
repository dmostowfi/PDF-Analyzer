# PDF-Analyzer
Event-driven cloud application that analyzes a PDF's text when uploaded and writes results to a .txt file

## Project Details
- Context: Class project for CS-310: Scalable Software Architectures [(syllabus)](https://www.dropbox.com/s/ltwtt7p91qutv5t/cs310-Syllabus.pdf?dl=0) with Prof. Joe Hummel at Northwestern University's McCormick School of Engineering.
- Purpose: Design an event-driven, serverless cloud application using AWS Lambda functions.

## Software Architecture
- AWS S3 (Simple Storage Service): object storage; uploading files triggers the call to Lambda function
- AWS Lambda: Python function, called when a PDF is uploaded to AWS (event-driven)
- AWS API Gateway: AWS-managed web-server

Features 
- Lambda function opens a PDF, iterates through and extracts numeric text from each page, does a computation, writes results to .txt file and uploads file to S3 bucket
