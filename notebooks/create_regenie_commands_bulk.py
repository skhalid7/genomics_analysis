#!/opt/conda/bin/python
import papermill as pm
import sys
from datetime import datetime
import argparse
import scrapbook as sb

parser = argparse.ArgumentParser()
parser.add_argument("--phenotype", "-p", type=str,
                    help="phenotype name", required = True)
parser.add_argument("--runname", "-r", type=str,
                    help="runname", required = True)
parser.add_argument("--cohort", "-c", type=str,
                    help="space delimited string of cohorts", required = True)
parser.add_argument("--metafile", "-m",
                    type=str, help="path to metafile", required=False, default="NA")

args = parser.parse_args()

now = datetime.now()
dt_string = now.strftime("%Y_%m_%d__%H:%M")

#update paths here 
#to automate put params in config file
path_2_notebook = "/home/jupyter/genomics_analysis/notebooks"
notebook_to_execute = f"{path_2_notebook}/create_regenie_commands.ipynb"
output_notebook = notebook_to_execute.split("/")[-1].split(".ipynb")[0]
output_nb_folder = f"{path_2_notebook}/notebook_runs"

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
