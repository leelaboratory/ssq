# ssq: super simple queue
simple script to make lsf job array
1. creates LSF job array from job file (one job per line)
2. sends email notification upon completion

## usage
```
usage: ssq.py [-h] --job-file JOB_FILE [--job-name JOB_NAME]
              [--max-jobs MAX_JOBS] [-P PROJECT] [-q QUEUE] [-W WALLTIME]
              [--node NODE] [--core CORE] [--mem MEM] [--other OTHER]
              [--email EMAIL]

super simple queue

optional arguments:
  -h, --help            show this help message and exit
  --job-file JOB_FILE   job file, one self-contained job per line
  --job-name JOB_NAME   name of your job array
  --max-jobs MAX_JOBS   maximum number of simultaneously running jobs from the
                        job array
  -P PROJECT, --project PROJECT
                        project name
  -q QUEUE, --queue QUEUE
                        queue name
  -W WALLTIME, --walltime WALLTIME
                        wall time limit (HH:MM)
  --node NODE           number of nodes per job
  --core CORE           number of cores per job
  --mem MEM             memory per node
  --other OTHER         other lsf argument(s)
  --email EMAIL         email after last job finishes
  ```
  
  ## example
  ```
python ssq.py --job-file test_jobfile --job-name test_jobname --project acc_yourprojectname --queue express --walltime 12:00 --max-jobs 20 --core 2 --mem 4G --email youremail@mssm.edu
  ```
