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

	for (const auto& file_name: problem.get_instance_filename_list())
	{
		problem.read_instance(file_name);

		st = std::chrono::steady_clock::now();
		Solution solution3(problem);
		int re1 = solution3.neh_fam();
		et = std::chrono::steady_clock::now();
		double duration1 = std::chrono::duration<double, std::milli>(et - st).count();
		assert(re1 == solution3.calculate_make_span());

		st = std::chrono::steady_clock::now();
		Solution solution4(problem);
		int re2 = solution4.neh_fam_job();
		et = std::chrono::steady_clock::now();
		double duration2 = std::chrono::duration<double, std::milli>(et - st).count();
		assert(re2 == solution4.calculate_make_span());

		//PyGantt::gantt(solution4);

		std::cout << re1 << "\t" << duration1 << "\t" << re2 << "\t" << duration2 << std::endl;

	}

	return 0;
}
