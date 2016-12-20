# -*- coding: utf-8 -*-

# Copyright (c) 2016 by University of Kassel and Fraunhofer Institute for Wind Energy and Energy
# System Technology (IWES), Kassel. All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.

import pandapower as pp
import pytest

try:
    import pplog as logging
except:
    import logging

logger = logging.getLogger(__name__)

def test_simplest_voltage():
    """ Testing a very simple network without transformer for voltage
    constraints with OPF """

    # boundaries:
    vm_max = 1.05
    vm_min = 0.95

    # create net
    net = pp.create_empty_network()
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=10.)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_gen(net, 1, p_kw=-100, controllable=True, max_p_kw=-150, min_p_kw=-5, max_q_kvar=50,
                  min_q_kvar=-50, cost_per_kw=100)
    pp.create_ext_grid(net, 0)
    pp.create_load(net, 1, p_kw=20)
    pp.create_line_from_parameters(net, 0, 1, 50, name="line2", r_ohm_per_km=0.876,
                                   c_nf_per_km=260.0, imax_ka=0.123, x_ohm_per_km=0.1159876,
                                   max_loading_percent=100*690)
    # run OPF
    pp.runopp(net, verbose=False)
    assert net["OPF_converged"]

    # check and assert result
    logger.debug("test_simplest_voltage")
    logger.debug("res_gen:\n%s" % net.res_gen)
    logger.debug("res_ext_grid:\n%s" % net.res_ext_grid)
    logger.debug("res_bus.vm_pu: \n%s" % net.res_bus.vm_pu)
    assert max(net.res_bus.vm_pu) < vm_max
    assert min(net.res_bus.vm_pu) > vm_min



def test_eg_voltage():
    """ Testing a very simple network without transformer for voltage
    constraints with OPF """

    # boundaries:
    vm_max = 1.05
    vm_min = 0.95

    # create net
    net = pp.create_empty_network()
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=10.)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_gen(net, 1, p_kw=-100, controllable=True, max_p_kw=-150, min_p_kw=-5, max_q_kvar=50,
                  min_q_kvar=-50)
    pp.create_ext_grid(net, 0, vm_pu=1.01)
    pp.create_load(net, 1, p_kw=20)
    pp.create_line_from_parameters(net, 0, 1, 50, name="line2", r_ohm_per_km=0.876,
                                   c_nf_per_km=260.0, imax_ka=0.123, x_ohm_per_km=0.1159876,
                                   max_loading_percent=100*690)
    # run OPF
    pp.runopp(net, verbose=False)
    assert net["OPF_converged"]

    # check and assert result
    logger.debug("test_simplest_voltage")
    logger.debug("res_gen:\n%s" % net.res_gen)
    logger.debug("res_ext_grid:\n%s" % net.res_ext_grid)
    logger.debug("res_bus.vm_pu: \n%s" % net.res_bus.vm_pu)
    assert net.res_bus.vm_pu.at[0] == net.ext_grid.vm_pu.values


def test_simplest_dispatch():
    """ Testing a very simple network without transformer for voltage
    constraints with OPF """

    # boundaries:
    vm_max = 1.05
    vm_min = 0.95

    # create net
    net = pp.create_empty_network()
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=10.)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_gen(net, 1, p_kw=-100, controllable=True, max_p_kw=-150, min_p_kw=-5, max_q_kvar=50,
                  min_q_kvar=-50, cost_per_kw=100)
    pp.create_ext_grid(net, 0, cost_per_kw=101)
    pp.create_load(net, 1, p_kw=20)
    pp.create_line_from_parameters(net, 0, 1, 50, name="line2", r_ohm_per_km=0.876,
                                   c_nf_per_km=260.0, imax_ka=0.123, x_ohm_per_km=0.1159876,
                                   max_loading_percent=100*690)
    # run OPF
    pp.runopp(net, verbose=False)
    assert net["OPF_converged"]

    # check and assert result
    logger.debug("test_simplest_voltage")
    logger.debug("res_gen:\n%s" % net.res_gen)
    logger.debug("res_est_grid:\n%s" % net.res_ext_grid)
    logger.debug("res_bus.vm_pu: \n%s" % net.res_bus.vm_pu)
    assert max(net.res_bus.vm_pu) < vm_max
    assert min(net.res_bus.vm_pu) > vm_min



