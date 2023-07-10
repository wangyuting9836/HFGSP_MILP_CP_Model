import csv
import datetime

from HFGSP_Model.hfgsp_milp_model import HFGSPMILPModel


# B.a.1
def milp_model1(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model1")
    m.creat_var_c()
    m.arrangement_of_families1()
    m.arrangement_of_jobs_in_the_family1()
    m.process_requirements_between_families1()
    m.process_requirements_between_jobs_from_same_family1()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model2(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model2")
    m.creat_var_c()
    m.arrangement_of_families1()
    m.arrangement_of_jobs_in_the_family2()
    m.process_requirements_between_families1()
    m.process_requirements_between_jobs_from_same_family2()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model3(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model3")
    m.creat_var_c()
    m.arrangement_of_families1()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families1()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model4(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model4")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families1()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families1()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model5(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model5")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families1()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families1()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model6(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model6")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families1()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families1()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model7(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model7")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families1()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families1()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model8(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model8")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families1()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families2()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model9(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model9")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families1()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families2()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model10(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model10")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families1()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families2()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model11(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model11")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families1()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families2()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model12(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model12")
    m.creat_var_a()
    m.arrangement_of_families1()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families2()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages2()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


# B.a.2
def milp_model13(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model13")
    m.creat_var_c()
    m.arrangement_of_families2()
    m.arrangement_of_jobs_in_the_family1()
    m.process_requirements_between_families3()
    m.process_requirements_between_jobs_from_same_family1()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model14(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model14")
    m.creat_var_c()
    m.arrangement_of_families2()
    m.arrangement_of_jobs_in_the_family2()
    m.process_requirements_between_families3()
    m.process_requirements_between_jobs_from_same_family2()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model15(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model15")
    m.creat_var_c()
    m.arrangement_of_families2()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families3()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model16(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model16")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families2()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families3()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model17(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model17")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families2()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families3()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model18(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model18")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families2()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families3()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model19(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model19")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families2()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families3()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model20(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model20")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families2()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families4()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model21(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model21")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families2()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families4()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model22(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model22")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families2()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families4()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model23(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model23")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families2()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families4()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model24(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model24")
    m.creat_var_a()
    m.arrangement_of_families2()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families4()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages2()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


# B.a.3
def milp_model25(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model25")
    m.creat_var_c()
    m.arrangement_of_families3()
    m.arrangement_of_jobs_in_the_family1()
    m.process_requirements_between_families5()
    m.process_requirements_between_jobs_from_same_family1()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model26(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model26")
    m.creat_var_c()
    m.arrangement_of_families3()
    m.arrangement_of_jobs_in_the_family2()
    m.process_requirements_between_families5()
    m.process_requirements_between_jobs_from_same_family2()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model27(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model27")
    m.creat_var_c()
    m.arrangement_of_families3()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families5()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model28(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model28")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families3()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families5()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model29(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model29")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families3()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families5()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model30(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model30")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families3()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families5()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model31(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model31")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families3()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families5()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model32(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model32")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families3()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families6()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model33(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model33")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families3()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families6()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model34(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model34")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families3()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families6()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model35(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model35")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families3()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families6()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model36(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model36")
    m.creat_var_a()
    m.arrangement_of_families3()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families6()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages2()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


# B.a.4
def milp_model37(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model37")
    m.creat_var_c()
    m.arrangement_of_families4()
    m.arrangement_of_jobs_in_the_family1()
    m.process_requirements_between_families7()
    m.process_requirements_between_jobs_from_same_family1()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model38(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model38")
    m.creat_var_c()
    m.arrangement_of_families4()
    m.arrangement_of_jobs_in_the_family2()
    m.process_requirements_between_families7()
    m.process_requirements_between_jobs_from_same_family2()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model39(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model39")
    m.creat_var_c()
    m.arrangement_of_families4()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families7()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model40(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model40")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families4()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families7()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model41(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model41")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families4()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families7()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model42(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model42")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families4()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families7()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model43(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model43")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families4()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families7()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model44(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model44")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families4()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families8()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model45(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model45")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families4()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families8()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model46(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model46")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families4()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families8()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model47(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model47")
    m.creat_var_c()
    m.creat_var_a()
    m.arrangement_of_families4()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families8()
    m.process_requirements_between_jobs_from_same_family3()
    m.process_requirements_between_adjacent_stages2()
    m.relationship_between_the_decision_variables_of_completion_time1()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model48(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model48")
    m.creat_var_a()
    m.arrangement_of_families4()
    m.arrangement_of_jobs_in_the_family3()
    m.process_requirements_between_families8()
    m.process_requirements_between_jobs_from_same_family4()
    m.process_requirements_between_adjacent_stages2()
    m.makespan_constraint2()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


# B.a.5
def milp_model49(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model49")
    m.creat_var_c()
    m.arrangement_of_families5()
    m.arrangement_of_jobs_in_the_family4()
    m.process_requirements_between_families9()
    m.process_requirements_between_jobs_from_same_family5()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model50(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model50")
    m.creat_var_c()
    m.creat_var_b()
    m.arrangement_of_families5()
    m.arrangement_of_jobs_in_the_family4()
    m.process_requirements_between_families9()
    m.process_requirements_between_jobs_from_same_family6()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time2()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model51(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model51")
    m.creat_var_c()
    m.creat_var_b()
    m.arrangement_of_families5()
    m.arrangement_of_jobs_in_the_family4()
    m.process_requirements_between_families9()
    m.process_requirements_between_jobs_from_same_family6()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time2()
    m.makespan_constraint3()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model52(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model52")
    m.creat_var_c()
    m.creat_var_b()
    m.arrangement_of_families5()
    m.arrangement_of_jobs_in_the_family4()
    m.process_requirements_between_families9()
    m.process_requirements_between_jobs_from_same_family6()
    m.process_requirements_between_adjacent_stages3()
    m.relationship_between_the_decision_variables_of_completion_time2()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model53(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model53")
    m.creat_var_c()
    m.creat_var_b()
    m.arrangement_of_families5()
    m.arrangement_of_jobs_in_the_family4()
    m.process_requirements_between_families9()
    m.process_requirements_between_jobs_from_same_family6()
    m.process_requirements_between_adjacent_stages3()
    m.relationship_between_the_decision_variables_of_completion_time2()
    m.makespan_constraint3()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model54(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model54")
    m.creat_var_c()
    m.creat_var_b()
    m.arrangement_of_families5()
    m.arrangement_of_jobs_in_the_family4()
    m.process_requirements_between_families10()
    m.process_requirements_between_jobs_from_same_family5()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time2()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model55(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model55")
    m.creat_var_c()
    m.creat_var_b()
    m.arrangement_of_families5()
    m.arrangement_of_jobs_in_the_family4()
    m.process_requirements_between_families10()
    m.process_requirements_between_jobs_from_same_family5()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time2()
    m.makespan_constraint3()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model56(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model56")
    m.creat_var_c()
    m.creat_var_b()
    m.arrangement_of_families5()
    m.arrangement_of_jobs_in_the_family4()
    m.process_requirements_between_families10()
    m.process_requirements_between_jobs_from_same_family5()
    m.process_requirements_between_adjacent_stages3()
    m.relationship_between_the_decision_variables_of_completion_time2()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model57(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model57")
    m.creat_var_c()
    m.creat_var_b()
    m.arrangement_of_families5()
    m.arrangement_of_jobs_in_the_family4()
    m.process_requirements_between_families10()
    m.process_requirements_between_jobs_from_same_family5()
    m.process_requirements_between_adjacent_stages3()
    m.relationship_between_the_decision_variables_of_completion_time2()
    m.makespan_constraint3()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model58(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model58")
    m.creat_var_b()
    m.arrangement_of_families5()
    m.arrangement_of_jobs_in_the_family4()
    m.process_requirements_between_families10()
    m.process_requirements_between_jobs_from_same_family6()
    m.process_requirements_between_adjacent_stages3()
    m.makespan_constraint3()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


# B.a.6
def milp_model59(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model59")
    m.creat_var_c()
    m.arrangement_of_families6()
    m.arrangement_of_jobs_in_the_family5()
    m.process_requirements_between_families11()
    m.process_requirements_between_jobs_from_same_family7()
    m.process_requirements_between_adjacent_stages1()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model60(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model60")
    m.creat_var_c()
    m.creat_var_b1()
    m.arrangement_of_families6()
    m.arrangement_of_jobs_in_the_family5()
    m.process_requirements_between_families11()
    m.process_requirements_between_jobs_from_same_family8()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time3()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model61(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model61")
    m.creat_var_c()
    m.creat_var_b1()
    m.arrangement_of_families6()
    m.arrangement_of_jobs_in_the_family5()
    m.process_requirements_between_families11()
    m.process_requirements_between_jobs_from_same_family8()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time3()
    m.makespan_constraint4()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model62(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model62")
    m.creat_var_c()
    m.creat_var_b1()
    m.arrangement_of_families6()
    m.arrangement_of_jobs_in_the_family5()
    m.process_requirements_between_families11()
    m.process_requirements_between_jobs_from_same_family8()
    m.process_requirements_between_adjacent_stages4()
    m.relationship_between_the_decision_variables_of_completion_time3()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model63(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model63")
    m.creat_var_c()
    m.creat_var_b1()
    m.arrangement_of_families6()
    m.arrangement_of_jobs_in_the_family5()
    m.process_requirements_between_families11()
    m.process_requirements_between_jobs_from_same_family8()
    m.process_requirements_between_adjacent_stages4()
    m.relationship_between_the_decision_variables_of_completion_time3()
    m.makespan_constraint4()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model64(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model64")
    m.creat_var_c()
    m.creat_var_b1()
    m.arrangement_of_families6()
    m.arrangement_of_jobs_in_the_family5()
    m.process_requirements_between_families12()
    m.process_requirements_between_jobs_from_same_family7()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time3()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model65(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model65")
    m.creat_var_c()
    m.creat_var_b1()
    m.arrangement_of_families6()
    m.arrangement_of_jobs_in_the_family5()
    m.process_requirements_between_families12()
    m.process_requirements_between_jobs_from_same_family7()
    m.process_requirements_between_adjacent_stages1()
    m.relationship_between_the_decision_variables_of_completion_time3()
    m.makespan_constraint4()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model66(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model66")
    m.creat_var_c()
    m.creat_var_b1()
    m.arrangement_of_families6()
    m.arrangement_of_jobs_in_the_family5()
    m.process_requirements_between_families12()
    m.process_requirements_between_jobs_from_same_family7()
    m.process_requirements_between_adjacent_stages4()
    m.relationship_between_the_decision_variables_of_completion_time3()
    m.makespan_constraint1()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model67(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model67")
    m.creat_var_c()
    m.creat_var_b1()
    m.arrangement_of_families6()
    m.arrangement_of_jobs_in_the_family5()
    m.process_requirements_between_families12()
    m.process_requirements_between_jobs_from_same_family7()
    m.process_requirements_between_adjacent_stages4()
    m.relationship_between_the_decision_variables_of_completion_time3()
    m.makespan_constraint4()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


def milp_model68(filename, csv_result_file):
    m = HFGSPMILPModel(filename)
    m.creat_model("milp_model68")
    m.creat_var_b1()
    m.arrangement_of_families6()
    m.arrangement_of_jobs_in_the_family5()
    m.process_requirements_between_families12()
    m.process_requirements_between_jobs_from_same_family8()
    m.process_requirements_between_adjacent_stages4()
    m.makespan_constraint4()
    m.set_objective()
    m.print_vars()
    m.write_csv(csv_result_file)


if __name__ == '__main__':
    header = ("Problem",
              "Model",
              "Current optimization status",
              "Indicates whether the model is a MIP",
              "Indicates whether the model has multiple objectives",
              "Current relative MIP optimality gap",
              "Runtime for most recent optimization",
              "Work spent on most recent optimization",
              "Number of variables",
              "Number of integer variables",
              "NumBinVars",
              "Number of linear constraints",
              "Number of SOS constraints",
              "Number of quadratic constraints",
              "Number of general constraints",
              "Number of non-zero coefficients in the constraint matrix",
              "Number of non-zero coefficients in the constraint matrix (in double format)",
              "Number of non-zero quadratic objective terms",
              "Number of non-zero terms in quadratic constraints",
              "Number of stored solutions",
              "Number of simplex iterations performed in most recent optimization",
              "Number of barrier iterations performed in most recent optimization",
              "Number of branch-and-cut nodes explored in most recent optimization",
              "Number of open branch-and-cut nodes at the end of most recent optimization",
              "Maximum linear objective coefficient (in absolute value)",
              "MinObjCoeff Minimum (non-zero) linear objective coefficient (in absolute value)",
              "Maximum constraint right-hand side (in absolute value)",
              "Minimum (non-zero) constraint right-hand side (in absolute value)",
              "Number of objectives",
              "Number of solutions Gurobi found",
              "PoolObjVal")

    csv_file = 'result/result' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv'

    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    # instanceFile = open(os.path.dirname(os.path.abspath(__file__)) + '/data/InstanceFileNameList.txt')
    # fileNames = instanceFile.readlines()
    fileNames = ["HFG_4_2.txt"]
    for fileName in fileNames:
        # print("\033[0;31;40m" + fileName + "\033[0m")
        print(fileName)
        milp_model1(fileName.replace('\n', ''), csv_file)
        milp_model2(fileName.replace('\n', ''), csv_file)
        milp_model3(fileName.replace('\n', ''), csv_file)
        milp_model4(fileName.replace('\n', ''), csv_file)
        milp_model5(fileName.replace('\n', ''), csv_file)
        milp_model6(fileName.replace('\n', ''), csv_file)
        milp_model7(fileName.replace('\n', ''), csv_file)
        milp_model8(fileName.replace('\n', ''), csv_file)
        milp_model9(fileName.replace('\n', ''), csv_file)
        milp_model10(fileName.replace('\n', ''), csv_file)
        milp_model11(fileName.replace('\n', ''), csv_file)
        milp_model12(fileName.replace('\n', ''), csv_file)
        milp_model13(fileName.replace('\n', ''), csv_file)
        milp_model14(fileName.replace('\n', ''), csv_file)
        milp_model15(fileName.replace('\n', ''), csv_file)
        milp_model16(fileName.replace('\n', ''), csv_file)
        milp_model17(fileName.replace('\n', ''), csv_file)
        milp_model18(fileName.replace('\n', ''), csv_file)
        milp_model19(fileName.replace('\n', ''), csv_file)
        milp_model20(fileName.replace('\n', ''), csv_file)
        milp_model21(fileName.replace('\n', ''), csv_file)
        milp_model22(fileName.replace('\n', ''), csv_file)
        milp_model23(fileName.replace('\n', ''), csv_file)
        milp_model24(fileName.replace('\n', ''), csv_file)
        milp_model25(fileName.replace('\n', ''), csv_file)
        milp_model26(fileName.replace('\n', ''), csv_file)
        milp_model27(fileName.replace('\n', ''), csv_file)
        milp_model28(fileName.replace('\n', ''), csv_file)
        milp_model29(fileName.replace('\n', ''), csv_file)
        milp_model30(fileName.replace('\n', ''), csv_file)
        milp_model31(fileName.replace('\n', ''), csv_file)
        milp_model32(fileName.replace('\n', ''), csv_file)
        milp_model33(fileName.replace('\n', ''), csv_file)
        milp_model34(fileName.replace('\n', ''), csv_file)
        milp_model35(fileName.replace('\n', ''), csv_file)
        milp_model36(fileName.replace('\n', ''), csv_file)
        milp_model37(fileName.replace('\n', ''), csv_file)
        milp_model38(fileName.replace('\n', ''), csv_file)
        milp_model39(fileName.replace('\n', ''), csv_file)
        milp_model40(fileName.replace('\n', ''), csv_file)
        milp_model41(fileName.replace('\n', ''), csv_file)
        milp_model42(fileName.replace('\n', ''), csv_file)
        milp_model43(fileName.replace('\n', ''), csv_file)
        milp_model44(fileName.replace('\n', ''), csv_file)
        milp_model45(fileName.replace('\n', ''), csv_file)
        milp_model46(fileName.replace('\n', ''), csv_file)
        milp_model47(fileName.replace('\n', ''), csv_file)
        milp_model48(fileName.replace('\n', ''), csv_file)
        milp_model49(fileName.replace('\n', ''), csv_file)
        milp_model50(fileName.replace('\n', ''), csv_file)
        milp_model51(fileName.replace('\n', ''), csv_file)
        milp_model52(fileName.replace('\n', ''), csv_file)
        milp_model53(fileName.replace('\n', ''), csv_file)
        milp_model54(fileName.replace('\n', ''), csv_file)
        milp_model55(fileName.replace('\n', ''), csv_file)
        milp_model56(fileName.replace('\n', ''), csv_file)
        milp_model57(fileName.replace('\n', ''), csv_file)
        milp_model58(fileName.replace('\n', ''), csv_file)
        milp_model59(fileName.replace('\n', ''), csv_file)
        milp_model60(fileName.replace('\n', ''), csv_file)
        milp_model61(fileName.replace('\n', ''), csv_file)
        milp_model62(fileName.replace('\n', ''), csv_file)
        milp_model63(fileName.replace('\n', ''), csv_file)
        milp_model64(fileName.replace('\n', ''), csv_file)
        milp_model65(fileName.replace('\n', ''), csv_file)
        milp_model66(fileName.replace('\n', ''), csv_file)
        milp_model67(fileName.replace('\n', ''), csv_file)
        milp_model68(fileName.replace('\n', ''), csv_file)
