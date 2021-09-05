from pathlib import Path

import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')
prefix = 'runs/outputs/FFPE_for_LDT_2.1/'
bucket = s3.Bucket('ldt-metrics-automatisation')
for my_bucket_object in bucket.objects.filter(Prefix=prefix):
    filename = "somatic-strelka-passed-vep-annotated.maf"
    if my_bucket_object.key.endswith(filename):
        key = my_bucket_object.key

        target_dir = "/home/user39/Documents/" + key
        path = Path(target_dir)
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        bucket.download_file(key, str(target_dir))
