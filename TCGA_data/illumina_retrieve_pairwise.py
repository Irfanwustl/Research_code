import requests
import json
from io import StringIO
import pandas as pd
import numpy as np
import re
import os
from pandas.errors import EmptyDataError 
import sys

organ = sys.argv[1]

def save_files(organ):
    organ_name = '_'.join(organ.split(' '))
    try:
        os.mkdir(organ_name)
    except FileExistsError:
        pass
    fields = [
        "file_name",
        "cases.submitter_id",
        "cases.samples.sample_type",
        "cases.disease_type",
        "cases.project.project_id",
        "cases.primary_site"
        ]

    fields = ",".join(fields)

    files_endpt = "https://api.gdc.cancer.gov/files"
    
    filters = {
        "op": "and",
        "content":[
            {
            "op": "in",
            "content":{
                "field": "files.data_format",
                "value": ["TXT"]
                }
            },
            {
            "op": "in",
            "content":{
                "field": "cases.project.primary_site",
                "value": [organ]
                }
            },
            {
            "op": "in",
            "content":{
                "field": "files.data_category",
                "value": ["DNA Methylation"]
                }
            },
            {
            "op": "in",
            "content":{
                "field": "files.platform",
                "value": ["Illumina Human Methylation 450"]
                }
            },
        ]
    }

    # A POST is used, so the filter parameters can be passed directly as a Dict object.
    params = {
        "filters": filters,
        "fields": fields,
        "format": "TSV",
        "size": "2000"
        }

    # The parameters are passed to 'json' rather than 'params' in this case
    response = requests.post(files_endpt, headers = {"Content-Type": "application/json"}, json = params)
    resp = response.content.decode("utf-8")
    try:
        resp_df = pd.read_csv(StringIO(resp), sep='\t')
    except EmptyDataError:
        print('No normal tissue for', organ)
        return 0
    u, c = np.unique(np.array(resp_df['cases.0.submitter_id']), return_counts=True)
    dup = u[c > 1]
    df_new = pd.DataFrame(columns=resp_df.columns)
    for sub in dup:
        df_sub = resp_df[resp_df['cases.0.submitter_id'] == sub]
        tissues = np.unique(df_sub['cases.0.samples.0.sample_type'])
        if len(tissues) > 1 and "Solid Tissue Normal" in tissues:
            df_new = pd.concat([df_new, df_sub])
            for i, ID in enumerate(np.array(df_sub['id'])):
                file_id = ID
                project_id = np.array(df_sub['cases.0.project.project_id'])[i]
                tissue = np.array(df_sub['cases.0.samples.0.sample_type'])[i]

                data_endpt = "https://api.gdc.cancer.gov/data/{}".format(file_id)

                response = requests.get(data_endpt, headers = {"Content-Type": "application/json"})

                # The file name can be found in the header within the Content-Disposition key.
                response_head_cd = response.headers["Content-Disposition"]

                file_name = re.findall("filename=(.+)", response_head_cd)[0]

                tissue_name = '_'.join(tissue.split(' '))
                full_name = organ_name + '/' + organ_name + '_' + project_id + '_' + sub + '_' + tissue_name + '_' + file_name
                with open(full_name, "wb") as output_file:
                    output_file.write(response.content)
    df_new.to_csv(organ_name + '/' + organ_name + '.txt', sep='\t', index=None)
    return df_new

res = save_files(organ)