def test_opf_gen_voltage():
    """ Testing a  simple network with transformer for voltage
    constraints with OPF using a generator """

    # boundaries:
    vm_max = 1.05
    vm_min = 0.95

    # ceate net
    net = pp.create_empty_network()
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=10.)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_transformer_from_parameters(net, 0, 1, vsc_percent=3.75,
                                          tp_max=2, vn_lv_kv=0.4,
                                          shift_degree=150, tp_mid=0,
                                          vn_hv_kv=10.0, vscr_percent=2.8125,
                                          tp_pos=0, tp_side="hv", tp_min=-2,
                                          tp_st_percent=2.5, i0_percent=0.68751,
                                          sn_kva=16.0, pfe_kw=0.11, name=None,
                                          in_service=True, index=None, max_loading_percent=200)
    pp.create_gen(net, 3, p_kw=-10, controllable=True, max_p_kw=-25, min_p_kw=-5, max_q_kvar=50,
                  min_q_kvar=-50, cost_per_kw = -100)
    pp.create_ext_grid(net, 0)
    pp.create_line_from_parameters(net, 1, 2, 1, name="line2", r_ohm_per_km=0.876,
                                   c_nf_per_km=260.0, imax_ka=0.123, x_ohm_per_km=0.1159876,
                                   max_loading_percent=100000)
    pp.create_line_from_parameters(net, 2, 3, 1, name="line2", r_ohm_per_km=0.876,
                                   c_nf_per_km=260.0, imax_ka=0.123, x_ohm_per_km=0.1159876,
                                   max_loading_percent=100000)

    # run OPF
    pp.runopp(net, verbose=False)
    assert net["OPF_converged"]

    # check and assert result
    logger.debug("test_opf_gen_voltage")
    logger.debug("res_gen:\n%s" % net.res_gen)
    logger.debug("res_bus.vm_pu: \n%s" % net.res_bus.vm_pu)
    assert max(net.res_bus.vm_pu) < vm_max
    assert min(net.res_bus.vm_pu) > vm_min


def test_opf_sgen_voltage():
    """ Testing a  simple network with transformer for voltage
    constraints with OPF using a static generator """

    # boundaries
    vm_max = 1.04
    vm_min = 0.96

    # create net
    net = pp.create_empty_network()
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=10.)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_transformer_from_parameters(net, 0, 1, vsc_percent=3.75,
                                          tp_max=2, vn_lv_kv=0.4,
                                          shift_degree=150, tp_mid=0,
                                          vn_hv_kv=10.0, vscr_percent=2.8125,
                                          tp_pos=0, tp_side="hv", tp_min=-2,
                                          tp_st_percent=2.5, i0_percent=0.68751,
                                          sn_kva=16.0, pfe_kw=0.11, name=None,
                                          in_service=True, index=None, max_loading_percent=1000000)
    pp.create_sgen(net, 3, p_kw=-10, controllable=True, max_p_kw=-
                   15, min_p_kw=-5, max_q_kvar=25, min_q_kvar=-25, cost_per_kw = -100)
    pp.create_ext_grid(net, 0)
    pp.create_line_from_parameters(net, 1, 2, 1, name="line2", r_ohm_per_km=0.876,
                                   c_nf_per_km=260.0, imax_ka=0.123, x_ohm_per_km=0.1159876,
                                   max_loading_percent=1000000)
    pp.create_line_from_parameters(net, 2, 3, 1, name="line2", r_ohm_per_km=0.876,
                                   c_nf_per_km=260.0, imax_ka=0.123, x_ohm_per_km=0.1159876,
                                   max_loading_percent=1000000)

    # run OPF
    pp.runopp(net, verbose=False)
    assert net["OPF_converged"]

    # assert and check result
    logger.debug("test_opf_sgen_voltage")
    logger.debug("res_sgen:\n%s" % net.res_sgen)
    logger.debug("res_bus.vm_pu: \n%s" % net.res_bus.vm_pu)
    assert max(net.res_bus.vm_pu) < vm_max
    assert min(net.res_bus.vm_pu) > vm_min


