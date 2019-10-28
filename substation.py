
import pandas as pd
import numpy as np

df = pd.read_excel(r'D:\Work\Python\PycharmProjects\pythonRepository\example.xlsx', header=0, index_col=0)
print(df)

# get the column value of the specified feature: max, min, mean, median
#tmp = df.get(max)
#print(tmp)


class substation:

    def __init__(self, substation_df, feature, pressure_allowed_error, temperature_allowed_error, flow_allowed_error, seoncdary_return_min_pressure):
        self.substation_df = substation_df
        self.substation_data = self.substation_df.get(feature)
        self.substation_data_mean_dev = self.substation_df.get('mean_dev') # absolute mean deviation
        self.pressure_margin = pressure_allowed_error # unit in kPa
        self.temperature_margin = temperature_allowed_error # unit in degrees
        self.flow_margin = flow_allowed_error # unit in ton/h
        self.secondary_return_min_pressure = seoncdary_return_min_pressure # unit in kPa


    def assign_values(self):
        # assign values of substation to each individual variables
        self.TT11 = self.substation_data['TT11'] # departure temp on primary side
        self.TT12 = self.substation_data['TT12'] # return temp on primary side
        self.TT21 = self.substation_data['TT21'] # departure temp on secondary side
        self.TT22 = self.substation_data['TT22'] # return temp on secondary side
        self.PT11 = self.substation_data['PT11'] # supply pressure on primary side
        self.PT1A = self.substation_data['PT1A'] # supply pressure on primary side before y-filter # NOT YET
        self.PT1B = self.substation_data['PT1B'] # supply pressure on primary side after electric control valve # NOT YET
        self.PT12 = self.substation_data['PT12'] # return pressure on primary side
        self.PT21 = self.substation_data['PT21'] # supply pressure on secondary side
        self.PT22 = self.substation_data['PT22'] # return pressure on secondary side before y-filter # NOT YET
        self.PT23 = self.substation_data['PT23'] # return pressure on secondary side before pump
        self.PT24 = self.substation_data['PT24'] # return pressure on secondary side after pump # NOT YET
        self.FT11 = self.substation_data['FT11'] # instantaneous flow rate on primary
        self.HT11 = self.substation_data['HT11'] # instantaneous heat transferred on primary side
        self.FT30 = self.substation_data['FT30'] # instantaneous make-up water flow rate
        self.CV01 = self.substation_data['CV01'] # electric control valve opening
        self.CP01 = self.substation_data['CP01'] # frequency of circulation pump
        self.TT00 = self.substation_data['TT00'] # outdoor temp
        self.TT01 = self.substation_data['TT01'] # indoor temp after compensation
        self.JS_PT11 = self.substation_data['JS_PT11'] # departure pressure in well
        self.JS_PT12 = self.substation_data['JS_PT12'] # return pressure in well
        self.JS_TT11 = self.substation_data['JS_TT11'] # departure temp in well
        self.JS_TT12 = self.substation_data['JS_TT12'] #　return temp in well

        self.TT23 = self.substation_data['TT23'] # safety valve water temperature
        self.surface = self.substation_data['surface'] # total heated area
        self.other_temp = self.substation_data['other_temp'] # average temperature of other unit of same kind
        self.HD101 = self.substation_data['HD101'] # total heat produced by plant
        #self.HV31 = self.substation_data['HV31'] # make-up water valve feedback
        #self.HV41 = self.substation_data['HV41'] # over-pressure discharge valve feedback

        self.CV01_mean_dev = self.substation_data_mean_dev['CV01']
        self.FT30_mean_dev = self.substation_data_mean_dev['FT30']

    def print_data(self):
        print(self.substation_data)

    def move_data(self):
        # move current data set to another place for further use
        self.substation_data_prev = self.substation_data
        self.substation_data = []

    def clear_data(self):
        self.substation_df = []
        self.substation_data = []

    def calculate_secondary_supply_temperature(self, list_outdoor_temp, list_water_temp):
        if self.TT00>list_outdoor_temp[0]:
            setting_water_temp = list_water_temp[0]
        elif list_outdoor_temp[1] < self.TT00 <= list_outdoor_temp[0]:
            rate_of_change_temp = (float(list_water_temp[1])-float(list_water_temp[0]))/(float(list_outdoor_temp[1])-float(list_outdoor_temp[0]))
            setting_water_temp = float(list_water_temp[1]) + (self.TT00-list_outdoor_temp[1])*rate_of_change_temp
        elif list_outdoor_temp[2] < self.TT00 <= list_outdoor_temp[1]:
            rate_of_change_temp = (float(list_water_temp[2])-float(list_water_temp[1]))/(float(list_outdoor_temp[2])-float(list_outdoor_temp[1]))
            setting_water_temp = float(list_water_temp[2]) + (self.TT00-list_outdoor_temp[2])*rate_of_change_temp
        elif list_outdoor_temp[3] <self.TT00<=list_outdoor_temp[2]:
            rate_of_change_temp = (float(list_water_temp[3])-float(list_water_temp[2]))/(float(list_outdoor_temp[3])-float(list_outdoor_temp[2]))
            setting_water_temp = float(list_water_temp[3]) + (self.TT00 - list_outdoor_temp[3]) * rate_of_change_temp
        elif list_outdoor_temp[4] <self.TT00<=list_outdoor_temp[3]:
            rate_of_change_temp = (float(list_water_temp[4])-float(list_water_temp[3]))/(float(list_outdoor_temp[4])-float(list_outdoor_temp[3]))
            setting_water_temp = float(list_water_temp[4]) + (self.TT00 - list_outdoor_temp[4]) * rate_of_change_temp
        elif list_outdoor_temp[5] <self.TT00<=list_outdoor_temp[4]:
            rate_of_change_temp = (float(list_water_temp[5])-float(list_water_temp[4]))/(float(list_outdoor_temp[5])-float(list_outdoor_temp[4]))
            setting_water_temp = float(list_water_temp[5]) + (self.TT00 - list_outdoor_temp[5]) * rate_of_change_temp
        return setting_water_temp

    def calculate_unit_flow_heat(self):
        if self.FT11<self.flow_margin:
            unit_flow_heat=0
        else:
            unit_flow_heat = (self.HD101/self.surface-self.HT11)/self.HT11
        return unit_flow_heat

    def calculate_electric_valve_status(self):
        if self.CV01_mean_dev*15>0.03*5:
            steady = 0
        else: steady = 1 # if electric valve is in steady status
        return steady

