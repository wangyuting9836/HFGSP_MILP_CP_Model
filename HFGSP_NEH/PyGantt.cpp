//
// Created by wangy on 2023/4/26.
//

#include <iostream>
#include <string>
#include <numeric>
#include <matplotlibcpp.h>
#include <iomanip>
#include <sstream>
#include "Family.h"
#include "Job.h"
#include "PyGantt.h"

namespace plt = matplotlibcpp;

std::vector<std::string> PyGantt::color_dict =
		{ "WhiteSmoke", "SeaShell", "PapayaWhip", "MintCream", "LightYellow", "Ivory", "GhostWhite",
		  "FloralWhite", "Cornsilk", "Azure", "AliceBlue", "LightBlue", "LightCoral", "LightCyan",
		  "LightGoldenRodYellow", "LightGrey", "LightGreen", "LightPink", "LightSalmon", "LightSeaGreen",
		  "LightSkyBlue", "LightSlateBlue", "LightSlateGray", "LightSteelBlue", "White" };

void PyGantt::ganttForward(const Solution& solution)
{
	plt::figure_size(1000, 250);
	int makeSpan = solution.make_span;
	std::vector<double> x(makeSpan + 1);
	std::iota(std::begin(x), std::end(x), 0);
	std::vector<double> y(makeSpan + 1);
	//const Problem& problem = solution.problem;

	std::vector<double> y_ticks;
	std::vector<std::string> y_labels;

	int y_tick = 0;

	int s = 1;
	for(const auto& gbs_at_stage : solution.decode_result)
	{
		int m = 1;
		for(const auto& gbs_on_machine : gbs_at_stage)
		{
			for(const auto &gb : gbs_on_machine)
			{
				int xrange1 = gb.start_time;
				int xrange2 = gb.finish_time - gb.start_time;
				if(gb.family_id == -1)
				{
					plt::broken_barh(xrange1, xrange2, y_tick - 0.4, 0.7,
							{{ "edgecolor", "gray" },
							 { "facecolor", "lightgray" }});

				}
				else
				{
					plt::broken_barh(xrange1, xrange2, y_tick - 0.4, 0.7,
							{{ "edgecolor", "gray" },
							 { "facecolor", color_dict[gb.family_id % color_dict.size()] }});

					plt::text(static_cast<double>(xrange1 + xrange2 / 2.0), static_cast<double>(y_tick),
							"$j_{" + std::to_string(gb.job_id + 1) + "}$", {{ "verticalalignment", "center" },
																	{ "horizontalalignment", "center" },
																	{ "color", "black" },
																	{ "fontsize", "10" }});
				}
				plt::text(static_cast<double>(xrange1), static_cast<double>(y_tick - 0.4),
						std::to_string(xrange1), {{ "verticalalignment", "bottom" },
												  { "horizontalalignment", "left" },
												  { "color", "black" },
												  { "fontsize", "7" },
												  { "fontweight", "semibold" }});
				plt::text(static_cast<double>(xrange1 + xrange2), static_cast<double>(y_tick - 0.4),
						std::to_string(xrange1 + xrange2), {{ "verticalalignment", "bottom" },
															{ "horizontalalignment", "right" },
															{ "color", "black" },
															{ "fontsize", "7" },
															{ "fontweight", "semibold" }});
			}

			y_ticks.emplace_back(y_tick);
			y_labels.emplace_back("$s_{" + std::to_string(s) + "}m_{" + std::to_string(m) + "}$");
			++y_tick;
			++m;
		}
		++s;
	}

	//plt::legend();
	//plt::yticks(std::vector<double>{}, std::vector<std::string>{});
	plt::yticks(y_ticks, y_labels);
	plt::xticks(std::vector<double>{}, std::vector<std::string>{});
	plt::xlim(0, makeSpan);
	plt::show();
}


