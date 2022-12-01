"""All Nilan Registers"""


class CTS602InputRegisters:
    """Register map of Nilan CTS602"""

    bus_version = 0
    app_version_major = 1
    app_version_minor = 2
    app_version_release = 3
    info_app_id = 4
    info_hw_type = 5

    input_user_func = 100
    input_air_filter = 101
    input_door_open = 102
    input_smoke = 103
    input_motor_thermo = 104
    input_frost_overht = 105
    input_airflow = 106
    input_p_hi = 107
    input_p_lo = 108
    input_boil = 109
    input_3way_pos = 110
    input_defrost_hg = 111
    input_defrost = 112
    input_user_func_2 = 113
    input_damper_closed = 114
    input_damper_opened = 115
    input_f_cor_thermo_al = 116

    input_t0_controller = 200
    input_t1_intake = 201
    input_t2_inlet = 202
    input_t3_exhaust = 203
    input_t4_outlet = 204
    input_t5_cond = 205
    input_t6_evap = 206
    input_t7_inlet = 207
    input_t8_outdoor = 208
    input_t9_heater = 209
    input_t10_extern = 210
    input_t11_top = 211
    input_t12_bottom = 212
    input_t13_return = 213
    input_t14_supply = 214
    input_t15_room = 215
    input_t16 = 216
    input_t17_pre_heat = 217
    input_t18_pres_pibe = 218
    input_p_suc = 219
    input_p_dis = 220
    air_qual_rh = 221
    air_qual_co2 = 222

    alarm_status = 400
    alarm_list_1_id = 401
    alarm_list_1_date = 402
    alarm_list_1_time = 403
    alarm_list_2_id = 404
    alarm_list_2_date = 405
    alarm_list_2_time = 406
    alarm_list_3_id = 407
    alarm_list_3_date = 408
    alarm_list_3_time = 409

    control_run_act = 1000
    control_mode_act = 1001
    control_state_display = 1002
    control_sec_in_state = 1003

    air_flow_vent_set = 1100
    air_flow_inlet_act = 1101
    air_flow_exhaust_act = 1102
    air_flow_since_filt_day = 1103
    air_flow_to_filt_day = 1104

    air_temp_is_summer = 1200
    air_temp_temp_inlet_set = 1201
    air_temp_temp_control = 1202
    air_temp_temp_room = 1203
    air_temp_eff_pct = 1204
    air_temp_cap_set = 1205
    air_temp_cap_act = 1206

    compressor_type = 1500

    hot_water_type = 1700
    hot_water_anode_state = 1701

    central_heat_heat_ext_set = 1800

    display_led_1 = 2000
    display_led_2 = 2001
    display_text_1_2 = 2002
    display_text_3_4 = 2003
    display_text_5_6 = 2004
    display_text_7_8 = 2005
    display_attr_1_8 = 2006
    display_text_9_10 = 2007
    display_text_11_12 = 2008
    display_text_13_14 = 2009
    display_text_15_16 = 2010
    display_attr_9_16 = 2011

    pre_heat_block_remain = 2100

    dpt_in_session = 2200
    dpt_air_flow_1 = 2201
    dpt_air_flow_2 = 2202

    air_bypass_is_open = 3000
    output_air_heat_cap = 3001
    defrost_exch_defrost = 3002
    air_qual_co2_enable = 3003
    air_flow_room_reduce = 3004
    air_flow_last_test_day = 3005
    air_flow_since_filt_day = 3006
    air_flow_winter_reduce = 3007
    air_temp_temp_set = 3008
    air_temp_temp_control = 3009

    alarm_event_log_id = 3050
    alarm_log_date = 3051
    alarm_log_t1 = 3052
    alarm_log_t2 = 3053
    alarm_log_t3 = 3054
    alarm_log_t4 = 3055
    alarm_log_t5 = 3056
    alarm_log_t6 = 3057
    alarm_log_t7 = 3058
    alarm_log_t8 = 3059
    alarm_log_t9 = 3060
    alarm_log_t10 = 3061
    alarm_log_t11 = 3062
    alarm_log_t12 = 3063
    alarm_log_t13 = 3064
    alarm_log_t14 = 3065
    alarm_log_t15 = 3066
    alarm_log_di_1_8 = 3067
    alarm_log_di_9_16 = 3068
    alarm_log_do_1_8 = 3069
    alarm_log_do_9_16 = 3070
    alarm_log_ao_1 = 3071
    alarm_log_ao_2 = 3072
    alarm_log_ao_3 = 3073
    alarm_log_ao_4 = 3074
    alarm_log_contol_state = 3075

    air_qual_rh_avg = 3100
    opt9_1_board_id = 3101
    air_flow_vent_state = 3102


