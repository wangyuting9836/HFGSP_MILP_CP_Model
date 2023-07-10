//
// Created by wangy on 2023/4/26.
//

#ifndef HFGSP_NEH_PYGANTT_H
#define HFGSP_NEH_PYGANTT_H

#include "Solution.h"

class PyGantt
{
	static std::vector<std::string> color_dict;
public:
	static void ganttForward(const Solution& solution);
};


#endif //HFGSP_NEH_PYGANTT_H
