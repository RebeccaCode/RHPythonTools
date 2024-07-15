import gzip
import os

import boto3


class AwsS3Utilities:

    def __init__(self, aws_source_user, aws_source_secret, aws_destination_user, aws_destination_secret):
        self.aws_source_user = aws_source_user
        self.aws_source_secret = aws_source_secret
        self.aws_destination_user = aws_destination_user
        self.aws_destination_secret = aws_destination_secret

    def download_from_s3(self, s3_source_uris, local_destination_path):
        # establish connections
        source_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_source_user,
            aws_secret_access_key=self.aws_source_secret,
        )

        destination_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_destination_user,
            aws_secret_access_key=self.aws_destination_secret,
        )

        # one file at a time (because size constraints)
        for index, s3_source_uri in enumerate(s3_source_uris):
            file_name = s3_source_uri.split('/')[-1]
            s3_source_bucket = s3_source_uri.split('/')[2]
            s3_object_key = s3_source_uri.replace(s3_source_bucket+'/', '').replace('s3://','')

            local_file_compressed_path = os.path.join(local_destination_path, file_name)

            source_client.download_file(s3_source_bucket, s3_object_key, local_file_compressed_path)

            print(local_file_compressed_path)

    # def unzip_downloaded_file(self):
    #     local_file_decompressed = local_file_compressed_path[0:len(local_file_compressed_path) - 3]
    #
    #     with gzip.open(local_file_compressed_path, 'rb') as f_read:
    #         s_out = gzip.decompress(f_read)
    #         with open(local_file_decompressed, 'wb') as f_write:
    #             f_write.write(s_out)
    #
    #     print(local_file_decompressed)


if __name__ == "__main__":
    test = AwsS3Utilities(aws_source_user='',
                          aws_source_secret='',
                          aws_destination_user=None, aws_destination_secret=None)
    test.download_from_s3(
        s3_source_uris=[
            '',
            ''],
        local_destination_path='')
