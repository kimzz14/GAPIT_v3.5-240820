import os
import numpy as np

command_GAPIT = """
library(GAPIT)
myY <- read.table("phenotype.txt", head=TRUE)
myG <- read.table("../../variant.hmp.tab", head=FALSE)
myGAPIT <- GAPIT(Y=myY, G=myG, PCA.total=5, model=c("Blink", "FarmCPU", "SUPER", "MLMM", "CMLM", "MLM", "GLM", "gBLUP", "cBLUP", "sBLUP"), Multiple_analysis=TRUE)
q()
"""

phenotypeFile = 'phenotype.txt'

prefix = 'GAPIT'

fin = open(phenotypeFile)

legend_LIST = fin.readline().rstrip('\n').split('\t')
fields_LIST = []
for line in fin:
    data_LIST = line.rstrip('\n').split('\t')
    fields = {key:value for key, value in zip(legend_LIST, data_LIST)}
    fields_LIST += [fields]
fin.close()


if os.path.isdir(prefix) == True:
    print("exist directory")
    raise SystemExit(-1)

os.mkdir(prefix)
fout_all = open('run.sh', 'w')
for phenotype in legend_LIST[1:]:
    os.mkdir(prefix + '/' + phenotype)
    fout = open(prefix + '/' + phenotype + '/' + phenotypeFile, 'w')
    fout.write('Taxa' + '\t' + phenotype + '\n')
    for fields in fields_LIST:
        fout.write(fields['Taxa'] + '\t' + fields[phenotype] + '\n')
    fout.close()

    fout = open(prefix + '/' + phenotype + '/' + 'run_GAPIT.r', 'w')
    fout.write(command_GAPIT)
    fout.close()

    fout = open(prefix + '/' + phenotype + '/' + 'run.sh', 'w')
    fout.write('cd' + ' ' + prefix + '/' + phenotype + '\n')
    fout.write('Rscript --verbose run_GAPIT.r 1> run.log 2> run.err')
    fout.close()
    fout_all.write('sh' + ' ' + prefix + '/' + phenotype + '/' + 'run.sh' + '\n')
fout_all.close()