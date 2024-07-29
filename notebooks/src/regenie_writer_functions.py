from datetime import datetime
import pandas as pd


def printRegenieHouseKeeping(file_handle, regenie_path, step, phenotypes, cohort, run_name, date_time, threads):
    '''
    This function will add the top comments and regenie version to regnie command
    '''
    print('#Regenie Step {} command'.format(step), file=file_handle)
    print('#Phenotypes: {}'.format(phenotypes), file=file_handle)
    print('#Cohort: {}'.format(cohort), file=file_handle)
    print('#run_name: {}'.format(run_name), file=file_handle)
    print('#Date_Time Generated: {}'.format(date_time), file=file_handle)
    print(" ", file=file_handle)
    print("{} \\".format(regenie_path), file=file_handle)
    print("--threads {} \\".format(threads), file=file_handle)

def printRegenieExtractions(file_handle, base_path, bgen_file, vars_to_extract, phenotypes_file_name,\
                            covariates_file_name, cat_covars, covar_lists, \
                            trait_type, rint, ref_first = True, verbose = True, bsize = 2000):
    '''
    Given bgen file with variant lists phenotypes and covariates file  write out commands which
    are common to step 1 and 2
    '''
    
    bgen_sample_file = bgen_file.split(".bgen")[0] + ".sample"
    
    print("--bgen {}/{} \\".format(base_path, bgen_file) , file=file_handle)
    print("--extract {}/{} \\".format(base_path, vars_to_extract), file=file_handle)
    print("--sample {}/{} \\".format(base_path, bgen_sample_file), file=file_handle)
    print("--phenoFile {} \\".format(phenotypes_file_name), file=file_handle)
    print("--covarFile {} \\".format(covariates_file_name), file=file_handle)
    if len(cat_covars) > 0:
        print("--catCovarList {} \\".format(",".join(cat_covars)), file=file_handle)
    if len(covar_lists) > 0:
        print("--covarColList {} \\".format(",".join(covar_lists)), file=file_handle)
    if ref_first:
        print("--ref-first \\", file=file_handle)
    if verbose:
        print("--verbose \\", file=file_handle)
    print("--{} \\".format(trait_type), file=file_handle)
    if rint != "false" and trait_type == "qt":
        print("--apply-rint \\", file=file_handle) #apply rint if QT
    print("--bsize {} \\".format(bsize), file=file_handle)

def printRegenieStep2(file_handle, base_path, cohort, run_name, output_file, trait_type, model, loco_predictions = "nan",\
                      anno_file = "nan", set_list = "nan", mask_defs = "nan", aafs = "nan", case_control_imbalance = "--firth --approx --pThresh 0.05"):
    
    '''
    print out step 2 specific commands, if gene burden files will write out gene burden command
    '''
    print("--step 2 \\", file = file_handle)
    print("--htp {}-{} \\".format(cohort, run_name), file = file_handle)
    if loco_predictions != "nan":
        print("--pred {} \\".format(loco_predictions), file=file_handle)
    else:
        print("--ignore-pred \\", file = file_handle)
    if trait_type == "bt":
        print("{} \\".format(case_control_imbalance), file = file_handle) #add p-value threshold for case control imbalance correction
    if model == "nan":
        print("--test {} \\".format("additive"), file = file_handle)
    else:
        print("--test {} \\".format(model), file = file_handle)
    
    '''
    print gene burden specific commands
    '''
    if anno_file != "nan" and set_list != "nan" and mask_defs != "nan" and aafs != "nan":
        print("writing gene burden results files")
        print("--anno-file {}/{} \\".format(base_path, anno_file), file=file_handle)
        print("--set-list {}/{} \\".format(base_path, set_list), file=file_handle)
        print("--mask-def {}/{} \\".format(base_path, mask_defs), file=file_handle)
        print("--aaf-file {}/{} \\".format(base_path, aafs), file=file_handle)
        print("--write-mask-snplist \\", file=file_handle)
    
    '''
    print output path
    '''
    print("--out {}".format(output_file), file=file_handle)

def printGenericRegenieStep2(output_file, trait_type, gene_burden = True, rint = "false", base_path = "."):
    f = open(output_file)
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d__%H:%M")
    printRegenieHouseKeeping(f, "2", "X", "X", "X", dt_string)
    printRegenieExtractions(file_handle = f, base_path = base_path, bgen_file = "X", vars_to_extract = "X", phenotypes_file_name = "X", \
                            covariates_file_name = "X", cat_covars = "X", covar_lists = "X", \
                            trait_type = trait_type, rint = rint)
    if gene_burden:
        printRegenieStep2(file_handle = f, base_path = base_path, cohort = "X", run_name = "X", output_file = "X", trait_type = trait_type, model = "X", loco_predictions = "X",\
            anno_file = "X", set_list = "X", mask_defs = "X", aafs = "X")
    else:
        printRegenieStep2(file_handle = f, base_path = base_path, cohort = "X", run_name = "X", output_file = "X", trait_type = trait_type, model = "X", loco_predictions = "X",)

    f.close()

def processPCInput(pc_covars_string):
    '''
    This will convert strings such as PC:{1:10},rare_PC{1:10} to [ PC1,PC2...PC10 and rare_PC1, rare_PC2... ]
    '''
    try:
        
        split_vals = pc_covars_string.split("{")
        base_col_name = split_vals[0]
        number_of_pcs = [ int(x) for x in split_vals[1][:-1].split(":") ]
        
        return [ base_col_name + str(x) for x in range(number_of_pcs[0], number_of_pcs[1] + 1) ]
    except:
        "Error parsing covariates string {}".format(pc_covars_string)

def createAnalysisReadyFiles(df):
    '''
    Format phenotype and covariates file to a regenie amenable format
    '''
    df.reset_index(inplace = True)
    df.rename(columns = {"sampleId" : "IID"}, inplace = True)
    df_cols = list(df.columns)
    df["FID"] = df.loc[:, 'IID']
    return df[["FID"] + df_cols]

def splitIfExists(cols, delim = ";"):
    '''
    If column exists will return a split array otherwise will return an empty array
    '''
    if pd.notnull(cols):
        return cols.split(delim)
    else:
        return []