## example of conditional alerts follows
    def alert_ball_valve_off_primary_departure(self, supply_water_temp):
        if self.PT11-self.JS_PT12<self.pressure_margin and self.PT12-self.JS_PT12 <self.pressure_margin and self.PT1A-self.JS_PT12<self.pressure_margin and self.PT1B-self.JS_PT12<self.pressure_margin and self.PT11<self.JS_PT11 and self.PT12<self.JS_PT11 and self.PT1A<self.JS_PT11 and self.PT1B<self.JS_PT11:
            if self.PT1A-self.PT11<self.pressure_margin and self.PT11-self.PT1B<self.pressure_margin and self.PT1B-self.PT12<self.pressure_margin:
                if self.JS_TT11-self.TT11>20 and self.JS_TT11-self.TT12>20 and supply_water_temp-self.TT21<5:
                    if self.TT22<supply_water_temp-20:
                        if self.TT21-self.TT22<self.temperature_margin:
                            if self.FT11<self.flow_margin: # if flow is less than 0.2, assume it to be 0
                                print("ball valve is OFF on primary departure side")
        """
                            else: print("ball valve on primary departure side is in normal status")
                        else: print("ball valve on primary departure side is in normal status")
                    else: print("ball valve on primary departure side is in normal status")
                else: print("ball valve on primary departure side is in normal status")
            else: print("ball valve on primary departure side is in normal status")
        else: print("ball valve on primary departure side is in normal status")
        """

    def alert_ball_valve_off_primary_return(self, supply_water_temp):
        if self.JS_PT11-self.TT11<self.pressure_margin and self.JS_PT11-self.PT12<self.pressure_margin and self.JS_PT11-self.PT1A<self.pressure_margin and self.JS_PT11-self.PT1B<self.pressure_margin and self.PT11>self.JS_PT12 and self.PT12>self.JS_PT12 and self.PT1A>self.JS_PT12 and self.PT1B>self.JS_PT12:
            if self.PT1A-self.PT11<self.pressure_margin and self.PT11-self.PT1B<self.pressure_margin and self.PT1B-self.PT12<self.pressure_margin:
                if self.JS_TT11 - self.TT11 > 20 and self.JS_TT11 - self.TT12 > 20 and supply_water_temp-self.TT21<5:
                    if self.TT22 < supply_water_temp - 20:
                        if self.TT21 - self.TT22 < self.temperature_margin:
                            if self.FT11 < self.flow_margin:  # if flow is less than 0.2, assume it to be 0
                                print("ball valve is OFF on primary return side")
        """
                            else: print("ball valve on primary return side is in normal status")
                        else: print("ball valve on primary return side is in normal status")
                    else: print("ball valve on primary return side is in normal status")
                else: print("ball valve on primary return side is in normal status")
            else: print("ball valve on primary return side is in normal status")
        else: print("ball valve on primary return side is in normal status")
        """

    def alert_y_filter_blocked_primary_departure(self, supply_water_temp, unit_flow_heat):
        if self.PT1A-self.PT11>50:
            if supply_water_temp-self.TT21>5:
                if self.TT22<supply_water_temp-20:
                    if self.JS_TT12 - self.TT12 > 10:
                        if self.TT21-self.TT22<5:
                            if unit_flow_heat>0.3:
                                print("y filter is BLOCKED on primary departure side")
        """
                            else: print("y filter on primary departure side is in normal status")
                        else: print("y filter on primary departure side is in normal status")
                    else: print("y filter on primary departure side is in normal status")
                else: print("y filter on primary departure side is in normal status")
            else: print("y filter on primary departure side is in normal status")
        else: print("y filter on primary departure side is in normal status")
        """

    def alert_electric_contorl_valve_off(self):
        if self.PT1A-self.PT11<self.pressure_margin and self.PT1B-self.PT12<self.pressure_margin:
            if self.JS_TT11 - self.TT11 > 20 and self.JS_TT11 - self.TT12 > 20:
                if self.TT21 - self.TT22 < self.temperature_margin:
                    if self.FT11 < self.flow_margin:
                        print("electric control valve is OFF")
        """
                    else: print("electric control valve is in normal status")
                else: print("electric control valve is in normal status")
            else: print("electric control valve is in normal status")
        else: print("electric control valve is in normal status")
        """

    def alert_electric_contorl_valve_blocked(self, supply_water_temp, unit_flow_heat):
        if self.PT11-self.PT1B>50:
            if supply_water_temp-self.TT21>5:
                if self.JS_TT12-self.TT12>10:
                    if self.TT21-self.TT22<5:
                        if unit_flow_heat>0.3:
                            print("electric control valve is BLOCKED")
        """
                        else: print("electric control valve is in normal status")
                    else: print("electric control valve is in normal status")
                else: print("electric control valve is in normal status")
            else: print("electric control valve is in normal status")
        else: print("electric control valve is in normal status")
        """

    def alert_electric_contorl_valve_CANNOT_off(self,supply_water_temp, unit_flow_heat):
        if self.TT21-supply_water_temp>5:
            if self.TT12-self.other_temp>10:
                if self.TT21-self.TT22<5:
                    if unit_flow_heat>0.3:
                        print("electric control valve CANNOT be turned OFF")
        """
                    else: print("electric control valve is in normal status")
                else: print("electric control valve is in normal status")
            else: print("electric control valve is in normal status")
        else: print("electric control valve is in normal status")
        """

    def alert_electric_control_valve_fault(self, supply_water_temp, steady):
        if abs(supply_water_temp-self.TT21)>5:
            if (0.98<self.CV01<1.02 or -0.02<self.CV01<0.02) and supply_water_temp-self.TT21>5:
                if not (steady):
                    print("electric control valve is malfunctioning")
        """
                else: print("electric control valve is in normal status")
            else: print("electric control valve is in normal status")
        else: print("electric control valve is in normal status")
        """

    def alert_heat_exchanger_BLOCKED_primary(self, supply_water_temp, unit_flow_heat):
        if self.PT1B-self.PT12>50:
            if supply_water_temp-self.TT21>5:
                if self.TT21-self.TT22<5:
                    if unit_flow_heat >0.3:
                        print("heat exchanger is BLOCKED on the primary side")
        """
                    else: print("heat exchanger on the primary side is in normal status")
                else: print("heat exchanger on the primary side is in normal status")
            else: print("heat exchanger on the primary side is in normal status")
        else: print("heat exchanger on the primary side is in normal status")
        """

    def alert_heat_exchanger_dirty_primary(self, supply_water_temp, unit_flow_heat):
        if self.PT1B-self.PT12>50 or self.PT24-self.PT23>60:
            if supply_water_temp-self.TT21>5:
                if self.TT21-self.TT22<5:
                    if unit_flow_heat>0.3:
                        print("heat exchanger is dirty on the primary side")
        """
                    else: print("heat exchanger on the primary side is in normal status")
                else: print("heat exchanger on the primary side is in normal status")
            else: print("heat exchanger on the primary side is in normal status")
        else: print("heat exchanger on the primary side is in normal status")
        """

    def alert_heat_exchanger_leakage(self, supply_water_temp, steady):
        if self.CV01<0.05 and self.TT21-supply_water_temp>5:
            if not steady:
                print("heat exchanger is leaking")
        """
            else: print("heat exchanger is in normal status")
        else:print("heat exchanger is in normal status")
        """

    def alert_heat_meter_dirty(self, unit_flow_heat):
        if abs(supply_water_temp-self.TT21)>5:
            if unit_flow_heat>0.3:
                print("heat meter is dirty")
        """
            else: print("heat meter is in normal status")
        else: print("heat meter is in normal status")
        """

    def alert_heat_meter_fault(self, unit_flow_heat):
        if unit_flow_heat>0.3:
            if self.TT21-self.TT22>5 and (self.FT11<self.flow_margin or self.FT11>100-self.flow_margin):
                print("heat meter is malfunctioning")
        """
            else: print("heat meter is in normal status")
        else: print("heat meter is in normal status")
        """

    def alert_heat_meter_gas(self, unit_flow_heat):
        if unit_flow_heat>0.3:
            if self.TT21-self.TT22>5 and (self.FT11<self.flow_margin or self.FT11>100-self.flow_margin):
                print("heat meter contains gas")
        """
            else: print("heat meter is in normal status")
        else: print("heat meter is in normal status")
        """

    def alert_ball_valve_off_secondary_departure(self):
        if self.PT24-self.PT21<20 and self.PT22-self.PT24<20:
            if self.TT21-self.TT22<5:
                if self.TT11-self.TT12<5:
                    print("ball valve is OFF on secondary departure side")
        """
                else: print("ball valve on secondary departure side is in normal status")
            else: print("ball valve on secondary return side is in normal status")
        else: print("ball valve on secondary return side is in normal status")
        """

    def alert_ball_valve_off_secondary_return(self):
        if self.PT24-self.PT21<20 and self.PT22-self.PT23<20:
            if self.PT24-self.PT23>100 and self.PT21-self.PT23>100:
                if self.TT21-self.TT22<5:
                    if self.TT11-self.TT12<5:
                        print("ball valve is OFF on secondary return side")
        """
                    else: print("ball valve on secondary return side is in normal status")
                else: print("ball valve on secondary return side is in normal status")
            else: print("ball valve on secondary return side is in normal status")
        else: print("ball valve on secondary return side is in normal status")
        """

    def alert_y_filter_BLOCKED_secondary_return(self, unit_flow_heat):
        if self.PT22-self.PT23>50:
            if self.TT21-self.TT22>20:
                if unit_flow_heat<0.6:
                    print("y-filter is BLOCKED on the secondary return side")
        """
                else: print("y filter on secondary return side is in normal status")
            else: print("y filter on secondary return side is in normal status")
        else: print("y filter on secondary return side is in normal status")
        """

    def alert_safety_valve_off(self):
        if self.PT23-self.secondary_return_min_pressure>300:
            print("safety valve is OFF")
        """
        else: print("safety valve is in normal status")
        """

    def alert_safety_valve_CANNOT_off(self):
        if self.secondary_return_min_pressure-self.PT23>300:
            if self.TT23>30:
                if self.FT30>8:
                    print("safety valve CANNOT be turned OFF")
        """
                else: print("safety valve is in normal status")
            else: print("safety valve is in normal status")
        else: print("safety valve is in normal status")
        """

    def alert_circulation_pump_fault(self, unit_flow_heat):
        if self.PT24-self.PT23<30:
            if unit_flow_heat<0.6:
                if self.PT22-self.PT23<self.pressure_margin and self.PT22-self.PT24<self.pressure_margin and self.PT22-self.PT21<self.pressure_margin:
                    if self.PT24-self.PT23<30:
                        print("circulation pump is malfunctioning")
        """
                    else: print("circulation pump is in normal status"\)
                else: print("circulation pump is in normal status")
            else: print("circulation pump is in normal status")
        else: print("circulation pump is in normal status")
        """

    def alert_heat_exchanger_BLOCKED_secondary(self, steady, unit_flow_heat):
        if self.PT24-self.PT21>60 and self.PT24-self.PT23>100:
            if self.TT21-self.TT22>20:
                if not steady:
                    if unit_flow_heat<0.6:
                        print("heat exchanger is BLOCKED on the secondary side")
        """
                    else: print("heat exchanger on the secondary side is in normal status")
                else: print("heat exchanger on the secondary side is in normal status")
            else: print("heat exchanger on the secondary side is in normal status")
        else: print("heat exchanger on the secondary side is in normal status")
        """

    def alert_heat_exchanger_dirty_secondary(self, supply_water_temp, unit_flow_heat, steady):
        if supply_water_temp-self.TT21>5:
            if self.TT12-self.other_temp>10:
                if unit_flow_heat>0.3:
                    if steady and (98.8<=self.CV01<=100.02):
                        print("heat exchanger is dirty on the secondary side")
        """
                    else: print("heat exchanger on the primary side is in normal status")
                else: print("heat exchanger on the primary side is in normal status")
            else: print("heat exchanger on the primary side is in normal status")
        else: print("heat exchanger on the primary side is in normal status")
        """

    def alert_mix_water_valve_off(self):
        if self.PT24-self.PT21>60:
            print("mix water valve is OFF")
        """
        else: print("mix water valve is in normal status")
        """

    def alert_mix_water_valve_CANNOT_off(self, supply_water_temp):
        if supply_water_temp-self.TT21>5:
            if self.TT11-self.TT12<5:
                if self.TT12-self.other_temp>10:
                    print("mix water valve CANNOT be turned off")
        """
                else: print("mix water valve is in normal status")
            else: print("mix water valve is in normal status")
        else: print("mix water valve is in normal status")
        """

    def alert_over_pressure_water_discharge_valve_off(self):
        if self.PT23-self.secondary_return_min_pressure>150:
            print("over pressure water discharge valve is OFF")
        """
        else: print("over pressure water discharge valve is in normal status")
        """

    def alert_over_pressure_water_discharge_valve_BLOCKED(self):
        if self.PT23-self.secondary_return_min_pressure>150:
            if self.TT23>30:
                print("over pressure water discharge valve is BLOCKED")
        """
            else: print("over pressure water discharge valve is in normal status")
        else: print("over pressure water discharge valve is in normal status")
        """
    def alert_over_pressure_water_discharge_valve_CANNOT_off(self):
        if self.secondary_return_min_pressure-self.PT23>300:
            if self.TT23>30:
                if self.FT30>8:
                    print("over pressure water discharge valve CANNOT be turned off")
        """
                else: print("over pressure water discharge valve is in normal status")
            else: print("over pressure water discharge valve is in normal status")
        else: print("over pressure water discharge valve is in normal status")
        """

    """
    def alert_over_pressure_water_discharge_valve_fault(self):
        if self.HV41 ==1:
            if abs(self.PT23-self.secondary_return_min_pressure)>100:
                print("over pressure water discharge valve is malfunctioning")
            else: print("over pressure water discharge valve is in normal status")
        else: print("over pressure water discharge valve is in normal status")
    """

    def alert_make_up_water_flow_meter_fault(self):
        if self.HT11<0.1 or self.HT11>99.9:
            if self.FT30_mean_dev<0.1:
                if self.FT30>8:
                    print("make-up water flow indicator is malfunctioning")
        """
                else: print("make-up water flow indicator is in normal status")
            else: print("make-up water flow indicator is in normal status")
        else: print("make-up water flow indicator is in normal status")
        """

    def alert_make_up_water_valve_off(self):
        if self.secondary_return_min_pressure-self.PT23>300:
            if self.FT30<self.flow_margin:
                print("make-up water valve is OFF")
        """
            else: print("make-up water valve is in normal status")
        else: print("make-up water valve is in normal status")
        """

    def alert_make_up_water_valve_BLOCKED(self):
        if self.secondary_return_min_pressure-self.PT23>200:
            if self.FT30<self.flow_margin:
                print("make-up water valve is BLOCKED")
        """
            else: print("make-up water valve is in normal status")
        else: print("make-up water valve is in normal status")
        """

    def alert_make_up_water_valve_CANNOT_off(self):
        if self.PT23-self.secondary_return_min_pressure>150:
            if self.FT30>2.5: # make-up water continuously above 2.5 ton/h
                print("make-up water valve CANNOT be turned off")
        """
            else: print("make-up water valve is in normal status")
        else: print("make-up water valve is in normal status")
        """

    """
    def alert_make_up_water_valve_fault(self):
        if self.HT11<0.1 or self.HT11>100:
            if self.HV31 == 0:
                if self.FT30_mean_dev < 0.1:
                    print("make-up water valve is malfunctioning")
                else: print("make-up water valve is in normal status")
            else: print("make-up water valve is in normal status")
        else: print("make-up water valve is in normal status")
    """

