//
// Created by wangy on 2021/12/27.
//

#include <iostream>
#include "Solution.h"
#include "Family.h"
#include "Job.h"
#include "rand.h"


Solution::Solution(const Problem& problem) : problem(problem)
{
	/*family_sequence.emplace_back(problem.families[1]);
	family_sequence.emplace_back(problem.families[2]);
	family_sequence.emplace_back(problem.families[3]);
	family_sequence.emplace_back(problem.families[0]);

	job_sequence_in_each_family.resize(problem.num_of_families);
	for (auto famPtr: problem.families)
	{
		//family_sequence.emplace_back(famPtr);
		for (auto jobPtr: famPtr->jobs)
		{
			job_sequence_in_each_family[famPtr->id].emplace_back(jobPtr);
		}
	}*/

	/*const std::vector<Family*>& families = problem.families;

	family_sequence.emplace_back(families[2]);
	family_sequence.emplace_back(families[3]);
	family_sequence.emplace_back(families[0]);
	family_sequence.emplace_back(families[1]);
	job_sequence_in_each_family.resize(problem.num_of_families);

	job_sequence_in_each_family[0].emplace_back(families[0]->jobs[1]);
	job_sequence_in_each_family[0].emplace_back(families[0]->jobs[7]);
	job_sequence_in_each_family[0].emplace_back(families[0]->jobs[5]);
	job_sequence_in_each_family[0].emplace_back(families[0]->jobs[4]);
	job_sequence_in_each_family[0].emplace_back(families[0]->jobs[2]);
	job_sequence_in_each_family[0].emplace_back(families[0]->jobs[6]);
	job_sequence_in_each_family[0].emplace_back(families[0]->jobs[3]);
	job_sequence_in_each_family[0].emplace_back(families[0]->jobs[0]);

	job_sequence_in_each_family[1].emplace_back(families[1]->jobs[3]);
	job_sequence_in_each_family[1].emplace_back(families[1]->jobs[5]);
	job_sequence_in_each_family[1].emplace_back(families[1]->jobs[4]);
	job_sequence_in_each_family[1].emplace_back(families[1]->jobs[2]);
	job_sequence_in_each_family[1].emplace_back(families[1]->jobs[1]);
	job_sequence_in_each_family[1].emplace_back(families[1]->jobs[0]);

	job_sequence_in_each_family[2].emplace_back(families[2]->jobs[0]);
	job_sequence_in_each_family[2].emplace_back(families[2]->jobs[1]);

	job_sequence_in_each_family[3].emplace_back(families[3]->jobs[1]);
	job_sequence_in_each_family[3].emplace_back(families[3]->jobs[0]);*/


	/*for (auto famPtr: problem.families)
	{
		family_sequence.emplace_back(famPtr);
		for (auto jobPtr: famPtr->jobs)
		{
			job_sequence_in_each_family[famPtr->id].emplace_back(jobPtr);
		}
		shuffle(std::begin(job_sequence_in_each_family[famPtr->id]),
				std::end(job_sequence_in_each_family[famPtr->id]),
				rand_generator());
	}
	shuffle(std::begin(family_sequence), std::end(family_sequence), rand_generator());*/
}


