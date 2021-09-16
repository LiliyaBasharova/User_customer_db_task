import os
from collections import Counter
from typing import Union, Dict, Any
from pathlib import Path

import boto3
import pandas as pd

from Catalog import *
from db_utils import *

catalog = Catalog(engine)

path = "/home/user39/Documents/runs/outputs/FFPE_for_LDT_2.1"
path_end = "output/somatic-strelka-passed-vep-annotated.maf"

def download_from_aws():
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


class Parser:
    def parse_maf(maf_path: Union[str, "Path"]) -> Dict[str, Any]:
        data = pd.read_csv(maf_path, sep='\t', comment='#')
        counter = Counter(data["Variant_Classification"])
        value = "Missense_Mutation"
        return counter[value]


for subdir in os.listdir(path):
        filepath = os.path.join(path, subdir, path_end)
        res = Parser.parse_maf(filepath)
        print(subdir, res)
        sample = catalog.insert_sample(name=subdir)
        mutation = catalog.insert_mutation(name=res)
        catalog.add_mutation_to_sample(sample_id=sample.id, mutation_id=mutation.id)