## test module
sub1 = substation(df,min,10, 2, 0.2, 490)

# assign values to the object
sub1.assign_values()
#print(sub1.TT00)

# calculate the corresponding supply water temperature on the secondary side
supply_water_temp = sub1.calculate_secondary_supply_temperature(list_outdoor_temp=[15,7,5,0,-5,-10], list_water_temp=[22,30.8,33,38.5,44,49.5])
unit_flow_heat = sub1.calculate_unit_flow_heat()
steady = sub1.calculate_electric_valve_status()
#print(unit_flow_heat)

sub1.alert_ball_valve_off_primary_departure(supply_water_temp)
sub1.alert_ball_valve_off_primary_return(supply_water_temp)

sub1.alert_y_filter_blocked_primary_departure(supply_water_temp, unit_flow_heat)

sub1.alert_electric_contorl_valve_off()
sub1.alert_electric_contorl_valve_blocked(supply_water_temp, unit_flow_heat)
sub1.alert_electric_contorl_valve_CANNOT_off(supply_water_temp, unit_flow_heat)
sub1.alert_electric_control_valve_fault(supply_water_temp,steady)

sub1.alert_heat_exchanger_BLOCKED_primary(supply_water_temp,unit_flow_heat)
sub1.alert_heat_exchanger_dirty_primary(supply_water_temp,unit_flow_heat)
sub1.alert_heat_exchanger_leakage(supply_water_temp,steady)