int Solution::calculate_make_span()
{
	if (family_sequence.empty())
	{
		return 0;
	}
	int num_of_stages = problem.num_of_stages;
	int num_of_jobs = problem.num_of_jobs;

	std::vector<std::vector<int>> machine_ready_time(num_of_stages);
	std::vector<std::vector<Family*>> last_family_on_machine(num_of_stages);
	std::vector<std::vector<int>> complete_time(num_of_jobs, std::vector<int>(num_of_stages, 0));

	decode_result.clear();
	decode_result.resize(num_of_stages);

	for (int s = 0; s < num_of_stages; ++s)
	{
		machine_ready_time[s].resize(problem.num_of_machines_at_each_stage[s], 0);
		last_family_on_machine[s].resize(problem.num_of_machines_at_each_stage[s], nullptr);
		decode_result[s].resize(problem.num_of_machines_at_each_stage[s]);
	}

	for (auto fam_ptr: family_sequence)
	{
		for (int s = 0; s < problem.num_of_stages; ++s)
		{
			int min_available_time = INT_MAX;
			int select_machine = -1;
			for (int m = 0; m < problem.num_of_machines_at_each_stage[s]; ++m)
			{
				Family* pre_fam_ptr = last_family_on_machine[s][m];
				int cur_machine_available_time;
				if (pre_fam_ptr == nullptr)
				{
					cur_machine_available_time = machine_ready_time[s][m] + fam_ptr->setup_times[s][fam_ptr->id];
				}
				else
				{
					cur_machine_available_time = machine_ready_time[s][m] + pre_fam_ptr->setup_times[s][fam_ptr->id];
				}
				if (min_available_time > cur_machine_available_time)
				{
					min_available_time = cur_machine_available_time;
					select_machine = m;
				}
			}
			decode_result[s][select_machine].emplace_back(
					-1, -1, machine_ready_time[s][select_machine], min_available_time);
			machine_ready_time[s][select_machine] = min_available_time;

			for (auto job_ptr: job_sequence_in_each_family[fam_ptr->id])
			{
				machine_ready_time[s][select_machine] =
						std::max(machine_ready_time[s][select_machine],
								s == 0 ? 0 : complete_time[job_ptr->id][s - 1]) +
						job_ptr->process_times[s];
				complete_time[job_ptr->id][s] = machine_ready_time[s][select_machine];
				decode_result[s][select_machine].emplace_back(
						fam_ptr->id, job_ptr->id, complete_time[job_ptr->id][s] - job_ptr->process_times[s],
						complete_time[job_ptr->id][s]);
			}
			last_family_on_machine[s][select_machine] = fam_ptr;
		}
	}

	make_span = *std::max_element(std::begin(machine_ready_time[num_of_stages - 1]),
			std::end(machine_ready_time[num_of_stages - 1]));

	return make_span;
}

int Solution::neh_fam_1()
{
	std::vector<Family*> tmp_families = problem.families;

	job_sequence_in_each_family.resize(problem.num_of_families);

	for (auto fam_ptr: problem.families)
	{
		for (auto jobPtr: fam_ptr->jobs)
		{
			job_sequence_in_each_family[fam_ptr->id].emplace_back(jobPtr);
		}
	}

	std::sort(std::begin(tmp_families), std::end(tmp_families), [](auto fam_prt1, auto fam_ptr2)
	{
		return fam_prt1->total_process_time > fam_ptr2->total_process_time;
	});

	int min_span;
	for (auto fam_ptr: tmp_families)
	{
		min_span = INT_MAX;
		int best_pos = -1;
		for (int pos = 0; pos < family_sequence.size() + 1; ++pos)
		{
			family_sequence.insert(std::begin(family_sequence) + pos, fam_ptr);
			int span = calculate_make_span();
			if (min_span > span)
			{
				min_span = span;
				best_pos = pos;
			}
			family_sequence.erase(std::begin(family_sequence) + pos);
		}
		family_sequence.insert(std::begin(family_sequence) + best_pos, fam_ptr);
	}
	return min_span;
}

int Solution::neh_fam_2()
{
	std::vector<Family*> tmp_families = problem.families;

	job_sequence_in_each_family.resize(problem.num_of_families);

	for (auto fam_ptr: problem.families)
	{
		for (auto jobPtr: fam_ptr->jobs)
		{
			job_sequence_in_each_family[fam_ptr->id].emplace_back(jobPtr);
		}
		std::sort(std::begin(job_sequence_in_each_family[fam_ptr->id]),
				std::end(job_sequence_in_each_family[fam_ptr->id]), [](auto job_prt1, auto job_ptr2)
				{
					return job_prt1->total_process_time > job_ptr2->total_process_time;
				});
	}

	std::sort(std::begin(tmp_families), std::end(tmp_families), [](auto fam_prt1, auto fam_ptr2)
	{
		return fam_prt1->total_process_time > fam_ptr2->total_process_time;
	});

	int min_span;
	for (auto fam_ptr: tmp_families)
	{
		min_span = INT_MAX;
		int best_pos = -1;
		for (int pos = 0; pos < family_sequence.size() + 1; ++pos)
		{
			family_sequence.insert(std::begin(family_sequence) + pos, fam_ptr);
			int span = calculate_make_span();
			if (min_span > span)
			{
				min_span = span;
				best_pos = pos;
			}
			family_sequence.erase(std::begin(family_sequence) + pos);
		}
		family_sequence.insert(std::begin(family_sequence) + best_pos, fam_ptr);
	}
	return min_span;
}

