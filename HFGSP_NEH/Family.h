//
// Created by wangy on 2021/12/27.
//

#ifndef HFGSP_NEH_FAMILY_H
#define HFGSP_NEH_FAMILY_H

#include <vector>
#include <istream>
#include "Job.h"

class Family
{
public:

	Family() = default;

	virtual ~Family()
	{
		for (auto job_ptr: jobs)
		{
			delete job_ptr;
		}
	};

	int id = -1;
	std::vector<Job*> jobs;
	std::vector<std::vector<int>> setup_times;
	int num_of_jobs = 0;
	int total_process_time = 0; // all the operation times for the jobs in a Family

	void set_total_process_time()
	{
		for (auto job_ptr: jobs)
		{
			total_process_time += job_ptr->total_process_time;
		}
	}

};


#endif //HFGSP_NEH_FAMILY_H
