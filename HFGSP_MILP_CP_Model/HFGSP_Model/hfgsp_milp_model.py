import os
import gurobipy as gp
import numpy as np
import pandas
import pandas as pd
from gurobipy import GRB
import proplem_parser
from HFGSP_Model.hfgsp_roblem import HFGSProblem


class HFGSPMILPModel:
    G = 0x0000ffff

    def __init__(self, filename):

        self.problem_name = filename.replace('.txt', '')
        self.problem = proplem_parser.load(os.path.dirname(os.path.abspath(__file__)) + '/data/' + filename,
                                           problem_class=HFGSProblem)

        # self.problem = proplem_parser.load(filename, problem_class=HFGSProblem)

        self.F = self.problem.F
        self.family_array = np.arange(0, self.F + 1)

        self.S = self.problem.S
        self.stage_array = np.arange(0, self.S + 1)

        self.M = self.problem.M
        self.machine_array = np.arange(0, self.M + 1)

        self.J = self.problem.J
        self.job_array = np.arange(0, self.J + 1)

        self.M_s = np.insert(np.array(self.problem.M_s), 0, 0)
        self.machines_at_each_stage = self.problem.machines_at_each_stage

        self.J_f = np.insert(np.array(self.problem.J_f), 0, 0)
        self.jobs_in_each_family = self.problem.jobs_in_each_family

        for f in self.family_array[1:]:
            self.jobs_in_each_family[f] = np.insert(self.jobs_in_each_family[f], 0, 0)

        self.process_time = np.array(self.problem.process_time)
        self.process_time = np.insert(self.process_time, 0, np.zeros((1, self.S), dtype=int), 0)
        self.process_time = np.insert(self.process_time, 0, np.zeros((1, self.J + 1), dtype=int), 1)

        self.setup_time = np.array(self.problem.setup_time)
        self.setup_time = np.insert(self.setup_time, 0, np.zeros((self.F, self.F), dtype=int), 0)
        for s in self.stage_array:
            self.setup_time = np.insert(self.setup_time, s * (self.F + 1), np.zeros((1, self.F), dtype=int), 0)
        self.setup_time = np.insert(self.setup_time, 0, np.zeros((1, (self.S + 1) * (self.F + 1)), dtype=int), 1)
        self.setup_time = np.reshape(self.setup_time, (self.S + 1, self.F + 1, self.F + 1))

        for s in self.stage_array[1:]:
            for f in self.family_array[1:]:
                self.setup_time[s, 0, f] = self.setup_time[s, f, f]

        self.model = None
        self.c = None
        self.w = None
        self.x = None
        self.mu = None
        self.x1 = None
        self.mu1 = None
        self.q = None
        self.q1 = None
        self.d = None
        self.t = None
        self.u = None
        self.t1 = None
        self.u1 = None
        self.d1 = None
        self.y = None
        self.sigma = None
        self.z = None
        self.r = None
        self.v = None
        self.v1 = None
        self.a = None
        self.b = None
        self.b1 = None
        self.c_max = None
        self.model_name = None

    def creat_model(self, name):
        # Create a new model
        self.model_name = name
        self.model = gp.Model(name)
        self.model.setParam(GRB.Param.IntFeasTol, 1e-6)
        self.model.setParam(GRB.Param.TimeLimit, 1000)

    def creat_var_c(self):
        self.c = {}
        for f in self.family_array[1:]:
            self.c[f] = self.model.addVars(self.jobs_in_each_family[f][1:], [f], self.stage_array[1:],
                                           vtype=GRB.INTEGER, name='c')

    def creat_var_a(self):
        self.a = {}
        for f in self.family_array[1:]:
            self.a[f] = self.model.addVars(self.jobs_in_each_family[f][1:], [f], self.stage_array[1:],
                                           vtype=GRB.INTEGER, name='a')

    def creat_var_b(self):
        self.b = {}
        for s in self.stage_array[1:]:
            self.b[s] = self.model.addVars(self.job_array[1:], self.machines_at_each_stage[s], [s],
                                           vtype=GRB.INTEGER, name='b')

    def creat_var_b1(self):
        self.b1 = self.model.addVars(self.job_array[1:], self.stage_array[1:], vtype=GRB.INTEGER, name='b1')

    def set_objective(self):
        # Set objective
        self.model.setObjective(self.c_max, GRB.MINIMIZE)

        # Optimize model
        self.model.optimize()

    def arrangement_of_families1(self):

        # Create variables
        self.w = {}
        for s in self.stage_array[1:]:
            self.w[s] = self.model.addVars(self.family_array[1:], self.machines_at_each_stage[s], [s],
                                           vtype=GRB.BINARY, name="w")
        self.x = {}
        for s in self.stage_array[1:]:
            self.x[s] = self.model.addVars(self.family_array, self.family_array, self.machines_at_each_stage[s], [s],
                                           vtype=GRB.BINARY, name="x")
        self.mu = {}
        for s in self.stage_array[1:]:
            self.mu[s] = self.model.addVars(self.family_array[1:], self.machines_at_each_stage[s], [s],
                                            vtype=GRB.INTEGER, name="mu")

        # (1)
        self.model.addConstrs(gp.quicksum(self.w[s][f, m, s] for m in self.machines_at_each_stage[s]) == 1
                              for f in self.family_array[1:]
                              for s in self.stage_array[1:])
        # (2)
        self.model.addConstrs(
            gp.quicksum(self.x[s][f1, f2, m, s] for f2 in self.family_array if f2 != f1) == self.w[s][f1, m, s]
            for f1 in self.family_array[1:]
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s])

        # (3)
        self.model.addConstrs(
            gp.quicksum(self.x[s][f1, f2, m, s] for f1 in self.family_array if f1 != f2) == self.w[s][f2, m, s]
            for f2 in self.family_array[1:]
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s])

        # (4)
        self.model.addConstrs(
            gp.quicksum(self.x[s][0, f2, m, s] for f2 in self.family_array) == 1
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s])

        # (5)
        self.model.addConstrs(
            gp.quicksum(self.x[s][f1, 0, m, s] for f1 in self.family_array) == 1
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s])

        # (6)
        self.model.addConstrs(self.mu[s][f1, m, s] - self.mu[s][f2, m, s] - (1 - self.x[s][f1, f2, m, s]) * self.F <= -1
                              for f1 in self.family_array[1:]
                              for f2 in self.family_array[1:]
                              if f1 != f2
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])

        # (7)
        self.model.addConstrs(self.mu[s][f, m, s] >= 1
                              for f in self.family_array[1:]
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])

    def arrangement_of_families2(self):
        # Create variables
        self.x1 = self.model.addVars(self.family_array, self.family_array, self.stage_array[1:], vtype=GRB.BINARY,
                                     name="x1")
        self.mu1 = self.model.addVars(self.family_array[1:], self.stage_array[1:], vtype=GRB.INTEGER, name="mu1")

        # (8)
        self.model.addConstrs(
            gp.quicksum(self.x1[f1, f2, s] for f2 in self.family_array if f2 != f1) == 1
            for f1 in self.family_array[1:]
            for s in self.stage_array[1:])

        # (9)
        self.model.addConstrs(
            gp.quicksum(self.x1[f1, f2, s] for f1 in self.family_array if f1 != f2) == 1
            for f2 in self.family_array[1:]
            for s in self.stage_array[1:])

        # (10)
        self.model.addConstrs(
            gp.quicksum(self.x1[0, f2, s] for f2 in self.family_array) == self.M_s[s]
            for s in self.stage_array[1:])

        # (11)
        self.model.addConstrs(
            gp.quicksum(self.x1[f1, 0, s] for f1 in self.family_array) == self.M_s[s]
            for s in self.stage_array[1:])

        # (12)
        self.model.addConstrs(self.mu1[f1, s] - self.mu1[f2, s] - (1 - self.x1[f1, f2, s]) * self.F <= -1
                              for f1 in self.family_array[1:]
                              for f2 in self.family_array[1:]
                              if f1 != f2
                              for s in self.stage_array[1:])

        # (13)
        self.model.addConstrs(self.mu1[f, s] >= 1
                              for f in self.family_array[1:]
                              for s in self.stage_array[1:])

    def arrangement_of_families3(self):
        # Create variables
        self.w = {}
        for s in self.stage_array[1:]:
            self.w[s] = self.model.addVars(self.family_array[1:], self.machines_at_each_stage[s], [s],
                                           vtype=GRB.BINARY, name="w")
        self.q = {}
        for s in self.stage_array[1:]:
            self.q[s] = self.model.addVars(self.family_array[1:], self.family_array[1:], self.machines_at_each_stage[s],
                                           [s], vtype=GRB.BINARY, name="q")

        # (1)
        self.model.addConstrs(gp.quicksum(self.w[s][f, m, s] for m in self.machines_at_each_stage[s]) == 1
                              for f in self.family_array[1:]
                              for s in self.stage_array[1:])

        # (14)
        self.model.addConstrs(gp.quicksum(self.q[s][f, p, m, s] for p in self.family_array[1:]) == self.w[s][f, m, s]
                              for f in self.family_array[1:]
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])

        # (15)
        self.model.addConstrs(gp.quicksum(self.q[s][f, p, m, s] for f in self.family_array[1:]) <= 1
                              for p in self.family_array[1:]
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])

        # (16)
        self.model.addConstrs(gp.quicksum(self.q[s][f, p, m, s] for f in self.family_array[1:])
                              <= gp.quicksum(self.q[s][f, p - 1, m, s] for f in self.family_array[1:])
                              for p in self.family_array[2:]
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])

    def arrangement_of_families4(self):
        # Create variables
        self.q1 = self.model.addVars(self.family_array[1:], self.family_array[1:], self.stage_array[1:],
                                     vtype=GRB.BINARY, name="q1")
        self.d = self.model.addVars(self.family_array[1:], self.stage_array[1:], vtype=GRB.BINARY, name="d")

        # (17)
        self.model.addConstrs(gp.quicksum(self.q1[f, p, s] for p in self.family_array[1:]) == 1
                              for f in self.family_array[1:]
                              for s in self.stage_array[1:])

        # (18)
        self.model.addConstrs(gp.quicksum(self.q1[f, p, s] for f in self.family_array[1:]) == 1
                              for p in self.family_array[1:]
                              for s in self.stage_array[1:])

        # (19)
        self.model.addConstrs(self.d[1, s] == 1
                              for s in self.stage_array[1:])

        # (20)
        self.model.addConstrs(gp.quicksum(self.d[p, s] for p in self.family_array[1:]) <= self.M_s[s]
                              for s in self.stage_array[1:])

    def arrangement_of_families5(self):
        # Create variables
        self.w = {}
        for s in self.stage_array[1:]:
            self.w[s] = self.model.addVars(self.family_array[1:], self.machines_at_each_stage[s], [s],
                                           vtype=GRB.BINARY, name="w")
        self.t = {}
        for s in self.stage_array[1:]:
            self.t[s] = self.model.addVars(self.family_array[1:], self.job_array[1:], self.machines_at_each_stage[s],
                                           [s], vtype=GRB.BINARY, name="t")
        self.u = {}
        for s in self.stage_array[1:]:
            self.u[s] = self.model.addVars(self.family_array[1:], self.job_array[1:], self.machines_at_each_stage[s],
                                           [s], vtype=GRB.BINARY, name="u")

        # (1)
        self.model.addConstrs(gp.quicksum(self.w[s][f, m, s] for m in self.machines_at_each_stage[s]) == 1
                              for f in self.family_array[1:]
                              for s in self.stage_array[1:])

        # (21)
        self.model.addConstrs(
            gp.quicksum(self.t[s][f, p, m, s] for p in self.job_array[1:]) == self.w[s][f, m, s]
            for f in self.family_array[1:]
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s])

        # (22)
        self.model.addConstrs(gp.quicksum(self.u[s][f, p, m, s] for p in self.job_array[1:])
                              == self.J_f[f] * self.w[s][f, m, s]
                              for f in self.family_array[1:]
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])

        # (23)
        self.model.addConstrs(gp.quicksum(self.u[s][f, p, m, s] for f in self.family_array[1:]) <= 1
                              for p in self.job_array[1:]
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])

        # (24)
        self.model.addConstrs(self.u[s][f, 1, m, s] == self.t[s][f, 1, m, s]
                              for f in self.family_array[1:]
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])

        # (25)
        self.model.addConstrs(self.u[s][f, p, m, s] - self.u[s][f, p - 1, m, s] <= self.t[s][f, p, m, s]
                              for f in self.family_array[1:]
                              for p in self.job_array[2:]
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])
        # (26)
        self.model.addConstrs(gp.quicksum(self.u[s][f, p, m, s] for f in self.family_array[1:])
                              <= gp.quicksum(self.u[s][f, p - 1, m, s] for f in self.family_array[1:])
                              for p in self.job_array[2:]
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])

    def arrangement_of_families6(self):
        # Create variables
        self.t1 = self.model.addVars(self.family_array[1:], self.job_array[1:], self.stage_array[1:], vtype=GRB.BINARY,
                                     name="t1")
        self.u1 = self.model.addVars(self.family_array[1:], self.job_array[1:], self.stage_array[1:], vtype=GRB.BINARY,
                                     name="u1")
        self.d1 = self.model.addVars(self.job_array[1:], self.stage_array[1:], vtype=GRB.BINARY, name="d1")

        # (27)
        self.model.addConstrs(gp.quicksum(self.t1[f, p, s] for p in self.job_array[1:]) == 1
                              for f in self.family_array[1:]
                              for s in self.stage_array[1:])

        # (28)
        self.model.addConstrs(gp.quicksum(self.u1[f, p, s] for p in self.job_array[1:]) == self.J_f[f]
                              for f in self.family_array[1:]
                              for s in self.stage_array[1:])

        # (29)
        self.model.addConstrs(gp.quicksum(self.u1[f, p, s] for f in self.family_array[1:]) == 1
                              for p in self.job_array[1:]
                              for s in self.stage_array[1:])

        # (30)
        self.model.addConstrs(self.u1[f, 1, s] == self.t1[f, 1, s]
                              for f in self.family_array[1:]
                              for s in self.stage_array[1:])

        # (31)
        self.model.addConstrs(self.u1[f, p, s] - self.u1[f, p - 1, s] <= self.t1[f, p, s]
                              for f in self.family_array[1:]
                              for p in self.job_array[2:]
                              for s in self.stage_array[1:])

        # (32)
        self.model.addConstrs(self.d1[1, s] == 1
                              for s in self.stage_array[1:])

        # (33)
        self.model.addConstrs(self.d1[p, s] <= gp.quicksum(self.t1[f, p, s] for f in self.family_array[1:])
                              for p in self.job_array[1:]
                              for s in self.stage_array[1:])

        # (34)
        self.model.addConstrs(gp.quicksum(self.d1[p, s] for p in self.job_array[1:]) <= self.M_s[s]
                              for s in self.stage_array[1:])

    def arrangement_of_jobs_in_the_family1(self):
        # Create variables
        self.y = {}
        for f in self.family_array[1:]:
            self.y[f] = self.model.addVars(self.jobs_in_each_family[f], self.jobs_in_each_family[f], [f],
                                           vtype=GRB.BINARY, name='y')
        self.sigma = {}
        for f in self.family_array[1:]:
            self.sigma[f] = self.model.addVars(self.jobs_in_each_family[f][1:], [f], vtype=GRB.INTEGER, name='sigma')

        # (35)
        self.model.addConstrs(gp.quicksum(self.y[f][j1, j2, f] for j2 in self.jobs_in_each_family[f] if j2 != j1) == 1
                              for f in self.family_array[1:]
                              for j1 in self.jobs_in_each_family[f])

        # (36)
        self.model.addConstrs(gp.quicksum(self.y[f][j1, j2, f] for j1 in self.jobs_in_each_family[f] if j1 != j2) == 1
                              for f in self.family_array[1:]
                              for j2 in self.jobs_in_each_family[f])

        # (37)
        self.model.addConstrs(
            self.sigma[f][j1, f] - self.sigma[f][j2, f] - (1 - self.y[f][j1, j2, f]) * self.J_f[f] <= -1
            for f in self.family_array[1:]
            for j1 in self.jobs_in_each_family[f][1:]
            for j2 in self.jobs_in_each_family[f][1:]
            if j1 != j2)

        # (38)
        self.model.addConstrs(self.sigma[f][j, f] >= 1
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:])

    def arrangement_of_jobs_in_the_family2(self):
        # Create variables
        self.z = {}
        for f in self.family_array[1:]:
            self.z[f] = self.model.addVars(self.jobs_in_each_family[f][1:], self.jobs_in_each_family[f][1:], [f],
                                           vtype=GRB.BINARY, name='z')

        # (39)
        self.model.addConstrs(self.z[f][j1, j2, f] + self.z[f][j2, j1, f] == 1
                              for f in self.family_array[1:]
                              for j1 in self.jobs_in_each_family[f][1:]
                              for j2 in self.jobs_in_each_family[f][1:]
                              if j1 < j2)

    def arrangement_of_jobs_in_the_family3(self):
        # Create variables
        self.r = {}
        for f in self.family_array[1:]:
            self.r[f] = self.model.addVars(self.jobs_in_each_family[f][1:], self.jobs_in_each_family[f][1:], [f],
                                           vtype=GRB.BINARY, name='r')

        # (40)
        self.model.addConstrs(gp.quicksum(self.r[f][j, p, f] for p in self.jobs_in_each_family[f][1:]) == 1
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:])

        # (41)
        self.model.addConstrs(gp.quicksum(self.r[f][j, p, f] for j in self.jobs_in_each_family[f][1:]) == 1
                              for f in self.family_array[1:]
                              for p in self.jobs_in_each_family[f][1:])

    def arrangement_of_jobs_in_the_family4(self):
        # Create variables
        self.v = {}
        for s in self.stage_array[1:]:
            for f in self.family_array[1:]:
                self.v[s, f] = self.model.addVars(self.jobs_in_each_family[f][1:], [f], self.job_array[1:],
                                                  self.machines_at_each_stage[s], [s], vtype=GRB.BINARY, name='v')

        # (42)
        self.model.addConstrs(gp.quicksum(self.v[s, f][j, f, p, m, s] for j in self.jobs_in_each_family[f][1:])
                              == self.u[s][f, p, m, s]
                              for f in self.family_array[1:]
                              for p in self.job_array[1:]
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])

        # (43)
        self.model.addConstrs(gp.quicksum(self.v[s, f][j, f, p, m, s] for p in self.job_array[1:]) <= 1
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:]
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])

        # (44)
        self.model.addConstrs(self.v[1, f][j, f, p1 + p, m1, 1] >= self.v[s, f][j, f, p2 + p, m2, s] +
                              (self.t[1][f, p1, m1, 1] + self.t[s][f, p2, m2, s] - 2) * self.G
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:]
                              for p1 in self.job_array[1:-self.J_f[f] + 1]
                              for p2 in self.job_array[1:-self.J_f[f] + 1]
                              for p in np.arange(0, self.J_f[f])
                              for s in self.stage_array[2:]
                              for m1 in self.machines_at_each_stage[1]
                              for m2 in self.machines_at_each_stage[s])
        # (45)
        self.model.addConstrs(self.v[1, f][j, f, p1 + p, m1, 1] <= self.v[s, f][j, f, p2 + p, m2, s] -
                              (self.t[1][f, p1, m1, 1] + self.t[s][f, p2, m2, s] - 2) * self.G
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:]
                              for p1 in self.job_array[1:-self.J_f[f] + 1]
                              for p2 in self.job_array[1:-self.J_f[f] + 1]
                              for p in np.arange(0, self.J_f[f])
                              for s in self.stage_array[2:]
                              for m1 in self.machines_at_each_stage[1]
                              for m2 in self.machines_at_each_stage[s])

    def arrangement_of_jobs_in_the_family5(self):
        # Create variables
        self.v1 = {}
        for f in self.family_array[1:]:
            self.v1[f] = self.model.addVars(self.jobs_in_each_family[f][1:], [f], self.job_array[1:],
                                            self.stage_array[1:], vtype=GRB.BINARY, name='v1')

        # (46)
        self.model.addConstrs(gp.quicksum(self.v1[f][j, f, p, s] for j in self.jobs_in_each_family[f][1:])
                              == self.u1[f, p, s]
                              for f in self.family_array[1:]
                              for p in self.job_array[1:]
                              for s in self.stage_array[1:])

        # (47)
        self.model.addConstrs(gp.quicksum(self.v1[f][j, f, p, s] for p in self.job_array[1:]) == 1
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:]
                              for s in self.stage_array[1:])

        # (48)
        self.model.addConstrs(self.v1[f][j, f, p1 + p, 1] >= self.v1[f][j, f, p2 + p, s] +
                              (self.t1[f, p1, 1] + self.t1[f, p2, s] - 2) * self.G
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:]
                              for p1 in self.job_array[1:-self.J_f[f] + 1]
                              for p2 in self.job_array[1:-self.J_f[f] + 1]
                              for p in np.arange(0, self.J_f[f])
                              for s in self.stage_array[2:])
        # (49)
        self.model.addConstrs(self.v1[f][j, f, p1 + p, 1] <= self.v1[f][j, f, p2 + p, s] -
                              (self.t1[f, p1, 1] + self.t1[f, p2, s] - 2) * self.G
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:]
                              for p1 in self.job_array[1:-self.J_f[f] + 1]
                              for p2 in self.job_array[1:-self.J_f[f] + 1]
                              for p in np.arange(0, self.J_f[f])
                              for s in self.stage_array[2:])

    def process_requirements_between_families1(self):
        # (50)
        self.model.addConstrs(
            self.c[f][j, f, s] >= self.setup_time[s, 0, f]
            + (gp.quicksum(self.x[s][0, f, m, s] for m in self.machines_at_each_stage[s]) - 1) * self.G
            + self.process_time[j, s]
            for f in self.family_array[1:]
            for j in self.jobs_in_each_family[f][1:]
            for s in self.stage_array[1:])

        # (51)
        self.model.addConstrs(
            self.c[f2][j2, f2, s] >= self.c[f1][j1, f1, s] + self.setup_time[s, f1, f2]
            + (gp.quicksum(self.x[s][f1, f2, m, s] for m in self.machines_at_each_stage[s]) - 1) * self.G
            + self.process_time[j2, s]
            for f1 in self.family_array[1:]
            for f2 in self.family_array[1:]
            if f1 != f2
            for j1 in self.jobs_in_each_family[f1][1:]
            for j2 in self.jobs_in_each_family[f2][1:]
            for s in self.stage_array[1:])

    def process_requirements_between_families2(self):
        # (52)
        self.model.addConstrs(
            self.a[f][self.jobs_in_each_family[f][1], f, s] >= self.setup_time[s, 0, f]
            + (gp.quicksum(self.x[s][0, f, m, s] for m in self.machines_at_each_stage[s]) - 1) * self.G
            + gp.quicksum(self.process_time[j, s] * self.r[f][j, self.jobs_in_each_family[f][1], f]
                          for j in self.jobs_in_each_family[f][1:])
            for f in self.family_array[1:]
            for s in self.stage_array[1:])

        # (53)
        self.model.addConstrs(
            self.a[f2][self.jobs_in_each_family[f2][1], f2, s] >= self.a[f1][self.jobs_in_each_family[f1][-1], f1, s]
            + self.setup_time[s, f1, f2]
            + (gp.quicksum(self.x[s][f1, f2, m, s] for m in self.machines_at_each_stage[s]) - 1) * self.G
            + gp.quicksum(self.process_time[j2, s] * self.r[f2][j2, self.jobs_in_each_family[f2][1], f2]
                          for j2 in self.jobs_in_each_family[f2][1:])
            for f1 in self.family_array[1:]
            for f2 in self.family_array[1:]
            if f1 != f2
            for s in self.stage_array[1:])

    def process_requirements_between_families3(self):
        # (54)
        self.model.addConstrs(
            self.c[f][j, f, s] >= self.setup_time[s, 0, f] + (self.x1[0, f, s] - 1) * self.G + self.process_time[j, s]
            for f in self.family_array[1:]
            for j in self.jobs_in_each_family[f][1:]
            for s in self.stage_array[1:])

        # (55)
        self.model.addConstrs(
            self.c[f2][j2, f2, s] >= self.c[f1][j1, f1, s] + self.setup_time[s, f1, f2]
            + (self.x1[f1, f2, s] - 1) * self.G + self.process_time[j2, s]
            for f1 in self.family_array[1:]
            for f2 in self.family_array[1:]
            if f1 != f2
            for j1 in self.jobs_in_each_family[f1][1:]
            for j2 in self.jobs_in_each_family[f2][1:]
            for s in self.stage_array[1:])

    def process_requirements_between_families4(self):
        # (56)
        self.model.addConstrs(
            self.a[f][self.jobs_in_each_family[f][1], f, s] >= self.setup_time[s, 0, f]
            + (self.x1[0, f, s] - 1) * self.G
            + gp.quicksum(self.process_time[j, s] * self.r[f][j, self.jobs_in_each_family[f][1], f]
                          for j in self.jobs_in_each_family[f][1:])
            for f in self.family_array[1:]
            for s in self.stage_array[1:])

        # (57)
        self.model.addConstrs(
            self.a[f2][self.jobs_in_each_family[f2][1], f2, s] >= self.a[f1][self.jobs_in_each_family[f1][-1], f1, s]
            + self.setup_time[s, f1, f2] + (self.x1[f1, f2, s] - 1) * self.G
            + gp.quicksum(self.process_time[j2, s] * self.r[f2][j2, self.jobs_in_each_family[f2][1], f2]
                          for j2 in self.jobs_in_each_family[f2][1:])
            for f1 in self.family_array[1:]
            for f2 in self.family_array[1:]
            if f1 != f2
            for s in self.stage_array[1:])

    def process_requirements_between_families5(self):
        # (58)
        self.model.addConstrs(
            self.c[f][j, f, s] >= self.setup_time[s, 0, f]
            + (gp.quicksum(self.q[s][f, 1, m, s] for m in self.machines_at_each_stage[s]) - 1) * self.G
            + self.process_time[j, s]
            for f in self.family_array[1:]
            for j in self.jobs_in_each_family[f][1:]
            for s in self.stage_array[1:])

        # (59)
        self.model.addConstrs(
            self.c[f2][j2, f2, s] >= self.c[f1][j1, f1, s] + self.setup_time[s, f1, f2]
            + (self.q[s][f1, p - 1, m, s] + self.q[s][f2, p, m, s] - 2) * self.G
            + self.process_time[j2, s]
            for f1 in self.family_array[1:]
            for f2 in self.family_array[1:]
            if f1 != f2
            for j1 in self.jobs_in_each_family[f1][1:]
            for j2 in self.jobs_in_each_family[f2][1:]
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s]
            for p in self.family_array[2:])

    def process_requirements_between_families6(self):
        # (60)
        self.model.addConstrs(
            self.a[f][self.jobs_in_each_family[f][1], f, s] >= self.setup_time[s, 0, f]
            + (gp.quicksum(self.q[s][f, 1, m, s] for m in self.machines_at_each_stage[s]) - 1) * self.G
            + gp.quicksum(self.process_time[j, s] * self.r[f][j, self.jobs_in_each_family[f][1], f]
                          for j in self.jobs_in_each_family[f][1:])
            for f in self.family_array[1:]
            for s in self.stage_array[1:])

        # (61)
        self.model.addConstrs(
            self.a[f2][self.jobs_in_each_family[f2][1], f2, s] >= self.a[f1][self.jobs_in_each_family[f1][-1], f1, s]
            + self.setup_time[s, f1, f2] + (self.q[s][f1, p - 1, m, s] + self.q[s][f2, p, m, s] - 2) * self.G
            + gp.quicksum(self.process_time[j2, s] * self.r[f2][j2, self.jobs_in_each_family[f2][1], f2]
                          for j2 in self.jobs_in_each_family[f2][1:])
            for f1 in self.family_array[1:]
            for f2 in self.family_array[1:]
            if f1 != f2
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s]
            for p in self.family_array[2:])

    def process_requirements_between_families7(self):
        # (62)
        self.model.addConstrs(
            self.c[f][j, f, s] >= self.setup_time[s, 0, f] + (self.q1[f, p, s] + self.d[p, s] - 2) * self.G
            + self.process_time[j, s]
            for f in self.family_array[1:]
            for j in self.jobs_in_each_family[f][1:]
            for s in self.stage_array[1:]
            for p in self.family_array[1:])

        # (63)
        self.model.addConstrs(
            self.c[f2][j2, f2, s] >= self.c[f1][j1, f1, s] + self.setup_time[s, f1, f2]
            + (self.q1[f1, p - 1, s] + self.q1[f2, p, s]
               - (gp.quicksum(self.d[i, s] for i in np.arange(1, p + 1))
                  - gp.quicksum(self.d[i, s] for i in np.arange(1, p))) - 2) * self.G
            + self.process_time[j2, s]
            for f1 in self.family_array[1:]
            for f2 in self.family_array[1:]
            if f1 != f2
            for j1 in self.jobs_in_each_family[f1][1:]
            for j2 in self.jobs_in_each_family[f2][1:]
            for s in self.stage_array[1:]
            for p in self.family_array[2:])

    def process_requirements_between_families8(self):
        # (64)
        self.model.addConstrs(
            self.a[f][self.jobs_in_each_family[f][1], f, s] >= self.setup_time[s, 0, f]
            + (self.q1[f, p, s] + self.d[p, s] - 2) * self.G
            + gp.quicksum(self.process_time[j, s] * self.r[f][j, self.jobs_in_each_family[f][1], f]
                          for j in self.jobs_in_each_family[f][1:])
            for f in self.family_array[1:]
            for s in self.stage_array[1:]
            for p in self.family_array[1:])

        # (65)
        self.model.addConstrs(
            self.a[f2][self.jobs_in_each_family[f2][1], f2, s] >= self.a[f1][self.jobs_in_each_family[f1][-1], f1, s]
            + self.setup_time[s, f1, f2]
            + (self.q1[f1, p - 1, s] + self.q1[f2, p, s]
               - (gp.quicksum(self.d[i, s] for i in np.arange(1, p + 1))
                  - gp.quicksum(self.d[i, s] for i in np.arange(1, p))) - 2) * self.G
            + gp.quicksum(self.process_time[j2, s] * self.r[f2][j2, self.jobs_in_each_family[f2][1], f2]
                          for j2 in self.jobs_in_each_family[f2][1:])
            for f1 in self.family_array[1:]
            for f2 in self.family_array[1:]
            if f1 != f2
            for s in self.stage_array[1:]
            for p in self.family_array[2:])

    def process_requirements_between_families9(self):
        # (66)
        self.model.addConstrs(
            self.c[f][j, f, s] >= self.setup_time[s, 0, f]
            + (gp.quicksum(self.t[s][f, 1, m, s] for m in self.machines_at_each_stage[s]) - 1) * self.G
            + self.process_time[j, s]
            for f in self.family_array[1:]
            for j in self.jobs_in_each_family[f][1:]
            for s in self.stage_array[1:])

        # (67)
        self.model.addConstrs(
            self.c[f2][j2, f2, s] >= self.c[f1][j1, f1, s] + self.setup_time[s, f1, f2]
            + (self.t[s][f1, p - self.J_f[f1], m, s] + self.t[s][f2, p, m, s] - 2) * self.G
            + self.process_time[j2, s]
            for f1 in self.family_array[1:]
            for f2 in self.family_array[1:]
            if f1 != f2
            for j1 in self.jobs_in_each_family[f1][1:]
            for j2 in self.jobs_in_each_family[f2][1:]
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s]
            for p in self.job_array[self.J_f[f1] + 1:-self.J_f[f2] + 1])

    def process_requirements_between_families10(self):
        # (68)
        self.model.addConstrs(
            self.b[s][1, m, s] >= self.setup_time[s, 0, f]
            + (self.t[s][f, 1, m, s] - 1) * self.G
            + gp.quicksum(
                self.process_time[j, s] * self.v[s, f][j, f, 1, m, s] for j in self.jobs_in_each_family[f][1:])
            for f in self.family_array[1:]
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s])

        # (69)
        self.model.addConstrs(
            self.b[s][p, m, s] >= self.b[s][p - 1, m, s] + self.setup_time[s, f1, f2]
            + (self.t[s][f1, p - self.J_f[f1], m, s] + self.t[s][f2, p, m, s] - 2) * self.G
            + gp.quicksum(
                self.process_time[j2, s] * self.v[s, f2][j2, f2, p, m, s] for j2 in self.jobs_in_each_family[f2][1:])
            for f1 in self.family_array[1:]
            for f2 in self.family_array[1:]
            if f1 != f2
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s]
            for p in self.job_array[self.J_f[f1] + 1:-self.J_f[f2] + 1])

    def process_requirements_between_families11(self):
        # (70)
        self.model.addConstrs(
            self.c[f][j, f, s] >= self.setup_time[s, 0, f] + (self.t1[f, p, s] + self.d1[p, s] - 2) * self.G
            + self.process_time[j, s]
            for f in self.family_array[1:]
            for j in self.jobs_in_each_family[f][1:]
            for s in self.stage_array[1:]
            for p in self.job_array[1:len(self.job_array) - self.J_f[f] + 1])

        # (71)
        self.model.addConstrs(
            self.c[f2][j2, f2, s] >= self.c[f1][j1, f1, s] + self.setup_time[s, f1, f2]
            + (self.t1[f1, p - self.J_f[f1], s] + self.t1[f2, p, s]
               - (gp.quicksum(self.d1[i, s] for i in np.arange(1, p + 1))
                  - gp.quicksum(self.d1[i, s] for i in np.arange(1, p - self.J_f[f1] + 1))) - 2) * self.G
            + self.process_time[j2, s]
            for f1 in self.family_array[1:]
            for f2 in self.family_array[1:]
            if f1 != f2
            for j1 in self.jobs_in_each_family[f1][1:]
            for j2 in self.jobs_in_each_family[f2][1:]
            for s in self.stage_array[1:]
            for p in self.job_array[self.J_f[f1] + 1:len(self.job_array) - self.J_f[f2] + 1])

    def process_requirements_between_families12(self):
        # (72)
        self.model.addConstrs(
            self.b1[p, s] >= self.setup_time[s, 0, f] + (self.t1[f, p, s] + self.d1[p, s] - 2) * self.G
            + gp.quicksum(
                self.process_time[j, s] * self.v1[f][j, f, p, s] for j in self.jobs_in_each_family[f][1:])
            for f in self.family_array[1:]
            for s in self.stage_array[1:]
            for p in self.job_array[1:])

        # (73)
        self.model.addConstrs(
            self.b1[p, s] >= self.b1[p - 1, s] + self.setup_time[s, f1, f2]
            + (self.t1[f1, p - self.J_f[f1], s] + self.t1[f2, p, s]
               - (gp.quicksum(self.d1[i, s] for i in np.arange(1, p + 1))
                  - gp.quicksum(self.d1[i, s] for i in np.arange(1, p - self.J_f[f1] + 1))) - 2) * self.G
            + gp.quicksum(
                self.process_time[j, s] * self.v1[f2][j, f2, p, s] for j in self.jobs_in_each_family[f2][1:])
            for f1 in self.family_array[1:]
            for f2 in self.family_array[1:]
            if f1 != f2
            for s in self.stage_array[1:]
            for p in self.job_array[self.J_f[f1] + 1:len(self.job_array) - self.J_f[f2] + 1])

    def process_requirements_between_jobs_from_same_family1(self):
        # (74)
        self.model.addConstrs(self.c[f][j2, f, s] >= self.c[f][j1, f, s] + (self.y[f][j1, j2, f] - 1) * self.G
                              + self.process_time[j2, s]
                              for f in self.family_array[1:]
                              for j1 in self.jobs_in_each_family[f][1:]
                              for j2 in self.jobs_in_each_family[f][1:]
                              if j1 != j2
                              for s in self.stage_array[1:])

    def process_requirements_between_jobs_from_same_family2(self):
        # (75)
        self.model.addConstrs(self.c[f][j2, f, s] >= self.c[f][j1, f, s] + (self.z[f][j1, j2, f] - 1) * self.G
                              + self.process_time[j2, s]
                              for f in self.family_array[1:]
                              for j1 in self.jobs_in_each_family[f][1:]
                              for j2 in self.jobs_in_each_family[f][1:]
                              if j1 != j2
                              for s in self.stage_array[1:])

    def process_requirements_between_jobs_from_same_family3(self):
        # (76)
        self.model.addConstrs(
            self.c[f][j2, f, s] >= self.c[f][j1, f, s] + (self.r[f][j1, p - 1, f] + self.r[f][j2, p, f] - 2) * self.G
            + self.process_time[j2, s]
            for f in self.family_array[1:]
            for j1 in self.jobs_in_each_family[f][1:]
            for j2 in self.jobs_in_each_family[f][1:]
            if j1 != j2
            for p in self.jobs_in_each_family[f][2:]
            for s in self.stage_array[1:])

    def process_requirements_between_jobs_from_same_family4(self):
        # (77)
        self.model.addConstrs(
            self.a[f][p, f, s] >= self.a[f][p - 1, f, s]
            + gp.quicksum(self.process_time[j, s] * self.r[f][j, p, f] for j in self.jobs_in_each_family[f][1:])
            for f in self.family_array[1:]
            for p in self.jobs_in_each_family[f][2:]
            for s in self.stage_array[1:])

    def process_requirements_between_jobs_from_same_family5(self):
        # (78)
        self.model.addConstrs(
            self.c[f][j2, f, s] >= self.c[f][j1, f, s] + (
                    self.v[s, f][j1, f, p - 1, m, s] + self.v[s, f][j2, f, p, m, s] - 2) * self.G
            + self.process_time[j2, s]
            for f in self.family_array[1:]
            for j1 in self.jobs_in_each_family[f][1:]
            for j2 in self.jobs_in_each_family[f][1:]
            if j1 != j2
            for p in self.job_array[2:]
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s])

    def process_requirements_between_jobs_from_same_family6(self):
        # (79)
        self.model.addConstrs(
            self.b[s][p, m, s] >= self.b[s][p - 1, m, s]
            + gp.quicksum(self.process_time[j, s] * self.v[s, f][j, f, p, m, s]
                          for f in self.family_array[1:]
                          for j in self.jobs_in_each_family[f][1:])
            for p in self.job_array[2:]
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s])

    def process_requirements_between_jobs_from_same_family7(self):
        # (80)
        self.model.addConstrs(
            self.c[f][j2, f, s] >= self.c[f][j1, f, s] + (
                    self.v1[f][j1, f, p - 1, s] + self.v1[f][j2, f, p, s] - 2) * self.G
            + self.process_time[j2, s]
            for f in self.family_array[1:]
            for j1 in self.jobs_in_each_family[f][1:]
            for j2 in self.jobs_in_each_family[f][1:]
            if j1 != j2
            for p in self.job_array[2:]
            for s in self.stage_array[1:])

    def process_requirements_between_jobs_from_same_family8(self):
        # (81)
        self.model.addConstrs(
            self.b1[p, s] >= self.b1[p - 1, s] - self.d1[p, s] * self.G
            + gp.quicksum(self.process_time[j, s] * self.v1[f][j, f, p, s]
                          for f in self.family_array[1:]
                          for j in self.jobs_in_each_family[f][1:])
            for p in self.job_array[2:]
            for s in self.stage_array[1:])

    def process_requirements_between_adjacent_stages1(self):
        # (82)
        self.model.addConstrs(self.c[f][j, f, s] >= self.c[f][j, f, s - 1] + self.process_time[j, s]
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:]
                              for s in self.stage_array[2:])

    def process_requirements_between_adjacent_stages2(self):
        # (83)
        None
        self.model.addConstrs(
            self.a[f][p, f, s] >= self.a[f][p, f, s - 1]
            + gp.quicksum(self.process_time[j, s] * self.r[f][j, p, f] for j in self.jobs_in_each_family[f][1:])
            for f in self.family_array[1:]
            for p in self.jobs_in_each_family[f][1:]
            for s in self.stage_array[2:])

    def process_requirements_between_adjacent_stages3(self):
        # (84)
        self.model.addConstrs(
            self.b[s][p1, m1, s] >= self.b[s - 1][p2, m2, s - 1]
            + (self.v[s, f][j, f, p1, m1, s] + self.v[s - 1, f][j, f, p2, m2, s - 1] - 2) * self.G
            + self.process_time[j, s]
            for f in self.family_array[1:]
            for j in self.jobs_in_each_family[f][1:]
            for p1 in self.job_array[1:]
            for p2 in self.job_array[1:]
            for s in self.stage_array[2:]
            for m1 in self.machines_at_each_stage[s]
            for m2 in self.machines_at_each_stage[s - 1])

    def process_requirements_between_adjacent_stages4(self):
        # (85)
        self.model.addConstrs(
            self.b1[p1, s] >= self.b1[p2, s - 1] + (self.v1[f][j, f, p1, s] + self.v1[f][j, f, p2, s - 1] - 2) * self.G
            + self.process_time[j, s]
            for f in self.family_array[1:]
            for j in self.jobs_in_each_family[f][1:]
            for p1 in self.job_array[1:]
            for p2 in self.job_array[1:]
            for s in self.stage_array[2:])

    def relationship_between_the_decision_variables_of_completion_time1(self):
        # (86)
        self.model.addConstrs(self.c[f][j, f, s] >= self.a[f][p, f, s] + (self.r[f][j, p, f] - 1) * self.G
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:]
                              for p in self.jobs_in_each_family[f][1:]
                              for s in self.stage_array[1:])
        # (87)
        self.model.addConstrs(self.c[f][j, f, s] <= self.a[f][p, f, s] - (self.r[f][j, p, f] - 1) * self.G
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:]
                              for p in self.jobs_in_each_family[f][1:]
                              for s in self.stage_array[1:])

    def relationship_between_the_decision_variables_of_completion_time2(self):
        # (88)
        self.model.addConstrs(self.c[f][j, f, s] >= self.b[s][p, m, s] + (self.v[s, f][j, f, p, m, s] - 1) * self.G
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:]
                              for p in self.job_array[1:]
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])
        # (89)
        self.model.addConstrs(self.c[f][j, f, s] <= self.b[s][p, m, s] - (self.v[s, f][j, f, p, m, s] - 1) * self.G
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:]
                              for p in self.job_array[1:]
                              for s in self.stage_array[1:]
                              for m in self.machines_at_each_stage[s])

    def relationship_between_the_decision_variables_of_completion_time3(self):
        # (90)
        self.model.addConstrs(self.c[f][j, f, s] >= self.b1[p, s] + (self.v1[f][j, f, p, s] - 1) * self.G
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:]
                              for p in self.job_array[1:]
                              for s in self.stage_array[1:])
        # (91)
        self.model.addConstrs(self.c[f][j, f, s] <= self.b1[p, s] - (self.v1[f][j, f, p, s] - 1) * self.G
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:]
                              for p in self.job_array[1:]
                              for s in self.stage_array[1:])

    def makespan_constraint1(self):
        self.c_max = self.model.addVar(name='c_max', vtype=GRB.INTEGER)

        # (92)
        self.model.addConstrs(self.c_max >= self.c[f][j, f, self.S]
                              for f in self.family_array[1:]
                              for j in self.jobs_in_each_family[f][1:])

    def makespan_constraint2(self):
        self.c_max = self.model.addVar(name='c_max', vtype=GRB.INTEGER)

        # (93)
        self.model.addConstrs(self.c_max >= self.a[f][self.jobs_in_each_family[f][self.J_f[f]], f, self.S]
                              for f in self.family_array[1:])

    def makespan_constraint3(self):
        self.c_max = self.model.addVar(name='c_max', vtype=GRB.INTEGER)

        # (94)
        self.model.addConstrs(self.c_max >= self.b[self.S][p, m, self.S]
                              for m in self.machines_at_each_stage[self.S]
                              for p in self.job_array[1:])

    def makespan_constraint4(self):
        self.c_max = self.model.addVar(name='c_max', vtype=GRB.INTEGER)

        # (95)
        self.model.addConstrs(self.c_max >= self.b1[p, self.S]
                              for p in self.job_array[1:])

    def print_vars(self):
        # print("Model Attributes")
        print("Current optimization status", self.model.Status)
        print("Indicates whether the model is a MIP", self.model.IsMIP)
        print("Indicates whether the model has multiple objectives", self.model.IsMultiObj)
        if self.model.IsMultiObj == 0:
            print("Current relative MIP optimality gap", self.model.MIPGap)
        print("Runtime for most recent optimization", self.model.Runtime)
        print("Work spent on most recent optimization", self.model.Work)

        print("Number of variables", self.model.NumVars)
        print("Number of integer variables", self.model.NumIntVars)
        print("NumBinVars", self.model.NumBinVars)

        print("Number of linear constraints", self.model.NumConstrs)
        print("Number of SOS constraints", self.model.NumSOS)
        print("Number of quadratic constraints", self.model.NumQConstrs)
        print("Number of general constraints", self.model.NumGenConstrs)

        print("Number of non-zero coefficients in the constraint matrix", self.model.NumNZs)
        print("Number of non-zero coefficients in the constraint matrix (in double format)", self.model.DNumNZs)
        print("Number of non-zero quadratic objective terms", self.model.NumQNZs)
        print("Number of non-zero terms in quadratic constraints", self.model.NumQCNZs)

        print("Number of stored solutions", self.model.SolCount)
        print("Number of simplex iterations performed in most recent optimization", self.model.IterCount)
        print("Number of barrier iterations performed in most recent optimization", self.model.NodeCount)
        print("Number of branch-and-cut nodes explored in most recent optimization", self.model.NumQCNZs)
        print("Number of open branch-and-cut nodes at the end of most recent optimization", self.model.OpenNodeCount)

        print("Maximum linear objective coefficient (in absolute value)", self.model.MaxObjCoeff)
        print("MinObjCoeff	Minimum (non-zero) linear objective coefficient (in absolute value)",
              self.model.MinObjCoeff)
        print("Maximum constraint right-hand side (in absolute value)", self.model.MaxRHS)
        print("Minimum (non-zero) constraint right-hand side (in absolute value)", self.model.MinRHS)

        # get the set of variables
        variables = self.model.getVars()

        # Ensure status is optimal
        # assert self.model.Status == GRB.Status.OPTIMAL

        # Query number of multiple objectives, and number of solutions
        nSolutions = self.model.SolCount
        nObjectives = self.model.NumObj
        print('Problem has', nObjectives, 'objectives')
        print('Gurobi found', nSolutions, 'solutions')

        # For each solution, print value of first three variables, and
        # value for each objective function
        solutions = []
        for s in range(nSolutions):
            # Set which solution we will query from now on
            self.model.params.SolutionNumber = s

            # Print objective value of this solution in each objective
            print('Solution', s, ':', end=' ')
            if self.model.IsMultiObj == 0:
                print(self.model.PoolObjVal, end=' ')
            else:
                for o in range(nObjectives):
                    # Set which objective we will query
                    self.model.params.ObjNumber = o
                    # Query the o-th objective value
                    print(self.model.ObjNVal, end=' ')

            # print first three variables in the solution
            print('->', end=' ')
            n = min(len(variables), 10)
            j = 0
            for v in variables:
                if v.Xn >= 0.9:
                    print(v.VarName, v.Xn, end=' ')
                    j = j + 1
                    if j == n:
                        break
            print('')

            # query the full vector of the o-th solution
            solutions.append(self.model.getAttr('Xn', variables))
        print('Optimal Solution variables')
        if nSolutions > 0:
            for v in variables:
                if v.X >= 0.9:
                    print(v.VarName, v.X)

    def write_csv(self, csv_file):
        csv_result = {}
        csv_result["Problem"] = self.problem_name
        csv_result["Model"] = self.model_name
        status = ''
        match self.model.Status:
            case 1:
                status = "LOADED"
            case 2:
                status = "OPTIMAL"
            case 3:
                status = "INFEASIBLE"
            case 4:
                status = "INF_OR_UNBD"
            case 5:
                status = "UNBOUNDED"
            case 6:
                status = "CUTOFF"
            case 7:
                status = "ITERATION_LIMIT"
            case 8:
                status = "NODE_LIMIT"
            case 9:
                status = "TIME_LIMIT"
            case 10:
                status = "SOLUTION_LIMIT"
            case 11:
                status = "INTERRUPTED"
            case 12:
                status = "NUMERIC"
            case 13:
                status = "SUBOPTIMAL"
            case 14:
                status = "INPROGRESS"
            case 15:
                status = "USER_OBJ_LIMIT"
            case 16:
                status = "WORK_LIMIT"
            case 17:
                status = "MEM_LIMIT"
        csv_result["Current optimization status"] = status + "(" + str(self.model.Status) + ")"
        csv_result["Indicates whether the model is a MIP"] = self.model.IsMIP
        csv_result["Indicates whether the model has multiple objectives"] = self.model.IsMultiObj
        if self.model.IsMultiObj == 0:
            csv_result["Current relative MIP optimality gap"] = self.model.MIPGap
        csv_result["Runtime for most recent optimization"] = self.model.Runtime
        csv_result["Work spent on most recent optimization"] = self.model.Work

        csv_result["Number of variables"] = self.model.NumVars
        csv_result["Number of integer variables"] = self.model.NumIntVars
        csv_result["NumBinVars"] = self.model.NumBinVars

        csv_result["Number of linear constraints"] = self.model.NumConstrs
        csv_result["Number of SOS constraints"] = self.model.NumSOS
        csv_result["Number of quadratic constraints"] = self.model.NumQConstrs
        csv_result["Number of general constraints"] = self.model.NumGenConstrs

        csv_result["Number of non-zero coefficients in the constraint matrix"] = self.model.NumNZs
        csv_result["Number of non-zero coefficients in the constraint matrix (in double format)"] = self.model.DNumNZs
        csv_result["Number of non-zero quadratic objective terms"] = self.model.NumQNZs
        csv_result["Number of non-zero terms in quadratic constraints"] = self.model.NumQCNZs

        csv_result["Number of stored solutions"] = self.model.SolCount
        csv_result["Number of simplex iterations performed in most recent optimization"] = self.model.IterCount
        csv_result["Number of barrier iterations performed in most recent optimization"] = self.model.NodeCount
        csv_result["Number of branch-and-cut nodes explored in most recent optimization"] = self.model.NumQCNZs
        csv_result[
            "Number of open branch-and-cut nodes at the end of most recent optimization"] = self.model.OpenNodeCount

        csv_result["Maximum linear objective coefficient (in absolute value"] = self.model.MaxObjCoeff
        csv_result[
            "MinObjCoeff Minimum (non-zero) linear objective coefficient (in absolute value)"] = self.model.MinObjCoeff
        csv_result["Maximum constraint right-hand side (in absolute value)"] = self.model.MaxRHS
        csv_result["Minimum (non-zero constraint right-hand side (in absolute value)"] = self.model.MinRHS

        # get the set of variables
        variables = self.model.getVars()

        # Ensure status is optimal
        # assert self.model.Status == GRB.Status.OPTIMAL

        # Query number of multiple objectives, and number of solutions
        nSolutions = self.model.SolCount
        nObjectives = self.model.NumObj

        csv_result["Number of objectives"] = nObjectives
        csv_result["Number of solutions Gurobi found"] = nSolutions

        # For each solution, print value of first three variables, and
        # value for each objective function

        PoolObjVal = ''
        for s in range(nSolutions):
            # Set which solution we will query from now on
            self.model.params.SolutionNumber = s

            # Print objective value of this solution in each objective
            # print('Solution', s, ':', end=' ')
            if self.model.IsMultiObj == 0:
                PoolObjVal += str(self.model.PoolObjVal) + ','
            else:
                for o in range(nObjectives):
                    # Set which objective we will query
                    self.model.params.ObjNumber = o
                    # Query the o-th objective value
                    # print(self.model.ObjNVal, end=' ')
                    PoolObjVal += str(self.model.ObjNVal) + ' '
                PoolObjVal += ','
        csv_result["PoolObjVal"] = PoolObjVal

        df = pandas.DataFrame(csv_result, index=[0])
        df.to_csv(csv_file, mode='a', index=False, header=False)