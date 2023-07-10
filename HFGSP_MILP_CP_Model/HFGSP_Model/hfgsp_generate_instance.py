# Hybrid Permutation Flowshop Group Scheduling Problem
import os
import random


def generate_instance():
    minJobsInFamily = 1
    maxJobsInFamily = 10
    minMachinesInStage = 1
    maxMachinesInStage = 3
    minProcessingTime = 1
    maxProcessingTime = 10
    minSetupTime = 1
    maxSetupTimeArray = [20, 50, 100]
    # instanceRepeat = 5

    FamilyArray = [2, 4, 6, 8, 10]
    StageArray = [2, 3, 4, 5]
    SetupTypeArray = [0, 1, 2]
    # count_files = 1
    instanceFileName = os.path.dirname(os.path.abspath(__file__)) + '/data/InstanceFileNameList.txt'
    ofile1 = open(instanceFileName, "w")
    for famlily in FamilyArray:
        for stage in StageArray:
            setupType = SetupTypeArray[1]
            filename = "HFG_" + str(famlily) + "_" + str(stage) + ".txt"

            ofile1.write(filename + "\n")

            filename = os.path.dirname(os.path.abspath(__file__)) + '/data/' + filename
            ofile2 = open(filename, "w")

            ofile2.write("Families:")
            ofile2.write(str(famlily) + "\n")
            ofile2.write("Stages:")
            ofile2.write(str(stage) + "\n")

            MachinesInEachStage = []
            for s in range(0, stage):
                MachinesInEachStage.append(random.randint(minMachinesInStage, maxMachinesInStage))

            isExistsGreater1 = False
            for machineNum in MachinesInEachStage:
                if machineNum > 1:
                    isExistsGreater1 = True
                    break

            if not isExistsGreater1:
                MachinesInEachStage[random.randint(0, stage - 1)] = 2

            ofile2.write("Number of Machines at each Stage:\n")
            for s in range(0, stage):
                ofile2.write(str(MachinesInEachStage[s]) + "\t")
            ofile2.write("\n")

            ofile2.write("Machines at each Stage:\n")
            totalMachineNum = 0
            for s in range(0, stage):
                ofile2.write(str(s + 1) + "\t")
                for m in range(0, MachinesInEachStage[s]):
                    ofile2.write(str(totalMachineNum + 1) + "\t")
                    totalMachineNum = totalMachineNum + 1
                ofile2.write("\n")

            ofile2.write("Total number of machines:")
            ofile2.write(str(totalMachineNum) + "\n")

            ofile2.write("Number of Jobs in each Family:\n")
            JobsinAllFamily = []
            totalJobNum = 0
            for fam in range(0, famlily):
                nJobsinFamily = random.randint(minJobsInFamily, maxJobsInFamily)
                JobsinEachFamily = []
                for x in range(0, nJobsinFamily):
                    JobsinEachFamily.append(totalJobNum + x)
                totalJobNum = totalJobNum + nJobsinFamily
                JobsinAllFamily.append(JobsinEachFamily)
                ofile2.write(str(nJobsinFamily) + "\t")
            ofile2.write("\n")

            ofile2.write("Jobs in each Family:\n")
            for fam in range(0, famlily):
                ofile2.write(str(fam + 1) + "\t")
                for job in JobsinAllFamily[fam]:
                    ofile2.write(str(job + 1) + "\t")
                ofile2.write("\n")

            ofile2.write("Total number of jobs:")
            ofile2.write(str(totalJobNum) + "\n")

            ofile2.write("Processing times of jobs:\n")
            for job in range(0, totalJobNum):
                for s in range(0, stage):
                    ofile2.write(str(random.randint(minProcessingTime, maxProcessingTime)) + "\t")
                ofile2.write("\n")

            # ofile2.write("Setup times between Families, where [f][f] represents initial setup time\n")
            maxSetupTime = maxSetupTimeArray[setupType]
            ofile2.write("Setup times:\n")
            for s in range(0, stage):
                for fam1 in range(0, famlily):
                    for fam2 in range(0, famlily):
                        ofile2.write(str(random.randint(minSetupTime, maxSetupTime)) + "\t")
                    ofile2.write("\n")

            ofile2.close()
    print("end")


generate_instance()