sub1.alert_heat_meter_dirty(unit_flow_heat)
sub1.alert_heat_meter_fault(unit_flow_heat)
sub1.alert_heat_meter_gas(unit_flow_heat)

sub1.alert_ball_valve_off_secondary_departure()
sub1.alert_ball_valve_off_secondary_return()
sub1.alert_y_filter_BLOCKED_secondary_return(unit_flow_heat)

sub1.alert_safety_valve_off()
sub1.alert_safety_valve_CANNOT_off()

sub1.alert_circulation_pump_fault(unit_flow_heat)

sub1.alert_heat_exchanger_BLOCKED_secondary(steady,unit_flow_heat)
sub1.alert_heat_exchanger_dirty_secondary(supply_water_temp,unit_flow_heat,steady)

sub1.alert_mix_water_valve_off()
sub1.alert_mix_water_valve_CANNOT_off(supply_water_temp)

sub1.alert_over_pressure_water_discharge_valve_off()
sub1.alert_over_pressure_water_discharge_valve_BLOCKED()
sub1.alert_over_pressure_water_discharge_valve_CANNOT_off()
#sub1.alert_over_pressure_water_discharge_valve_fault()

sub1.alert_make_up_water_flow_meter_fault()

sub1.alert_make_up_water_valve_off()
sub1.alert_make_up_water_valve_BLOCKED()
sub1.alert_make_up_water_valve_CANNOT_off()
#sub1.alert_make_up_water_valve_fault()


#sub1.move_data()
#print(sub1.substation_data_prev)
#print(sub1.substation_data)

#sub1.clear_data()
#print(sub1)
#sub1.print_data()

