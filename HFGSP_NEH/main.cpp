#include <iostream>
#include <cassert>
#include <chrono>
#include "Problem.h"
#include "Solution.h"
#include "PyGantt.h"

int main()
{
	std::chrono::time_point<std::chrono::steady_clock> st;
	std::chrono::time_point<std::chrono::steady_clock> et;

	Problem problem;
	problem.read_instance_filename_list("..\\data");
	//problem.read_instance("..\\data\\HFG_4_3_d.txt");

	/*int span = INT_MAX;
	for (int i = 0; i < 1; ++i)
	{
		Solution solution(problem);
		span = std::min(span, solution.calculate_make_span());
		PyGantt::ganttForward(solution);
	}

	std::cout << span << std::endl;*/

	int neh1_total_span = 0;
	int neh2_total_span = 0;
	int neh3_total_span = 0;
	int neh4_total_span = 0;
	int count1 = 0, count2 = 0, count3 = 0, count4 = 0;
	for (const auto& file_name: problem.get_instance_filename_list())
	{
		problem.read_instance(file_name);

		Solution solution1(problem);
		int re1 = solution1.neh_fam_1();
		neh1_total_span += re1;
		assert(re1 == solution1.calculate_make_span());

		Solution solution2(problem);
		int re2 = solution2.neh_fam_2();
		neh2_total_span += re2;
		assert(re2 == solution2.calculate_make_span());

		st = std::chrono::steady_clock::now();
		Solution solution3(problem);
		int re3 = solution3.neh_fam_3();
		et = std::chrono::steady_clock::now();
		//auto duration3 = std::chrono::duration_cast<std::chrono::microseconds >(et - st);
		double duration3 = std::chrono::duration<double, std::milli>(et - st).count();
		neh3_total_span += re3;
		assert(re3 == solution3.calculate_make_span());

		st = std::chrono::steady_clock::now();
		Solution solution4(problem);
		int re4 = solution4.neh_fam_job();
		et = std::chrono::steady_clock::now();
		double duration4 = std::chrono::duration<double, std::milli>(et - st).count();
		neh4_total_span += re4;
		assert(re4 == solution4.calculate_make_span());
		PyGantt::ganttForward(solution4);

		std::cout << re1 << "\t" << re2 << "\t" << re3 << "\t" << duration3 << "\t" << re4 << "\t" << duration4 << std::endl;
		int min_span = std::min(re1, std::min(re2, std::min(re3, re4)));
		if (re1 == min_span)
		{
			++count1;
		}
		if (re2 == min_span)
		{
			++count2;
		}
		if (re3 == min_span)
		{
			++count3;
		}
		if (re4 == min_span)
		{
			++count4;
		}
	}
	std::cout << count1 << "\t" << count2 << "\t" << count3 << "\t" << count4 << std::endl;
	std::cout << neh1_total_span << "\t" << neh2_total_span << "\t" << neh3_total_span << "\t" << neh4_total_span
			  << std::endl;
	return 0;
}
