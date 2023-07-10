import os

import matplotlib
import numpy as np
from docplex.cp.model import *
import docplex.cp.utils_visu as visu
from matplotlib import pyplot as plt

import proplem_parser
from HFGSP_Model.hfgsp_roblem import HFGSProblem


class HFGSPCPModel:
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

        self.model_name = None
        self.model = None
        self.job_intervals = None
        self.family_intervals = None
        self.family_intervals_on_machine = None
        self.job_sequence_in_family = None
        self.family_sequence_on_machine = None
        self.res = None

    def creat_model(self, name):
        # Create a new model
        self.model_name = name
        self.model = CpoModel()

        self.job_intervals = {
            (j, f, s): interval_var(name='I_J{}_F{}_S{}'.format(j, f, s), size=self.process_time[j, s])
            for f in self.family_array[1:]
            for j in self.jobs_in_each_family[f][1:]
            for s in self.stage_array[1:]}

        self.family_intervals = {
            (f, s): interval_var(name='I_F{}_S{}'.format(f, s))
            for f in self.family_array[1:]
            for s in self.stage_array[1:]}

        self.family_intervals_on_machine = {
            (0, m, s): interval_var(name='I_F{}_M{}_S{}'.format(0, m, s), size=0)
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s]}

        self.family_intervals_on_machine.update({
            (f, m, s): interval_var(name='I_F{}_M{}_S{}'.format(f, m, s), optional=True)
            for f in self.family_array[1:]
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s]})

        self.job_sequence_in_family = {
            (f, s): sequence_var(
                [self.job_intervals[(_j, _f, _s)] for _j, _f, _s in self.job_intervals if (_f, _s) == (f, s)],
                name='S_F{}_S{}'.format(f, s))
            for f in self.family_array[1:]
            for s in self.stage_array[1:]}

        self.family_sequence_on_machine = {
            (m, s): sequence_var(
                [self.family_intervals_on_machine[(_f, _m, _s)]
                 for _f, _m, _s in self.family_intervals_on_machine if (_m, _s) == (m, s)],
                name='S_M{}_S{}'.format(m, s),
                types=self.family_array.tolist())
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s]}

        self.model.add(end_before_start(self.job_intervals[(j, f, s - 1)], self.job_intervals[(j, f, s)])
                       for f in self.family_array[1:]
                       for j in self.jobs_in_each_family[f][1:]
                       for s in self.stage_array[2:])

        self.model.add(no_overlap(self.job_sequence_in_family[(f, s)])
                       for f in self.family_array[1:]
                       for s in self.stage_array[1:])

        self.model.add(same_sequence(self.job_sequence_in_family[(f, 1)], self.job_sequence_in_family[(f, s)])
                       for f in self.family_array[1:]
                       for s in self.stage_array[2:])

        self.model.add(span(self.family_intervals[(f, s)],
                            [self.job_intervals[(_j, _f, _s)]
                             for _j, _f, _s in self.job_intervals if (_f, _s) == (f, s)])
                       for f in self.family_array[1:]
                       for s in self.stage_array[1:])

        self.model.add(alternative(self.family_intervals[(f, s)],
                                   [self.family_intervals_on_machine[(_f, _m, _s)]
                                    for _f, _m, _s in self.family_intervals_on_machine if (_f, _s) == (f, s)])
                       for f in self.family_array[1:]
                       for s in self.stage_array[1:])

        self.model.add(first(self.family_sequence_on_machine[(m, s)], self.family_intervals_on_machine[(0, m, s)])
                       for s in self.stage_array[1:]
                       for m in self.machines_at_each_stage[s])

        self.model.add(
            no_overlap(self.family_sequence_on_machine[(m, s)], distance_matrix=self.setup_time[s], is_direct=True)
            for s in self.stage_array[1:]
            for m in self.machines_at_each_stage[s])

        # Minimize termination date
        self.model.add(minimize(max(end_of(self.family_intervals[(f, self.S)]) for f in self.family_array[1:])))

        # Solve model
        print('Solving model...')
        self.res = self.model.solve(TimeLimit=10)
        print('Solution:')
        self.res.print_solution()

    def graph(self):
        color_dict = ["WhiteSmoke", "SeaShell", "PapayaWhip", "MintCream", "LightYellow", "Ivory", "GhostWhite",
                      "FloralWhite", "Cornsilk", "Azure", "AliceBlue", "LightBlue", "LightCoral", "LightCyan",
                      "LightGoldenRodYellow", "LightGrey", "LightGreen", "LightPink", "LightSalmon", "LightSeaGreen",
                      "LightSkyBlue", "LightSlateBlue", "LightSlateGray", "LightSteelBlue", "White"]

        total_machines = np.sum(self.M_s[1:])

        fig, axes = plt.subplots(1, 1, figsize=(15, total_machines * 0.4 + 0.35 + 0.4))
        ax = plt.gca()
        # left, bottom, width, height = ax.get_position().bounds
        # ax.set_position([left, bottom, width, 0.5])

        gantt_labels = {"BT": "Blocking time", "ST": "Setup time"}
        for f in self.family_array[1:]:
            gantt_labels["F" + str(f)] = "$f_{" + str(f) + "}$"
            ax.broken_barh([(0, 0)],
                           (0, 0),
                           facecolor=color_dict[f % len(color_dict)], edgecolor="gray",
                           label=gantt_labels["F" + str(f)])
            gantt_labels["F" + str(f)] = "_nolegend_"

        y_tick = 1
        y_labels = []
        y_ticks = []
        for s in self.stage_array[1:]:
            show_m = 1
            for m in self.machines_at_each_stage[s]:
                flag = True
                y_labels.append("$s_{" + str(s) + "}m_{" + str(show_m) + "}$")
                y_ticks.append(y_tick - 1 + 0.4)
                machine_sequence_var = self.family_sequence_on_machine[(m, s)]
                machine_sequence_var_sol = self.res.get_var_solution(machine_sequence_var)

                if isinstance(machine_sequence_var_sol, CpoSequenceVarSolution):
                    f_ivs = machine_sequence_var_sol.get_value()
                    pre_family = None
                    pre_iv = None
                    for f_iv in f_ivs:
                        family = int(f_iv.get_name().split("_")[1][1:])
                        if family != 0:
                            ax.broken_barh([(pre_iv.start + pre_iv.size, self.setup_time[s][pre_family][family])],
                                           (y_tick - 1 + 0.2, 0.4),
                                           facecolor="lightgray", edgecolor="gray", label=gantt_labels["ST"])
                            gantt_labels["ST"] = "_nolegend_"

                            job_sequence_var = self.job_sequence_in_family[(family, s)]
                            job_sequence_var_sol = self.res.get_var_solution(job_sequence_var)
                            if isinstance(job_sequence_var_sol, CpoSequenceVarSolution):
                                j_ivs = job_sequence_var_sol.get_value()
                                for j_iv in j_ivs:
                                    job = int(j_iv.get_name().split("_")[1][1:])
                                    ax.broken_barh([(j_iv.start, j_iv.size)],
                                                   (y_tick - 1 + 0.2, 0.4),
                                                   facecolor=color_dict[family % len(color_dict)], edgecolor="gray",
                                                   label=gantt_labels["F" + str(family)])
                                    gantt_labels["F" + str(family)] = "_nolegend_"

                                    ax.text(j_iv.start + j_iv.size / 2.0, y_tick - 1 if flag else y_tick - 0.3,
                                            str(job), verticalalignment="center",
                                            horizontalalignment="center", color="black",
                                            fontsize=8)
                                    flag = not flag

                        else:
                            ax.broken_barh([(f_iv.start, f_iv.size)],
                                           (y_tick - 1 + 0.2, 0.4),
                                           facecolor="None", edgecolor="None")
                        pre_family = family
                        pre_iv = f_iv
                show_m += 1
                y_tick += 1

        ax.set_xlim(0, int(self.res.get_objective_value()))
        if self.res.get_objective_value() > 300:
            ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(20))
            ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))
        else:
            ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(10))
            ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(5))

        ax.tick_params(bottom=True, top=False, left=False, right=False)

        # ax.set_xlabel("Time")

        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)

        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_color('none')

        plt.legend(bbox_to_anchor=(1.005, 1.0), loc='upper left', fontsize=8)
        ax.set_title(self.problem_name.split("_", 1)[1], {'fontsize': 12})
        plt.tight_layout()
        plt.show()
        # plt.savefig(r"result/" + self.problem_name + ".png", dpi=700, bbox_inches="tight")

    def write_csv(self, csv_file):
        statistics = self.model.get_statistics()

        csv_result = {"Problem": self.problem_name,
                      "Model": self.model_name,
                      "nb_constraints": statistics.nb_constraints,
                      "nb_interval_vars": statistics.nb_interval_vars,
                      "nb_sequence_vars": statistics.nb_sequence_vars,
                      "search_status": self.res.get_search_status(),
                      "solve_status": self.res.get_solve_status(),
                      "stop_cause": self.res.get_stop_cause(),
                      "objective_gap": self.res.get_objective_gap(),
                      "objective_value": self.res.get_objective_value(),
                      "solve_time": self.res.get_solve_time()}

        self.res.get_search_status()
        self.res.get_solve_status()
        self.res.get_stop_cause()
        self.res.get_objective_gap()
        self.res.get_objective_value()
        self.res.get_solve_time()

        df = pandas.DataFrame(csv_result, index=[0])
        df.to_csv(csv_file, mode='a', index=False, header=False)
