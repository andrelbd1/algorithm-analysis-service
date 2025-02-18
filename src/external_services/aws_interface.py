import boto3
import gzip
import json
from io import BytesIO
from src.common import Singleton


class AWS(metaclass=Singleton):

    @staticmethod
    def get_messages_from_queue(amount: int, params: dict) -> list:
        """
        Retrieve a specified number of messages from an AWS SQS queue.

        This method connects to an SQS queue using the provided AWS credentials
        and attempts to fetch messages in batches of up to 10 (SQS limit) until the
        requested amount is retrieved or no more messages are available.

        Args:
            amount (int): The total number of messages to retrieve from the queue.
            params (dict): A dictionary containing the following keys:
                - `aws_access_key_id` (str): AWS access key ID for authentication.
                - `aws_secret_access_key` (str): AWS secret access key for authentication.
                - `sqs_queue_url` (str): The URL of the SQS queue to receive messages from.
                - `sqs_visibility_timeout` (int, optional): The duration (in seconds) the received messages are hidden
                from subsequent retrieve requests. Default is 900 seconds.
                - `sqs_wait_time` (int, optional): The duration (in seconds) for which the call waits for a message
                to arrive in the queue before returning. Default is 10 seconds.

        Returns:
            list: A list of messages retrieved from the SQS queue. Each message is represented as a dictionary
            containing message attributes and body.

        Raises:
            boto3.exceptions.Boto3Error: If there is an issue connecting to SQS or receiving messages.

        Example:
            messages = get_messages_from_queue(20, {
                "aws_access_key_id": "your_access_key",
                "aws_secret_access_key": "your_secret_key",
                "sqs_queue_url": "https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue"
            })
        """
        aws_access_key_id = params.get('aws_access_key_id')
        aws_secret_access_key = params.get('aws_secret_access_key')
        region_name = params.get('aws_region')
        sqs_queue_url = params.get('sqs_queue_url')
        sqs_visibility_timeout = params.get('sqs_visibility_timeout', 900)
        sqs_wait_time = params.get('sqs_wait_time', 10)

        sqs_client = boto3.client('sqs', region_name=region_name,
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)

        all_messages = []
        curr_amount = 0
        while curr_amount < amount:
            res = sqs_client.receive_message(QueueUrl=sqs_queue_url,
                                             MaxNumberOfMessages=min(amount-curr_amount, 10),
                                             VisibilityTimeout=sqs_visibility_timeout,
                                             WaitTimeSeconds=sqs_wait_time)
            curr_messages = res.get("Messages", [])
            if not curr_messages:
                break
            all_messages.extend(curr_messages)
            curr_amount += len(curr_messages)

        return all_messages

    @staticmethod
    def load_json_file_from_storage(name: str, params: dict) -> dict:
        """
        Load a JSON file from an AWS S3 bucket.

        This method retrieves a JSON file from an S3 bucket and parses its content. If the file
        is compressed with gzip (`.gz` extension), it will be decompressed before parsing.

        Args:
            name (str): The name of the file to be loaded, including its extension.
            params (dict): A dictionary containing the following keys:
                - `aws_access_key_id` (str): AWS access key ID for authentication.
                - `aws_secret_access_key` (str): AWS secret access key for authentication.
                - `bucket` (str): The name of the S3 bucket where the file is stored.
                - `file_path` (str, optional): The directory path in the S3 bucket where the file is located.

        Returns:
            dict: The parsed content of the JSON file as a Python dictionary.

        Raises:
            boto3.exceptions.Boto3Error: If there is an error with the S3 connection or file retrieval.
            json.JSONDecodeError: If the file content cannot be parsed as JSON.

        Example:
            load_json_file_from_storage("data.json", {
                "aws_access_key_id": "your_access_key",
                "aws_secret_access_key": "your_secret_key",
                "bucket": "my-bucket"
            })

            load_json_file_from_storage("data.json.gz", {
                "aws_access_key_id": "your_access_key",
                "aws_secret_access_key": "your_secret_key",
                "bucket": "my-bucket"
            })
        """
        aws_access_key_id = params.get('aws_access_key_id')
        aws_secret_access_key = params.get('aws_secret_access_key')
        file_path = f"{params.get('file_path')}/{name}" if params.get('file_path') else name
        bucket = params.get('bucket')
        compressed = name.split('.')[-1]

        s3_resource = boto3.resource('s3',
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key)

        obj = s3_resource.Object(bucket, file_path)

        match compressed:
            case 'gz':
                file_content = obj.get()['Body'].read()
                with gzip.GzipFile(fileobj=BytesIO(file_content)) as gz_file:
                    decoded_data = gz_file.read().decode('utf-8')
                    data = json.loads(decoded_data)
            case _:
                file_content = obj.get()['Body'].read().decode('utf-8')
                data = json.loads(file_content)

        return data

    @staticmethod
    def remove_file_from_storage(name: str, params: dict) -> None:
        """
        Remove a file from an AWS S3 bucket.

        This method deletes a specified file from an S3 bucket using the provided AWS credentials.

        Args:
            name (str): The name of the file to be deleted.
            params (dict): A dictionary containing the following keys:
                - `aws_access_key_id` (str): AWS access key ID for authentication.
                - `aws_secret_access_key` (str): AWS secret access key for authentication.
                - `bucket` (str): The name of the S3 bucket where the file resides.
                - `file_path` (str, optional): The directory path in the S3 bucket where the file is stored.
                If not provided, the file is assumed to be in the root of the bucket.

        Returns:
            None

        Raises:
            boto3.exceptions.Boto3Error: If there is an error during the deletion process.

        Example:
            remove_file_from_storage("example.txt", {
                "aws_access_key_id": "your_access_key",
                "aws_secret_access_key": "your_secret_key",
                "bucket": "my-bucket",
                "file_path": "documents.json"
            })
        """
        aws_access_key_id = params.get('aws_access_key_id')
        aws_secret_access_key = params.get('aws_secret_access_key')
        file_path = f"{params.get('file_path')}/{name}" if params.get('file_path') else name
        bucket = params.get('bucket')
        s3_resource = boto3.resource('s3',
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key)

        s3_resource.Object(bucket, file_path).delete()

    @staticmethod
    def remove_messages_from_queue(messages: list, params: dict) -> None:
        """
        Remove a batch of messages from an AWS SQS queue.

        This method deletes messages from an SQS queue in batches of up to 10 messages at a time,
        as required by the SQS `delete_message_batch` API. The messages should include both
        `MessageId` and `ReceiptHandle`.

        Args:
            messages (list): A list of messages to be deleted from the SQS queue. Each message
                should be a dictionary containing:
                - `MessageId` (str): The unique identifier for the message.
                - `ReceiptHandle` (str): The receipt handle used for deletion.
            params (dict): A dictionary containing the following keys:
                - `aws_access_key_id` (str): AWS access key ID for authentication.
                - `aws_secret_access_key` (str): AWS secret access key for authentication.
                - `sqs_queue_url` (str): The URL of the SQS queue from which messages will be deleted.

        Returns:
            None

        Raises:
            boto3.exceptions.Boto3Error: If there is an issue with the SQS client or deletion process.

        Example:
            remove_messages_from_queue(
                messages=[
                    {'MessageId': '123', 'ReceiptHandle': 'abc123'},
                    {'MessageId': '456', 'ReceiptHandle': 'def456'}
                ],
                params={
                    'aws_access_key_id': 'your_access_key',
                    'aws_secret_access_key': 'your_secret_key',
                    'sqs_queue_url': 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'
                }
            )
        """
        aws_access_key_id = params.get('aws_access_key_id')
        aws_secret_access_key = params.get('aws_secret_access_key')
        region_name = params.get('aws_region')
        sqs_queue_url = params.get('sqs_queue_url')

        sqs_client = boto3.client('sqs', region_name=region_name,
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)
        batch_size = 10  # SQS allows max 10 messages per delete batch
        for i in range(0, len(messages), batch_size):
            batch = messages[i:i+batch_size]
            entries = [{'Id': m['MessageId'], 'ReceiptHandle': m['ReceiptHandle']} for m in batch]
            sqs_client.delete_message_batch(QueueUrl=sqs_queue_url,
                                            Entries=entries)

    @staticmethod
    def save_json_file_to_storage(json_content: str, name: str, params: dict) -> str:
        """
        Compress and upload a JSON file to an AWS S3 bucket.

        This method compresses the provided JSON content using Gzip and uploads it to the specified
        S3 bucket. The file path can be customized using the `file_path` parameter.

        Args:
            json_content (str): The JSON content to be compressed and uploaded, represented as a string.
            name (str): The name of the file to be created in the S3 bucket.
            params (dict): A dictionary containing the following keys:
                - `aws_access_key_id` (str): AWS access key ID for authentication.
                - `aws_secret_access_key` (str): AWS secret access key for authentication.
                - `file_path` (str, optional): The folder path where the file will be stored in the bucket.
                - `bucket` (str): The name of the S3 bucket where the file will be uploaded.

        Returns:
            str: The full S3 URI of the uploaded file.

        Raises:
            boto3.exceptions.Boto3Error: If an error occurs during the S3 upload process.

        Example:
            save_json_file_to_storage(
                json_content='{"key": "value"}',
                name='data.json.gz',
                params={
                    'aws_access_key_id': 'your_access_key',
                    'aws_secret_access_key': 'your_secret_key',
                    'file_path': 'folder/subfolder',
                    'bucket': 'my-s3-bucket'
                }
            )
        """
        aws_access_key_id = params.get('aws_access_key_id')
        aws_secret_access_key = params.get('aws_secret_access_key')
        file_path = f"{params.get('file_path')}/{name}" if params.get('file_path') else name
        bucket = params.get('bucket')
        file_buffer = BytesIO()
        with gzip.GzipFile(fileobj=file_buffer, mode='w') as gz_file:
            gz_file.write(json_content.encode('utf-8'))
        file_buffer.seek(0)

        s3_resource = boto3.resource('s3',
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key)

        s3_resource.Object(bucket, file_path).put(Body=file_buffer.getvalue())
        return f's3://{bucket}/{file_path}'
