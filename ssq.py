#!/usr/bin/python

__author__ = "Donghoon Lee"
__copyright__ = "Copyright 2020"
__credits__ = ["Donghoon Lee"]
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "donghoon.lee@mssm.edu"

### recreation of "dead simple queue" for LSF, inspired by https://github.com/ycrc/dSQ

import argparse
from subprocess import run
import sys
import re

### load args ###

parser = argparse.ArgumentParser(description='super simple queue')

### required args
parser.add_argument('--job-file', help='job file, one self-contained job per line', required=True)

### optional args
parser.add_argument('--job-name', help='name of your job array', required=False, type=str, default='ssq-job')
parser.add_argument('--max-jobs', help='maximum number of simultaneously running jobs from the job array',
                    required=False, type=int, default=100)

parser.add_argument('-P', '--project', help='project name', required=False, type=str, default='YourAllocationAccount')
parser.add_argument('-q', '--queue', help='queue name', required=False, type=str, default='express')
parser.add_argument('-W', '--walltime', help='wall time limit (HH:MM)', required=False, type=str, default='12:00')

parser.add_argument('--node', help='number of nodes per job', required=False, type=int, default=1)
parser.add_argument('--core', help='number of cores per job', required=False, type=int, default=2)
parser.add_argument('--mem', help='memory per node', required=False, type=str, default='8G')
parser.add_argument('--other', help='other lsf argument(s)', required=False, type=str)

parser.add_argument('--email', help='email after last job finishes', required=False, type=str)

args = parser.parse_args()


def main():
    desc = """Super Simple Queue v{}
    """.format(__version__)
    print(desc)

    ### count number of jobs in job_file
    n_jobs = sum(1 for line in open(args.job_file))

    ### make bsub command
    if args.other:
        cmd = 'bsub -J "%s[1-%s]%%%s" -P %s -q %s -W %s -n %s -R rusage[mem=%s] -R span[hosts=%s] -o %s_%%J_%%I.out %s "awk -v jobidx=\$LSB_JOBINDEX \'NR==jobidx\' %s | bash"' % (
            args.job_name, str(n_jobs), str(args.max_jobs), args.project, args.queue, args.walltime, str(args.core),
            args.mem, str(args.node), args.job_name, args.other, args.job_file)

    else:
        cmd = 'bsub -J "%s[1-%s]%%%s" -P %s -q %s -W %s -n %s -R rusage[mem=%s] -R span[hosts=%s] -o %s_%%J_%%I.out "awk -v jobidx=\$LSB_JOBINDEX \'NR==jobidx\' %s | bash"' % (
            args.job_name, str(n_jobs), str(args.max_jobs), args.project, args.queue, args.walltime, str(args.core),
            args.mem, str(args.node), args.job_name, args.job_file)

    ### submit
    print("submitting:\n    {}".format(cmd))
    out = run(cmd, shell=True, capture_output=True)
    print(out.stdout.decode("utf-8"))

    ### email notification
    if args.email:
        job_id_str = re.search('(?<=<).+?(?=>)', out.stdout.decode("utf-8")).group(0)
        email_cmd = 'bsub -J "%s_email" -P %s -q %s -W 10 -n 1 -o %s_%%J_email.out -w %s "bhist -l %s | mail -s \'[minerva job array] %s %s COMPLETED\' %s"' % (
            args.job_name, args.project, args.queue, args.job_name, job_id_str, job_id_str, args.job_name, job_id_str,
            args.email)
        print("submitting:\n    {}".format(email_cmd))
        run(email_cmd, shell=True, capture_output=False)

    sys.exit(out.returncode)


if __name__ == "__main__": main()