def test_opf_gen_loading():
    """ Testing a  simple network with transformer for loading
    constraints with OPF using a generator """

    # wide open voltage boundaries to make sure they don't interfere with loading constraints
    vm_max = 1.5
    vm_min = 0.5
    max_line_loading = 11

    # create net
    net = pp.create_empty_network()
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=10.)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_transformer_from_parameters(net, 0, 1, vsc_percent=3.75,
                                          tp_max=2, vn_lv_kv=0.4,
                                          shift_degree=150, tp_mid=0,
                                          vn_hv_kv=10.0, vscr_percent=2.8125,
                                          tp_pos=0, tp_side="hv", tp_min=-2,
                                          tp_st_percent=2.5, i0_percent=0.68751,
                                          sn_kva=16.0, pfe_kw=0.11, name=None,
                                          in_service=True, index=None, max_loading_percent=145)
    pp.create_gen(net, 3, p_kw=-10, controllable=True, max_p_kw=-15, min_p_kw=-5, max_q_kvar=50,
                  min_q_kvar=-50, cost_per_kw=-10)
    pp.create_ext_grid(net, 0, cost_per_kw=0.1)
    pp.create_line_from_parameters(net, 1, 2, 1, name="line2", r_ohm_per_km=0.876,
                                   c_nf_per_km=260.0, imax_ka=0.123, x_ohm_per_km=0.1159876,
                                   max_loading_percent=max_line_loading)
    pp.create_line_from_parameters(net, 2, 3, 1, name="line2", r_ohm_per_km=0.876,
                                   c_nf_per_km=260.0, imax_ka=0.123, x_ohm_per_km=0.1159876,
                                   max_loading_percent=max_line_loading)

    # run OPF
    pp.runopp(net, verbose=False)
    assert net["OPF_converged"]

    # assert and check result
    logger.debug("test_opf_gen_loading")
    logger.debug("res_gen:\n%s" % net.res_gen)
    logger.debug("res_line.loading_percent:\n%s" % net.res_line.loading_percent)
    assert max(net.res_line.loading_percent) < max_line_loading
    logger.debug("res_trafo.loading_percent:\n%s" % net.res_trafo.loading_percent)
    assert max(net.res_trafo.loading_percent) < 145
    assert max(net.res_bus.vm_pu) < vm_max
    assert min(net.res_bus.vm_pu) > vm_min


def test_opf_sgen_loading():
    """ Testing a  simple network with transformer for loading
    constraints with OPF using a generator """

    # boundaries
    vm_max = 1.5
    vm_min = 0.5
    max_trafo_loading = 800
    max_line_loading = 13

    # create net
    net = pp.create_empty_network()
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=10.)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_bus(net, max_vm_pu=vm_max, min_vm_pu=vm_min, vn_kv=.4)
    pp.create_transformer_from_parameters(net, 0, 1, vsc_percent=3.75, tp_max=2, vn_lv_kv=0.4,
                                          shift_degree=150, tp_mid=0, vn_hv_kv=10.0,
                                          vscr_percent=2.8125, tp_pos=0, tp_side="hv", tp_min=-2,
                                          tp_st_percent=2.5, i0_percent=0.68751, sn_kva=16.0,
                                          pfe_kw=0.11, name=None, in_service=True, index=None,
                                          max_loading_percent=max_trafo_loading)
    pp.create_sgen(net, 3, p_kw=-10, controllable=True, max_p_kw=-15, min_p_kw=-5, max_q_kvar=25,
                   min_q_kvar=-25, cost_per_kw=-10)
    pp.create_ext_grid(net, 0, cost_per_kw=0.1)
    pp.create_line_from_parameters(net, 1, 2, 1, name="line2", r_ohm_per_km=0.876,
                                   c_nf_per_km=260.0, imax_ka=0.123, x_ohm_per_km=0.1159876,
                                   max_loading_percent=max_line_loading)
    pp.create_line_from_parameters(net, 2, 3, 1, name="line2", r_ohm_per_km=0.876,
                                   c_nf_per_km=260.0, imax_ka=0.123, x_ohm_per_km=0.1159876,
                                   max_loading_percent=max_line_loading)

    # run OPF
    pp.runopp(net, verbose=False)
    assert net["OPF_converged"]

    # assert and check result
    logger.debug("test_opf_sgen_loading")
    logger.debug("res_sgen:\n%s" % net.res_sgen)
    logger.debug("res_line.loading_percent:\n%s" % net.res_line.loading_percent)
    assert max(net.res_line.loading_percent) < max_line_loading
    logger.debug("res_trafo.loading_percent:\n%s" % net.res_trafo.loading_percent)
    assert max(net.res_trafo.loading_percent) < max_trafo_loading
    assert max(net.res_bus.vm_pu) < vm_max
    assert min(net.res_bus.vm_pu) > vm_min