int Solution::neh_fam_3()
{
	std::vector<Family*> tmp_families = problem.families;

	job_sequence_in_each_family.resize(problem.num_of_families);

	for (auto fam_ptr: problem.families)
	{
		for (auto jobPtr: fam_ptr->jobs)
		{
			job_sequence_in_each_family[fam_ptr->id].emplace_back(jobPtr);
		}
//		shuffle(std::begin(job_sequence_in_each_family[fam_ptr->id]),
//				std::end(job_sequence_in_each_family[fam_ptr->id]),
//				rand_generator());
		std::sort(std::begin(job_sequence_in_each_family[fam_ptr->id]),
				std::end(job_sequence_in_each_family[fam_ptr->id]), [](auto job_prt1, auto job_ptr2)
				{
					return job_prt1->total_process_time > job_ptr2->total_process_time;
				});
	}

	std::sort(std::begin(tmp_families), std::end(tmp_families), [](auto fam_prt1, auto fam_ptr2)
	{
		return fam_prt1->total_process_time > fam_ptr2->total_process_time;
	});

	int min_span;
	for (auto fam_ptr: tmp_families)
	{
		min_span = INT_MAX;
		int best_pos = -1;
		for (int pos = 0; pos < family_sequence.size() + 1; ++pos)
		{
			family_sequence.insert(std::begin(family_sequence) + pos, fam_ptr);
			int span = calculate_make_span();
			if (min_span > span)
			{
				min_span = span;
				best_pos = pos;
			}
			family_sequence.erase(std::begin(family_sequence) + pos);
		}
		family_sequence.insert(std::begin(family_sequence) + best_pos, fam_ptr);
	}
	return min_span;
}


int Solution::neh_fam_job()
{
	std::vector<Family*> tmp_families = problem.families;

	job_sequence_in_each_family.resize(problem.num_of_families);

	for (auto fam_ptr: problem.families)
	{
		for (auto jobPtr: fam_ptr->jobs)
		{
			job_sequence_in_each_family[fam_ptr->id].emplace_back(jobPtr);
		}
		std::sort(std::begin(job_sequence_in_each_family[fam_ptr->id]),
				std::end(job_sequence_in_each_family[fam_ptr->id]), [](auto job_prt1, auto job_ptr2)
				{
					return job_prt1->total_process_time < job_ptr2->total_process_time;
				});
	}

	std::sort(std::begin(tmp_families), std::end(tmp_families), [](auto fam_prt1, auto fam_ptr2)
	{
		return fam_prt1->total_process_time > fam_ptr2->total_process_time;
	});

	int min_span;
	for (auto fam_ptr: tmp_families)
	{
		min_span = INT_MAX;
		int best_pos = -1;
		for (int pos = 0; pos < family_sequence.size() + 1; ++pos)
		{
			family_sequence.insert(std::begin(family_sequence) + pos, fam_ptr);
			int span = calculate_make_span();
			if (min_span > span)
			{
				min_span = span;
				best_pos = pos;
			}
			family_sequence.erase(std::begin(family_sequence) + pos);
		}
		family_sequence.insert(std::begin(family_sequence) + best_pos, fam_ptr);
	}

	std::vector<std::vector<Job*>> temp_job_sequence_in_each_family = job_sequence_in_each_family;

	for (auto fam_ptr: family_sequence)
	{
		job_sequence_in_each_family[fam_ptr->id].clear();
	}
	for (auto fam_ptr: family_sequence)
	{
		std::vector<Job*> tmp_jobs = temp_job_sequence_in_each_family[fam_ptr->id];
		//job_sequence_in_each_family[fam_ptr->id].clear();

		std::sort(std::begin(tmp_jobs), std::end(tmp_jobs), [](auto job_prt1, auto job_ptr2)
		{
			return job_prt1->total_process_time > job_ptr2->total_process_time;
		});

		for (auto job_ptr: tmp_jobs)
		{
			min_span = INT_MAX;
			int best_pos = -1;
			for (int pos = 0; pos < job_sequence_in_each_family[fam_ptr->id].size() + 1; ++pos)
			{
				job_sequence_in_each_family[fam_ptr->id].insert(
						std::begin(job_sequence_in_each_family[fam_ptr->id]) + pos, job_ptr);
				int span = calculate_make_span();
				if (min_span > span)
				{
					min_span = span;
					best_pos = pos;
				}
				job_sequence_in_each_family[fam_ptr->id].erase(
						std::begin(job_sequence_in_each_family[fam_ptr->id]) + pos);
			}
			job_sequence_in_each_family[fam_ptr->id].insert(
					std::begin(job_sequence_in_each_family[fam_ptr->id]) + best_pos, job_ptr);
		}
	}

	return min_span;
}


