# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
import os
import sys
import json
import argparse

from struct import *
sys.path.append('py')

from evaluate_event import EvaluateEvent


def evaluateLevelColorDecreasing(level, num, min_num, level_red, level_yellow, color_unavailable, show_none):

    if not show_none:
        return COLOR_NONE

    if num >= min_num:
        if level <= level_red:
            return "RED"
        elif level <= level_yellow:
            return "YELLOW"
        else:
            return "GREEN"

    return color_unavailable


def evaluateLevelColorIncreasing(level, num, min_num, level_red, level_yellow, color_unavailable, show_none):

    if not show_none:
        return COLOR_NONE

    if num >= min_num:
        if level >= level_red:
            return "RED"
        elif level >= level_yellow:
            return "YELLOW"
        else:
            return "GREEN"

    return color_unavailable

def evalueteT(T50Ex, T50Ex_nr, Td, Td_nr, T0, T0_nr):

    if(T50Ex_nr < 6):
        T50Ex = 'None'
    if (Td_nr < 6):
        Td = 'None'
    if (T0_nr < 6):
        T0 = 'None'

    inum_tdt0    = min(Td_nr, T0_nr)
    inum_TdT50Ex = min(Td_nr, T50Ex_nr)

    try:
        TdT50Ex = T50Ex * Td
    except:
        TdT50Ex = 'None'

    try:
        TdT0 = T0 * Td
    except:
        TdT0 = 'None'

    if(inum_tdt0 < 6):
        TdT0 = 'None'

    if (inum_TdT50Ex < 6):
        TdT50Ex = 'None'


    return TdT50Ex, TdT0, inum_TdT50Ex, inum_tdt0

def addInformationTableData(tableRow, padCellColors, bgColor, text):
    tableRowInternal = Tag.TR(tag_class="diagram")

    # use following if putting pad cells after new information in row
    # for i in range(len(padCellColors) - 1, -1, -1):
    #	color = padCellColors[i]
    for color in padCellColors:
        tableData = Tag.TD(tag_class="diagram_continued_bg" + color)
        tableData.append(Tag.FONT(self.space(1), tag_class="small"))
        tableRowInternal.append(tableData)

    color = "GREY"
    if bgColor is not None:
        color = bgColor
    tableData = Tag.TD(tag_class="diagram_bg" + color)
    tableData.append(Tag.FONT(self.space(1) + text, tag_class="small"))
    tableRowInternal.append(tableData)

    tableInternal = Tag.TABLE(tag_class="diagram")
    tableInternal.append(tableRowInternal)
    tableRow.append(Tag.TD(tableInternal, tag_class="diagram"))

    return tableRow


def parse_stdin():


    description = 'stdin parser'
    example     = 'EXAMPLES:\n=========\n' + \
                  'Example for rabbit connetion mode:\n'  + sys.argv[0] + ' --json json input_parameters.json' + '\n  '

    parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter, epilog = example)

    parser.add_argument('--json',   default = None,        help = 'json file with input parameters. Default: None')

    args = parser.parse_args()

    if not sys.argv[1:]:
        print ("Use -h or --help option for Help")
        sys.exit(0)


    return args



