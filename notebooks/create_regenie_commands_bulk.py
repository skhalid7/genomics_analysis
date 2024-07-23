#!/opt/conda/bin/python
import papermill as pm
import sys
from datetime import datetime
import argparse
import scrapbook as sb
from src import utils

parser = argparse.ArgumentParser()
parser.add_argument("--phenotype", "-p", type=str,
                    help="phenotype name", required = True)
parser.add_argument("--runname", "-r", type=str,
                    help="runname", required = True)
parser.add_argument("--cohort", "-c", type=str,
                    help="space delimited string of cohorts", required = True)
parser.add_argument("--configfile", "-cf",
                    type=str, help="path to config file")
parser.add_argument("--metafile", "-m",
                    type=str, help="path to metafile", required=False, default="NA")

args = parser.parse_args()

now = datetime.now()
dt_string = now.strftime("%Y_%m_%d__%H:%M")

#update paths here 
notebook_paths = utils.get_config_parameter("notebooks", args.configfile)
notebook_to_execute = notebook_paths["create_regenie_commands"]
path_2_notebook = "/".join(notebook_to_execute.split("/")[0:-1])
output_nb_folder = notebook_paths["output_folder"]
output_notebook = notebook_to_execute.split("/")[-1].split(".ipynb")[0]

outnotebook_name = output_nb_folder + "/" + output_notebook + "_" + args.runname + "_" + args.phenotype + "_" + args.cohort + "_" + dt_string + "." + "ipynb"

print("Phenotype: " + args.phenotype)
print("Cohort: " + args.cohort)
print("Run Name: " + args.runname)

pm.execute_notebook(
    notebook_to_execute,
    outnotebook_name,
    parameters = dict(run_name=args.runname, phenotype_names=args.phenotype, cohort=args.cohort, metafile=args.metafile),
    cwd = path_2_notebook
)

outputs = sb.read_notebook(outnotebook_name).scraps["command_files"].data
for output in outputs:
    print(output)
