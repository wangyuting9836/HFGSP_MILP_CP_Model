//
// Created by wangy on 2023/5/27.
//
#include "rand.h"
bool wyt_rand(double par) {
    std::bernoulli_distribution dist(par);
    return dist(rand_generator());
}