//
// Created by wangy on 2021/12/12.
//

#ifndef HFGSP_NEH_PROBLEM_H
#define HFGSP_NEH_PROBLEM_H

#include <vector>
#include <string>

class Family;

class Job;

class Problem {
public:
    void read_instance_filename_list(const std::string &dir);
    void read_instance(const std::string& file_name);

    Problem() = default;
    virtual ~Problem();

    int num_of_jobs{};
    int num_of_stages{};
    int num_of_families{};

    std::vector<Family *> families;
    std::vector<int> num_of_machines_at_each_stage;

    [[nodiscard]] const std::vector<std::string>& get_instance_filename_list() const
    {
        return instance_filename_list;
    }

private:
    std::vector<std::string> instance_filename_list;
    static void read_comment(std::ifstream &i_file, std::string &comment);
    void destroy_family_job();
};

#endif //HFGSP_NEH_PROBLEM_H
