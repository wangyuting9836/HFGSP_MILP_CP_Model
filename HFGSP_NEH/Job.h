//
// Created by wangy on 2021/12/27.
//

#ifndef HFGSP_NEH_JOB_H
#define HFGSP_NEH_JOB_H

#include <vector>
#include <numeric>

class Job
{
public:
	Job() = default;

	virtual ~Job() = default;

	int id = -1;
	std::vector<int> process_times;
	int total_process_time = 0;

	void calculate_total_process_time()
	{
		total_process_time = std::accumulate(process_times.begin(), process_times.end(), 0);
	}
};

#endif //HFGSP_NEH_JOB_H