if __name__ == '__main__':

    plate_boundary_color_interplate_thrust = None
    plate_boundary_color_thrust_fault = None
    plate_boundary_color_transform_fault = None
    closest_bndry_dist_min_interplate_thrust = -1.0
    closest_bndry_dist_min_thrust_fault = -1.0
    closest_bndry_dist_min_transform_fault = -1.0

    closest_plate_boundaries = []


    global __ALARM_CRITICAL_VALUE, __ALARM_RED_CUTOFF, __ALARM_YELLOW_CUTOFF
    __ALARM_CRITICAL_VALUE = 8.0  # NOTE: Important!!!  Must equal value in timedomain_processing_report.h
    __ALARM_RED_CUTOFF = (1.1 * __ALARM_CRITICAL_VALUE)
    __ALARM_YELLOW_CUTOFF = (0.9 * __ALARM_CRITICAL_VALUE)
    global __MIN_NUMBER_WARNING_LEVELS_ALARM
    __MIN_NUMBER_WARNING_LEVELS_ALARM = 4

    global __TDT0_CRITICAL_VALUE, __TDT0_RED_CUTOFF, __TDT0_YELLOW_CUTOFF
    __TDT0_CRITICAL_VALUE = 510  # NOTE: Important!!!  Must equal value in papers
    __TDT0_RED_CUTOFF = (1.1 * __TDT0_CRITICAL_VALUE)
    __TDT0_YELLOW_CUTOFF = (0.9 * __TDT0_CRITICAL_VALUE)
    global __MIN_NUMBER_WARNING_LEVELS_TDT0
    __MIN_NUMBER_WARNING_LEVELS_TDT0 = __MIN_NUMBER_WARNING_LEVELS_ALARM

    global __UNDERWATER_RED_CUTOFF, __UNDERWATER_YELLOW_CUTOFF
    __UNDERWATER_RED_CUTOFF = 20.0  # percent
    __UNDERWATER_YELLOW_CUTOFF = 2.0  # percent

    global __SLAB_DEPTH_RED_CUTOFF, __SLAB_DEPTH_YELLOW_CUTOFF
    __SLAB_DEPTH_RED_CUTOFF = 35
    __SLAB_DEPTH_YELLOW_CUTOFF = 45

    global __MWP_RED_CUTOFF, __MWP_YELLOW_CUTOFF
    __MWP_RED_CUTOFF = 7.65  # NOTE: Important!!!  Must equal value in timedomain_processing_report.h
    __MWP_YELLOW_CUTOFF = 7.35
    global __MIN_NUMBER_MWP_ALARM
    __MIN_NUMBER_MWP_ALARM = 4

    global __MIN_MWP_FOR_VALID_MWPD
    __MIN_MWP_FOR_VALID_MWPD = 7.0

    global __PLATE_BNDY_SUB_MAX_DIST, __PLATE_BNDY_MAX_DIST
    __PLATE_BNDY_SUB_MAX_DIST = 1000.0  # km
    __PLATE_BNDY_MAX_DIST = 200.0  # km

    global __PLATE_BNDY_SUB_DIST_RED_CUTOFF, __PLATE_BNDY_SUB_DIST_YELLOW_CUTOFF
    __PLATE_BNDY_SUB_DIST_RED_CUTOFF = 150.0
    __PLATE_BNDY_SUB_DIST_YELLOW_CUTOFF = 200.0
    global __PLATE_BNDY_CB_DIST_RED_CUTOFF, __PLATE_BNDY_CB_DIST_YELLOW_CUTOFF
    __PLATE_BNDY_CB_DIST_RED_CUTOFF = 50.0
    __PLATE_BNDY_CB_DIST_YELLOW_CUTOFF = 100.0
    global __PLATE_BNDY_TF_DIST_RED_CUTOFF, __PLATE_BNDY_TF_DIST_YELLOW_CUTOFF
    __PLATE_BNDY_TF_DIST_RED_CUTOFF = 30.0
    __PLATE_BNDY_TF_DIST_YELLOW_CUTOFF = 60.0

    global __MIN_NUM_MWP_FOR_TSUNAMI_RUPTURE_PREDICTION, __MIN_MWP_FOR_TSUNAMI_RUPTURE_PREDICTION
    __MIN_NUM_MWP_FOR_TSUNAMI_RUPTURE_PREDICTION = 20
    __MIN_MWP_FOR_TSUNAMI_RUPTURE_PREDICTION = 6.95

    global flag_config__event_info__tsunami_decision_table_colors_show
    flag_config__event_info__tsunami_decision_table_colors_show = True
    try:
        flag_config__event_info__tsunami_decision_table_colors_show = config.getboolean("EventInfo",
                                                                                        "tsunami.decision_table.colors.show")
    except:  # not present or syntax error
        pass


    args=parse_stdin()

    s = open(args.json, 'r') #.read()
    data = json.load(s)

    event_id    = data['event_id']
    origin_id   = data['origin_id']
    lat         = data['lat']
    lon         = data['lon']
    depth       = data['depth']
    minHorUnc   = data['minHorUnc']
    maxHorUnc   = data['maxHorUnc']
    azMaxHorUnc = data['azMaxHorUnc']
    mag         = data['mag']
    nr_mag      = data['nr_mag']
    T50Ex       = data['T50Ex']
    T50Ex_nr    = data['T50Ex_nr']
    Td          = data['Td']
    Td_nr       = data['Td_nr']
    T0          = data['T0']
    T0_nr       = data['T0_nr']

    TdT50Ex, TdT0, inum_TdT50Ex, inum_tdt0 = evalueteT(T50Ex, T50Ex_nr, Td, Td_nr, T0, T0_nr)

    #####################################################
    # Begin
    evaluateEvent = EvaluateEvent()

    # Underwater
    mean, std = evaluateEvent.percentProbIsUnderwater(lat, lon, minHorUnc, maxHorUnc, azMaxHorUnc)
    ipercent_prob_underwater = int(0.5 + mean)
    ipercent_prob_underwater_std_dev = int(0.5 + std)
    #print("Probability Underwater:", ipercent_prob_underwater, '-/+', ipercent_prob_underwater_std_dev)
    if(ipercent_prob_underwater >= 99):
        prob_underwater_text = '>99%'
    elif(ipercent_prob_underwater < 1):
        prob_underwater_text = '<1%'
    else:
        prob_underwater_text = ("%d " % (int(ipercent_prob_underwater))) + '%'


    # Inslab
    is_inside_slab, n_slab, slab_name, slab_depth = False, None, None, None
    is_inside_slab, n_slab, slab_name, slab_depth = evaluateEvent.isInsideSlab(lat, lon)
    #print(is_inside_slab, '++++',n_slab, '++++',slab_name, 'pppp',slab_depth)

    if(is_inside_slab == False):
        slab_text       = 'none or not available'
        slab_depth_text = 'n/a'
    else:
        slab_text = slab_name.replace(': \'gmt\'', '')
        if(slab_depth != EvaluateEvent.SLAB_DEPTH_ERROR):
            slab_depth_text = str(int(0.5 + slab_depth)) + "km"
        else:
            slab_depth_text = "error: evaluating slab depth: " + str(slab_depth)

    #print(slab_text)
    #print(slab_depth_text)


    print("Closest plate boundaries:")
    exclude_boundary_codes = ""
    nboundary = 0

    #ssys.exit()
    while nboundary < 99:

        distance_min, boundary_code, closest_boundary_class, closest_boundary_class_id = evaluateEvent.findClosestPlateBoundary(
            lat, lon, exclude_boundary_codes)

        if distance_min > 1000.0:
            break

        plate_boundary_identifiers, split_chr = evaluateEvent.evaluatePlateBoundaryCode(boundary_code)
        print(boundary_code, "[", \
              plate_boundary_identifiers[0], split_chr, \
              plate_boundary_identifiers[1], \
              ",", closest_boundary_class, ", ", closest_boundary_class_id, "]: distance:",
              "< " + str(int(distance_min)), "km")
        exclude_boundary_codes += "$" + boundary_code
        nboundary += 1

        distance_min = 10.0 * round(distance_min / 10.0)

        closest_plate_boundaries.append((distance_min, boundary_code, closest_boundary_class, closest_boundary_class_id))
        exclude_boundary_codes += "$" + boundary_code

        is_inside_slab, n_slab, slab_name, slab_depth = evaluateEvent.isInsideSlab(lat, lon)


    for closest_plate_boundary_distance_min, closest_plate_boundary_code, closest_plate_boundary_class, closest_boundary_class_id in closest_plate_boundaries:
        print(closest_plate_boundary_distance_min, closest_plate_boundary_code, closest_plate_boundary_class, closest_boundary_class_id)

        # Interplate Thrust
        if plate_boundary_color_interplate_thrust is None:
            if closest_boundary_class_id == "SUB":
                plate_boundary_color_interplate_thrust = evaluateLevelColorDecreasing(closest_plate_boundary_distance_min, 1, -1, \
                                                                                      __PLATE_BNDY_SUB_DIST_RED_CUTOFF + 2.0 * depth + maxHorUnc, \
                                                                                      __PLATE_BNDY_SUB_DIST_YELLOW_CUTOFF + depth + maxHorUnc, \
                                                                                      "GREY", flag_config__event_info__tsunami_decision_table_colors_show)
                closest_bndry_dist_min_interplate_thrust = closest_plate_boundary_distance_min


        # Thrust Fault
        if plate_boundary_color_thrust_fault is None:
            if closest_boundary_class_id == "OCB" or closest_boundary_class_id == "CCB":
                plate_boundary_color_thrust_fault = evaluateLevelColorDecreasing(closest_plate_boundary_distance_min, 1, -1, \
                                                                                      __PLATE_BNDY_CB_DIST_RED_CUTOFF + maxHorUnc, \
                                                                                      __PLATE_BNDY_CB_DIST_YELLOW_CUTOFF + maxHorUnc, \
                                                                                      "GREY", flag_config__event_info__tsunami_decision_table_colors_show)

                closest_bndry_dist_min_thrust_fault = closest_plate_boundary_distance_min

        # Transform Fault
            if plate_boundary_color_transform_fault is None:
                if closest_boundary_class_id == "OTF" or closest_boundary_class_id == "CTF":
                    plate_boundary_color_transform_fault = evaluateLevelColorDecreasing(closest_plate_boundary_distance_min, 1, -1, \
                                                                                        __PLATE_BNDY_TF_DIST_RED_CUTOFF + maxHorUnc,
                                                                                        __PLATE_BNDY_TF_DIST_YELLOW_CUTOFF + maxHorUnc, \
                                                                                        "GREY", flag_config__event_info__tsunami_decision_table_colors_show)
                    closest_bndry_dist_min_transform_fault = closest_plate_boundary_distance_min

    # Interplate Thrust
    # Interplate Thrust
    if plate_boundary_color_interplate_thrust == "RED" or plate_boundary_color_interplate_thrust == "YELLOW":
        text_thrust = "YES (" + str(int(0.5 + closest_bndry_dist_min_interplate_thrust)) + "km)"
    else:
        text_thrust = "No"

    # Thrust Fault
    if plate_boundary_color_thrust_fault == "RED" or plate_boundary_color_thrust_fault == "YELLOW":
        text_fault = "YES (" + str(int(0.5 + closest_bndry_dist_min_interplate_thrust)) + "km)"
    else:
        text_fault = "No"

    # Transform Fault
    if plate_boundary_color_transform_fault == "RED" or plate_boundary_color_transform_fault == "YELLOW":
        text_trasform_fault = "YES (" + str(int(0.5 + closest_bndry_dist_min_interplate_thrust)) + "km)"
    else:
        text_trasform_fault = "No"

    # Underater_color
    under_water_color = evaluateLevelColorIncreasing(ipercent_prob_underwater, 1, -1, __UNDERWATER_RED_CUTOFF, \
                                                    __UNDERWATER_YELLOW_CUTOFF, "GREY", \
                                                    flag_config__event_info__tsunami_decision_table_colors_show)

    # depth_color
    depth_color = evaluateLevelColorDecreasing(depth, 1, -1, __SLAB_DEPTH_RED_CUTOFF, __SLAB_DEPTH_YELLOW_CUTOFF, \
													   "GREY", flag_config__event_info__tsunami_decision_table_colors_show)

    if is_inside_slab and slab_depth != EvaluateEvent.SLAB_DEPTH_ERROR:
        slab_depth_color = evaluateLevelColorDecreasing(slab_depth, 1, -1, __SLAB_DEPTH_RED_CUTOFF, \
                                                      __SLAB_DEPTH_YELLOW_CUTOFF, "GREY", \
                                                      flag_config__event_info__tsunami_decision_table_colors_show)
    else:
        slab_depth_color = "GREY"


    # Mwp color
    if(mag != 'None'):
        mag_color = evaluateLevelColorIncreasing(mag, nr_mag, __MIN_NUMBER_MWP_ALARM, __MWP_RED_CUTOFF, __MWP_YELLOW_CUTOFF, \
                                                 "LTGREEN", flag_config__event_info__tsunami_decision_table_colors_show)
    else:
        mag_color = 'LTGREEN'
        mag_text  = '-'

    # TdT0
    if(TdT0 != 'None'):
        tdt0_color = evaluateLevelColorIncreasing(tdt0_value, inum_tdt0, __MIN_NUMBER_WARNING_LEVELS_TDT0, \
                                                  __TDT0_RED_CUTOFF, __TDT0_YELLOW_CUTOFF, \
                                                  "GREY", flag_config__event_info__tsunami_decision_table_colors_show)
    else:
        tdt0_color = "GREY"
        tdt0_text = "-"

    # TdT50Ex
    if(TdT50Ex != 'None'):
        TdT50Ex_color = evaluateLevelColorIncreasing(TdT50Ex, inum_TdT50Ex, __MIN_NUMBER_WARNING_LEVELS_ALARM,
                                                __ALARM_RED_CUTOFF, __ALARM_YELLOW_CUTOFF, \
                                                "LTGREEN", flag_config__event_info__tsunami_decision_table_colors_show)
    else:
        TdT50Ex_color = "LTGREEN"
        TdT50Ex_text = "-"

    """
    print(plate_boundary_color_interplate_thrust, plate_boundary_color_thrust_fault, plate_boundary_color_transform_fault)
    print(text_thrust, text_fault, text_trasform_fault)
    print(under_water_color)
    print(TdT50Ex_color)
    print(tdt0_color)
    print(mag_color)
    print(depth_color)
    print(slab_depth_color)
    """

    tsunamigenic_assesment            = dict()
    discriminants                     = dict()
    sub_geometry                      = dict()
    decision_table                    = dict()

    decision_table['event_type']              = ['Subduction Zone','Other Thrust/Normal','Strike-slip']
    decision_table['Compatible_close_plate_boundary_text'] = [text_thrust, text_fault, text_trasform_fault]
    decision_table['Compatible_close_plate_boundary_color'] = [plate_boundary_color_interplate_thrust, plate_boundary_color_thrust_fault, plate_boundary_color_transform_fault]
    decision_table['prob_underwater_text']    = [prob_underwater_text]
    decision_table['prob_underwater_color']   = [under_water_color]
    decision_table['TdT50Ex_color'] = [TdT50Ex_color]
    decision_table['TdT50Ex_value'] = [TdT50Ex_text]
    decision_table['tdt0_value'] = [tdt0_text]
    decision_table['tdt0_color'] = [tdt0_color]
    decision_table['Mwp_magnitude_text'] = [mag_text]
    decision_table['Mwp_magnitude_color'] = [mag_color]
    decision_table['Hypocenter_depth_text'] = ("%d [km]" % (depth) )
    decision_table['Hypocenter_depth_color'] = [depth_color]
    decision_table['slab_depth_text'] = [slab_depth_text]
    decision_table['slab_depth_color'] = [slab_depth_color]



    sub_geometry['zone']                      = slab_text
    sub_geometry['Slab_depth_at_epicenter']   = slab_depth_text

    discriminants['T50Ex']                    = T50Ex
    discriminants['T50Ex_nr']                 = T50Ex_nr
    discriminants['TdT50Ex']                  = TdT50Ex
    discriminants['TdT50Ex_nr']               = inum_TdT50Ex
    discriminants['Td']                       = Td
    discriminants['Td_nr']                    = Td_nr
    discriminants['T0']                       = T0
    discriminants['T0_nr']                    = T0_nr
    discriminants['Subduction_geometry']      = sub_geometry
    discriminants['Closest_plate_boundaries'] = closest_plate_boundaries

    tsunamigenic_assesment['origin_id']       = origin_id
    tsunamigenic_assesment['event_id']        = event_id
    tsunamigenic_assesment['latitude']        = lat
    tsunamigenic_assesment['longitude']       = lon
    tsunamigenic_assesment['depth']           = depth
    tsunamigenic_assesment['Discriminants']   = discriminants
    tsunamigenic_assesment['Decision_table']  = decision_table


    print(tsunamigenic_assesment)
    #print(closest_plate_boundaries)
    print(json.dumps(tsunamigenic_assesment, indent=4))
