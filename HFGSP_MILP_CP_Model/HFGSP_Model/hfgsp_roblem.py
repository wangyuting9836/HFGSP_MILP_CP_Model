# Hybrid Flowshop Group Scheduling Problem
import proplem_parser
from proplem_parser import fields  # noqa: F401


class HFGSProblem(proplem_parser.Problem):
    F = fields.IntegerField('Families')
    S = fields.IntegerField('Stages')
    # SetupType = fields.IntegerField('SetupType')
    M_s = fields.ListField('Number of Machines at each Stage')
    machines_at_each_stage = fields.IndexedCoordinatesField('Machines at each Stage:')
    M = fields.IntegerField('Total number of machines')
    J_f = fields.ListField('Number of Jobs in each Family')
    jobs_in_each_family = fields.IndexedCoordinatesField('Jobs in each Family')
    J = fields.IntegerField('Total number of jobs')
    process_time = fields.MatrixField('Processing times of jobs')
    setup_time = fields.MatrixField('Setup times')

    def __init__(self, **data):
        super().__init__(**data)