class CTS602HoldingRegisters:
    """Nilan CTS602 Holding Registers"""

    bus_address = 50

    output_air_flap = 100
    output_smoke_flap = 101
    output_bypass_open = 102
    output_bypass_close = 103
    output_air_circ_pump = 104
    output_air_heat_allow = 105
    output_air_heat_1 = 106
    output_air_heat_2 = 107
    output_air_heat_3 = 108
    output_compressor = 109
    output_compressor_2 = 110
    output_4_way_cool = 111
    output_hotgas_heat = 112
    output_hotgas_cool = 113
    output_cond_open = 114
    output_cond_close = 115
    output_water_heat = 116
    output_3_way_valve = 117
    output_cen_circ_pump = 118
    output_cen_heat_1 = 119
    output_cen_heat_2 = 120
    output_cen_heat_3 = 121
    output_cen_heat_ext = 122
    output_user_func = 123
    output_user_func_2 = 124
    output_defrosting = 125
    output_alarm_relay = 126
    output_pre_heat = 127

    output_exhaust_speed = 200
    output_inlet_speed = 201
    output_air_heat_cap = 202
    output_cen_heat_cap = 203
    output_cpr_cap = 204
    output_pre_heat_cap = 205

    time_second = 300
    time_minute = 301
    time_hour = 302
    time_day = 303
    time_month = 304
    time_year = 305

    alarm_reset = 400

    program_select = 500

    program_user_func_act = 600
    program_user_func_set = 601
    program_user_time_set = 602
    program_user_vent_set = 603
    program_user_temp_set = 604
    program_user_offs_set = 605

    program_user_2_func_act = 610
    program_user_2_func_set = 611
    program_user_2_time_set = 612
    program_user_2_vent_set = 613
    program_user_2_temp_set = 614
    program_user_2_offs_set = 615

    log_interval = 700

    control_type = 1000
    control_run_set = 1001
    control_mode_set = 1002
    control_vent_set = 1003
    control_temp_set = 1004
    control_service_mode = 1005
    control_service_pct = 1006
    control_preset = 1007

    air_flow_air_exch_mode = 1100
    air_flow_cool_vent = 1101
    air_flow_test_select = 1102
    air_flow_last_test_day = 1103
    air_flow_test_state = 1104
    air_flow_filt_alm_type = 1105

    air_temp_cool_set = 1200
    air_temp_temp_min_sum = 1201
    air_temp_temp_min_win = 1202
    air_temp_temp_max_sum = 1203
    air_temp_temp_max_win = 1204
    air_temp_temp_summer = 1205
    air_temp_night_day_lim = 1206
    air_temp_night_set = 1207
    air_temp_sensor_select = 1208
    air_temp_heat_select = 1209

    compressor_cond_temp_min = 1500
    compressor_cond_temp_max = 1501
    air_temp_temp_min_cpr = 1502
    air_temp_cpr_restart = 1503

    hot_water_temp_set_t11 = 1700
    hot_water_temp_set_t12 = 1701
    hot_water_priority = 1702
    hot_water_temp_cpr_max = 1703
    hot_water_heat_type = 1704
    hot_water_legio_type = 1705
    hot_water_temp_pri = 1706

    central_heat_heat_extern = 1800
    central_heat_heat_select = 1801
    central_heat_supply_min = 1802
    central_heat_supply_max = 1803
    central_heat_supply_offset = 1804
    central_heat_curve_select = 1805
    central_heat_circ_pump_mode = 1806
    central_heat_heat_type = 1807
    central_heat_reg_time = 1808

    air_qual_rh_vent_lo = 1910
    air_qual_rh_vent_hi = 1911
    air_qual_rh_lim_lo = 1912
    air_qual_time_out = 1913

    air_qual_co2_vent_hi = 1920
    air_qual_co2_lim_lo = 1921
    air_qual_co2_lim_hi = 1922

    display_key_code = 2000

    user_user_menu_open = 2002
    user_language = 2003

    pre_heat_block = 2100

    dpt_do_calibrate = 2200

    display_central_heat_heat_extern = 4000
    display_air_flow_cool_vent = 4001
    air_flow_winter_temp = 4002
    air_flow_winter_vent = 4003
    air_flow_test_select = 4004
    air_heat_type = 4005
    air_heat_delay = 4006
    display_air_temp_temp_min_sum = 4007
    display_air_temp_temp_max_sum = 4008
    display_air_temp_temp_min_win = 4009
    display_air_temp_temp_max_win = 4010
    air_temp_room_nz = 4011
    air_temp_temp_room_low = 4012
    air_heat_select_set = 4013

    air_flow_inlet_min = 4015
    air_flow_exhaust_min = 4016
    air_flow_exhaust_max = 4017
    air_flow_start_delay = 4018
    air_bypass_walking_time = 4019
    defrost_fans = 4020
    defrost_bypass = 4021
    defrost_block_minutes = 4022
    defrost_temp_start = 4023
    defrost_temp_stop = 4024
    defrost_dur_max_cpr = 4025
    defrost_dur_max_exh = 4026
    defrost_t6_min_run_sec = 4027

    program_edit_index = 4030
    program_edit_period = 4031
    program_edit_period_nx = 4032
    program_edit_func = 4033
    program_edit_time_star = 4034
    program_edit_vent = 4035
    program_edit_temp = 4036

    control_restart_mode = 4040
    control_power_save = 4041

    alarm_log_index = 4050

    air_flow_inlet_scale = 4098
    air_flow_exhaust_scale = 4099
    air_flow_inlet_spd_1 = 4100
    air_flow_inlet_spd_2 = 4101
    air_flow_inlet_spd_3 = 4102
    air_flow_inlet_spd_4 = 4103
    air_flow_exhaust_spd_1 = 4104
    air_flow_exhaust_spd_2 = 4105
    air_flow_exhaust_spd_3 = 4106
    air_flow_exhaust_spd_4 = 4107
    air_qual_type = 4108
    control_ana_out_type = 4109
    air_temp_room_response = 4110
    preheat_defrost = 4111
    preheat_temp_set = 4112
