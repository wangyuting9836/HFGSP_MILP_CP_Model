//
// Created by wangy on 2021/12/27.
//

#ifndef HFGSP_NEH_SOLUTION_H
#define HFGSP_NEH_SOLUTION_H

#include <vector>
#include "Problem.h"

class Family;

class Job;

struct GanttBar
{
	int family_id;
	int job_id;
	int start_time;
	int finish_time;

	GanttBar(int familyId, int jobId, int startTime, int finishTime) : family_id(familyId), job_id(jobId),
																	   start_time(startTime), finish_time(finishTime)
	{
	}
};

class Solution
{
public:
	explicit Solution(const Problem& problem);

	int neh_fam();
	int neh_fam_job();
	int calculate_make_span();

	const Problem& problem;

	std::vector<Family*> family_sequence; //Family sequence
	std::vector<std::vector<Job*>> job_sequence_in_each_family; //Job sequence in each Family

	int make_span{};

	std::vector<std::vector<std::vector<GanttBar>>> decode_result;

};

#endif //HFGSP_NEH_SOLUTION_H
