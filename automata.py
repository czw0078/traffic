#!/usr/bin/env python3

# Effect of driver over-acceleration on traffic breakdown in three-phase cellular automaton traffic flow models
# http://dx.doi.org/10.1016/j.physa.2013.04.035

import random

class kksw:
    def __init__(self):
        # constant not 1 equals 1.5 meters
        self.delta_x = 1.5
        self.v_free = 25 
        self.d = 5
        self.p3 = 0.05
        self.p02 = 0.5
        self.p22 = 0.35
        self.pa1 = 0.07
        self.pa2 = 0.08
        self.k1 = 3
        self.k2 = 2
        self.v_pinch = 6
        self.v_syn = 14
        self.delta_v_syn = 3
        # variables
        self.v_pre = 0
        self.v = 0
        self.v_next = 0
        self.g_vehicle_gap = self.v_free*self.k1
        self.vl_front= 0

    def update_a_v_vl_g_and_get_a_v(self, a, v, vl, g=120, v_free=25):
        self.v = v/self.delta_x 
        self.g_vehicle_gap = g/self.delta_x - self.d # at leaset 7.5 meters
        self.vl_front = vl/self.delta_x
        self.v_free = v_free

        self.rule_b_compare_syn_gap_then_rule_c_d_or_e()
        self.rule_f_decelerate()
        self.rule_g_randomize()
        self.v_pre = self.v
        self.v = self.v_next
        # update the v directly, not using a
        return 0, self.v*self.delta_x

    def rule_b_compare_syn_gap_then_rule_c_d_or_e(self):
        if self.g_vehicle_gap <= self.G():
            self.rule_c_speed_adapt_within_syn_gap()
            self.rule_d_over_accelerate_within_syn_gap()
        else:
            self.rule_e_accelerate()

    def rule_c_speed_adapt_within_syn_gap(self):
        if self.vl_front > self.v:
            self.v_next = self.v + 1
        elif self.vl_front < self.v:
            self.v_next = self.v - 1

    def rule_d_over_accelerate_within_syn_gap(self):
        if self.v >= self.vl_front and random.uniform(0,1) < self.pa():
            self.v_next = min(self.v_next + 1, self.v_free)

    def rule_e_accelerate(self):
        self.v_next = min(self.v + 1, self.v_free)

    def rule_f_decelerate(self):
        self.v_next = min(self.v_next, self.g_vehicle_gap)

    def rule_g_randomize(self): # bump
        r = random.uniform(0,1)
        if self.pa() <= r < self.p() + self.pa():
            self.v_next = max(self.v_next - 1, 0)

    def p(self):
        if self.v_next > self.v:
            return self.p2()
        else:
            return self.p3

    def p2(self):
        if self.v == 0:
            return self.p02
        else:
            return self.p12()

    def p12(self):
        if self.v <= self.v_pre:
            return self.p22
        else:
            return 0

    def pa(self):
        second_term = (self.v - self.v_syn)/self.delta_v_syn 
        return self.pa1 + self.pa2*max(0, min(1, second_term))

    def k(self):
        if self.v > self.v_pinch:
            return self.k1
        else:
            return self.k2

    def G(self):
        return self.k()*self.v



