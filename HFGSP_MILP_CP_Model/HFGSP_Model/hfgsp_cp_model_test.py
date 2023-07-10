import csv
import datetime
import os

from HFGSP_Model.hfgsp_cp_model import HFGSPCPModel


def cp_model(filename, csv_result_file):
    m = HFGSPCPModel(filename)
    m.creat_model("cp_model")
    m.write_csv(csv_result_file)
    m.graph()


if __name__ == '__main__':
    header = ("Problem",
              "Model",
              "nb_constraints",
              "nb_interval_vars",
              "nb_sequence_vars",
              "search_status",
              "solve_status",
              "stop_cause",
              "objective_gap",
              "objective_value",
              "solve_time")

    csv_file = 'result/result' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv'

    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

    instanceFile = open(os.path.dirname(os.path.abspath(__file__)) + '/data/InstanceFileNameList.txt')
    fileNames = instanceFile.readlines()
    for fileName in fileNames:
        fileName = fileName.replace("\n", "")
        print(fileName)
        cp_model(fileName, csv_file)