def test_opf_oberrhein():
   """ Testing a  simple network with transformer for loading
   constraints with OPF using a generator """
   import pandapower.networks as nw
   # create net
   net = nw.mv_oberrhein()
   net.bus["max_vm_pu"]=1.1
   net.bus["min_vm_pu"]=0.9
   net.line["max_loading_percent"]=200
   net.trafo["max_loading_percent"]=100
   net.sgen["max_p_kw"]=-net.sgen.sn_kva
   net.sgen["min_p_kw"]=0
   net.sgen["max_q_kvar"]=1
   net.sgen["min_q_kvar"]=-1
   net.sgen["controllable"] =1
   # run OPF
   pp.runopp(net, verbose=False)
   assert net["OPF_converged"]

def test_minimize_active_power_curtailment():
    net = pp.create_empty_network()

    # create buses
    bus1 = pp.create_bus(net, vn_kv=220.)
    bus2 = pp.create_bus(net, vn_kv=110.)
    bus3 = pp.create_bus(net, vn_kv=110.)
    bus4 = pp.create_bus(net, vn_kv=110.)

    # create 220/110 kV transformer
    pp.create_transformer(net, bus1, bus2, std_type="100 MVA 220/110 kV")

    # create 110 kV lines
    pp.create_line(net, bus2, bus3, length_km=70., std_type='149-AL1/24-ST1A 110.0')
    pp.create_line(net, bus3, bus4, length_km=50., std_type='149-AL1/24-ST1A 110.0')
    pp.create_line(net, bus4, bus2, length_km=40., std_type='149-AL1/24-ST1A 110.0')

    # create loads
    pp.create_load(net, bus2, p_kw=60e3)
    pp.create_load(net, bus3, p_kw=70e3)
    pp.create_load(net, bus4, p_kw=10e3)

    # create generators
    eg = pp.create_ext_grid(net, bus1)
    g0 = pp.create_gen(net, bus3, p_kw=-80 * 1e3, min_p_kw=0, max_p_kw=-80e3, vm_pu=1.01, controllable=True)
    g1 = pp.create_gen(net, bus4, p_kw=-100 * 1e3, min_p_kw=0, max_p_kw=-100e3, vm_pu=1.01, controllable=True)

    net.ext_grid.loc[eg, "cost_per_kw"] = 0.10
    net.gen.loc[g0, "cost_per_kw"] = 0.15
    net.gen.loc[g1, "cost_per_kw"] = 0.12

    net.trafo["max_loading_percent"] = 50
    net.line["max_loading_percent"] = 50

    net.bus["min_vm_pu"] = 1.0
    net.bus["max_vm_pu"] = 1.02

    net.ext_grid.cost_per_kw = 0
    net.gen.cost_per_kw = -1

    pp.runopp(net)
    # logger.info(net['res_bus'])
    assert net["OPF_converged"]
    # ToDo: Werte abtesten (@rieke)

#def test_linear_minloss_cost_fnc():


if __name__ == "__main__":
    pytest.main(["test_opf.py", "-s"])
    # test_minimize_active_power_curtailment()