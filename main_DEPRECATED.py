import os
os.environ["LOG_SEVERITY"] = "ERROR"
from flask_api import status as http_status_code
from main import create_logger
from settings import TestingConfig
import json
import argparse

create_logger(TestingConfig)
from main.api.queries import Queries

parser = argparse.ArgumentParser(description='tsunamigenic evaluator')
group = parser.add_mutually_exclusive_group()
group.add_argument('-f', '--json_data_file', help='input json formatted data-file-path')
group.add_argument('-d', '--json_data', help='input json formatted data')
args = parser.parse_args()

if args.json_data_file:
    if not os.path.isfile(args.json_data_file):
        print (f"file {args.json_data_file} do not exist")

    with open (args.json_data_file) as f:
        data = json.load(f)
else:
    data = json.loads(args.json_data)

queries = Queries()
data, status = queries.tsunamigenic_evaluation(data)

if status != http_status_code.HTTP_200_OK:
    print (json.dumps(data))
else:
    print (json.dumps(data))
