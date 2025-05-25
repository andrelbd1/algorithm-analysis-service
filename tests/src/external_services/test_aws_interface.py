import gzip
from math import ceil
from io import BytesIO

import mock

from src.common import Singleton
from src.external_services.aws_interface import AWS
from tests import BaseTestClass


class TestAWS(BaseTestClass):

    def setUp(self):
        Singleton.drop()

    @property
    def __cloud(self):
        return AWS()

    @mock.patch('boto3.client')
    def test_get_messages_from_queue_amount_greater_than_messages(self, mock_boto3):
        amount = 20
        params = {
            'aws_access_key_id': 'mock_access_key_id',
            'aws_secret_access_key': 'mock_secret_access_key',
            'sqs_queue_url': 'mock_sqs_queue_url',
        }
        messages = {'Messages': [{'MessageId': f'mock_MessageId_{i}', \
                                  'ReceiptHandle': f'mock_ReceiptHandle_{i}', \
                                  'MD5OfBody': f'mock_MD5OfBody_{i}', \
                                  'Body': f'mock_MD5OfBody_{i}'} for i in range(10)]}
       
        mock_sqs_client = mock_boto3.return_value
        mock_sqs_client.receive_message.return_value = messages

        result = self.__cloud.get_messages_from_queue(amount, params)
        self.assertEqual(len(result), amount)
        self.assertIsInstance(result, list)
        self.assertTrue(mock_sqs_client.receive_message.called)
        self.assertTrue(mock_sqs_client.receive_message.call_count == ceil(amount/10))

    @mock.patch('boto3.client')
    def test_get_messages_from_queue_amount_lower_than_messages(self, mock_boto3):
        amount = 100
        params = {
            'aws_access_key_id': 'mock_access_key_id',
            'aws_secret_access_key': 'mock_secret_access_key',
            'sqs_queue_url': 'mock_sqs_queue_url',
        }
        messages = {'Messages': [{'MessageId': f'mock_MessageId_{i}', \
                                  'ReceiptHandle': f'mock_ReceiptHandle_{i}', \
                                  'MD5OfBody': f'mock_MD5OfBody_{i}', \
                                  'Body': f'mock_MD5OfBody_{i}'} for i in range(10)]}
       
        mock_sqs_client = mock_boto3.return_value
        mock_sqs_client.receive_message.side_effect = [messages, {'Messages': []}]

        result = self.__cloud.get_messages_from_queue(amount, params)
        self.assertEqual(len(result), 10)
        self.assertIsInstance(result, list)
        self.assertTrue(mock_sqs_client.receive_message.call_count == 2)

    @mock.patch('boto3.resource')
    def test_load_json_file_from_storage_using_gz(self, mock_boto3):
        name = 'mock_name.json.gz'
        params = {
            'aws_access_key_id': 'mock_access_key_id',
            'aws_secret_access_key': 'mock_secret_access_key',
            'file_path': 'mock_path',
            'bucket': 'mock_bucket',
        }

        test_data = b'{"key": "value"}'
        compressed_data = BytesIO()
        with gzip.GzipFile(fileobj=compressed_data, mode='w') as gz_file:
            gz_file.write(test_data)
        compressed_data.seek(0)

        mock_s3_resource = mock_boto3.return_value
        mock_obj = mock_s3_resource.Object.return_value
        mock_obj.get.return_value = {'Body': mock.MagicMock(read=mock.MagicMock(return_value=compressed_data.getvalue()))}

        result = self.__cloud.load_json_file_from_storage(name, params)
        self.assertEqual(result, {"key": "value"})
    
    @mock.patch('boto3.resource')
    def test_load_json_file_from_storage_using_json(self, mock_boto3):
        name = 'mock_name.json'
        params = {
            'aws_access_key_id': 'mock_access_key_id',
            'aws_secret_access_key': 'mock_secret_access_key',
            'file_path': 'mock_path',
            'bucket': 'mock_bucket',
        }
        mock_s3_resource = mock_boto3.return_value
        mock_obj = mock_s3_resource.Object.return_value
        mock_obj.get.return_value = {'Body': mock.MagicMock(read=mock.MagicMock(return_value=b'{"key": "value"}'))}
        result = self.__cloud.load_json_file_from_storage(name, params)
        self.assertEqual(result, {"key": "value"})
    
    @mock.patch('boto3.resource')
    def test_remove_file_from_storage(self, mock_resource):
        name = 'mock_name.json.gz'
        params = {
            'aws_access_key_id': 'mock_access_key_id',
            'aws_secret_access_key': 'mock_secret_access_key',
            'file_path': 'mock_path',
            'bucket': 'mock_bucket',
        }

        self.__cloud.remove_file_from_storage(name, params)
        self.assertTrue(mock_resource.return_value.Object.return_value.delete.called)

    @mock.patch('boto3.client')
    def test_remove_messages_from_queue(self, mock_boto3):
        params = {
            'aws_access_key_id': 'mock_access_key_id',
            'aws_secret_access_key': 'mock_secret_access_key',
            'sqs_queue_url': 'mock_sqs_queue_url',
        }
        messages = [{'MessageId': f'mock_MessageId_{i}', \
                     'ReceiptHandle': f'mock_ReceiptHandle_{i}', \
                     'MD5OfBody': f'mock_MD5OfBody_{i}', \
                     'Body': f'mock_MD5OfBody_{i}'} for i in range(15)]
       
        mock_sqs_client = mock_boto3.return_value
        self.__cloud.remove_messages_from_queue(messages, params)
        self.assertTrue(mock_sqs_client.delete_message_batch.call_count == 2)

    @mock.patch('boto3.resource')
    def test_save_json_file_to_storage(self, mock_boto3):
        json_content = '{"key": "value"}'
        name = 'mock_name.json.gz'
        params = {
            'aws_access_key_id': 'mock_access_key_id',
            'aws_secret_access_key': 'mock_secret_access_key',
            'file_path': 'mock_path',
            'bucket': 'mock_bucket',
        }        
        mock_s3_resource = mock_boto3.return_value
        mock_obj = mock_s3_resource.Object.return_value

        result = self.__cloud.save_json_file_to_storage(json_content, name, params)
        location = f's3://{params['bucket']}/{params['file_path']}/{name}'
        mock_obj.put.assert_called_once()
        self.assertEqual(result, location)

    @mock.patch('boto3.client')
    def test_send_message_to_queue_standard(self, mock_boto3):
        message = 'mock_message'
        params = {
            'aws_access_key_id': 'mock_access_key_id',
            'aws_secret_access_key': 'mock_secret_access_key',
            'sqs_queue_url': 'mock_sqs_queue_url',
            'aws_region': 'mock_region'
        }
        mock_sqs_client = mock_boto3.return_value
        self.__cloud.send_message_to_sqs(message_body=message, fifo=False, params=params)
        self.assertTrue(mock_sqs_client.send_message.called)
        self.assertTrue(mock_sqs_client.send_message.call_count == 1)

    @mock.patch('boto3.client')
    def test_send_message_to_queue_fifo(self, mock_boto3):
        message = {'file_index': 'mock_message'}
        params = {
            'aws_access_key_id': 'mock_access_key_id',
            'aws_secret_access_key': 'mock_secret_access_key',
            'sqs_queue_url': 'mock_sqs_queue_url.fifo',
            'aws_region': 'mock_region'
        }
        mock_sqs_client = mock_boto3.return_value
        self.__cloud.send_message_to_sqs(message_body=message, fifo=True, params=params)
        self.assertTrue(mock_sqs_client.send_message.called)
        self.assertTrue(mock_sqs_client.send_message.call_count == 1)