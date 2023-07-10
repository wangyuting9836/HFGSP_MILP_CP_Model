//
// Created by wangy on 2021/12/12.
//

#include <fstream>
#include <sstream>
#include <iostream>
#include <numeric>
#include <cassert>
#include <algorithm>
#include <unordered_map>

#include "rand.h"
#include "Problem.h"
#include "Family.h"
#include "Job.h"

using namespace std;

void Problem::read_instance_filename_list(const std::string& dir)
{
	instance_filename_list.clear();
	ifstream i_file;
	i_file.open(dir + R"(\InstanceFileNameList.txt)");
	while (true)
	{
		int x;
		string FName;
		i_file >> FName;
		if (i_file.peek() != EOF)
		{
			instance_filename_list.push_back(dir + R"(\)" + FName);
		}
		else
			break;
	}
	i_file.close();
}

void Problem::read_comment(ifstream& i_file, string& comment)
{
	while (getline(i_file, comment))
	{
		size_t n = comment.find_last_not_of(" \r\n\t");
		if (n != string::npos)
		{
			comment.erase(n + 1, comment.size() - n);
		}
		n = comment.find_first_not_of(" \r\n\t");
		if (n != string::npos)
		{
			comment.erase(0, n);
		}
		if (!comment.empty() && comment != "\t")
		{
			break;
		}
	}
}

void Problem::read_instance(const std::string& file_name)
{
	destroy_family_job();

	ifstream i_file;
	i_file.open(file_name);
	string str;
	int data;

	read_comment(i_file, str);
	i_file >> num_of_families;

	read_comment(i_file, str);
	i_file >> num_of_stages;

	read_comment(i_file, str);
	num_of_machines_at_each_stage.clear();
	for (int s = 0; s < num_of_stages; ++s)
	{
		i_file >> data;
		num_of_machines_at_each_stage.emplace_back(data);
	}

	read_comment(i_file, str);
	for (int s = 0; s < num_of_stages; ++s)
	{
		std::getline(i_file, str);
	}

	read_comment(i_file, str);
	std::getline(i_file, str);

	read_comment(i_file, str);
	num_of_jobs = 0;
	for (int fam_id = 0; fam_id < num_of_families; ++fam_id)
	{
		auto* fam_ptr = new Family();
		fam_ptr->id = fam_id;
		i_file >> fam_ptr->num_of_jobs;
		num_of_jobs += fam_ptr->num_of_jobs;
		families.emplace_back(fam_ptr);
	}

	read_comment(i_file, str);
	unordered_map<int, Job*> job_map;
	for (auto fam_ptr: families)
	{
		i_file >> data;
		for (int i = 0; i < fam_ptr->num_of_jobs; ++i)
		{
			int job_id;
			Job* job_ptr = new Job();
			i_file >> job_id;
			job_ptr->id = job_id - 1;
			job_map[job_ptr->id] = job_ptr;
			fam_ptr->jobs.emplace_back(job_ptr);
		}
	}
	read_comment(i_file, str);
	std::getline(i_file, str);

	read_comment(i_file, str);
	for (auto fam_ptr: families)
	{
		for (auto job_ptr : fam_ptr->jobs)
		{
			for (int s = 0; s < num_of_stages; ++s)
			{
				int pt;
				i_file >> pt;
				job_ptr->process_times.emplace_back(pt);
			}
			job_ptr->calculate_total_process_time();
		}
	}

	read_comment(i_file, str);
	for (int s = 0; s < num_of_stages; s++)
	{
		for (auto fam_ptr: families)
		{
			fam_ptr->setup_times.resize(num_of_stages);
			for (auto& st: fam_ptr->setup_times)
			{
				st.resize(num_of_families);
			}
		}
	}

	for (int s = 0; s < num_of_stages; s++)
	{
		for (auto fam_ptr1: families)
		{
			for (auto fam_ptr2: families)
			{
				i_file >> fam_ptr1->setup_times[s][fam_ptr2->id];
			}
		}
	}

	for (auto fam_ptr: families)
	{
		fam_ptr->set_total_process_time();
	}

	i_file.close();
}


Problem::~Problem()
{
	destroy_family_job();
}

void Problem::destroy_family_job()
{
	for (auto FamPtr: families)
	{
		delete FamPtr;
	}
	families.clear();
}