import greetuser
import math
import converters
print('Please note, flat slab design of this module accommodates single panel only')
print('''Further assumption is that each singular panel is supported at corners by four(4) Columns,
Enter all dimensions in mm''')

print('SLAB PARAMETERS')
# Place potential valueerror try/except in while loops later

try:
    short_span = int(input('lx= '))
    long_span = int(input('ly= '))
except ValueError:
    print('Parameters must be integers')

count = 0
limit = 3
while count < limit:
    slab_depth = int(input('Slab thickness(h)= '))
    count += 1
    if slab_depth > 125:
        break
    else:
        print('Slab thickness cannot be lesser than 125mm as per BS 8110(1997)')
while count < limit:
    drop_depth = int(input('Drop thickness= '))
    count += 1
    if drop_depth > 125:
        break
    else:
        print('Drop thickness cannot be lesser than 125mm as per BS 8110(1997)')
slab_cover = int(input('Slab cover(c)= '))
internal = 'I'
external = 'E'
# Necessary to keep user aware of column location
column_type1 = input("Majorly Internal or External Column (I or E)> ")
head_depth = int(input('Column head depth(dh)= '))
rectangular = 'R'
squares = 'S'
circular = 'C'
column_type = input('''Rectangular = R, Squares = S or Circular = C
Column Type = ''')
if column_type.upper() == rectangular:
    rcolumn_section1 = int(input('Least Column dim. in dir. 1= '))
    rcolumn_section2 = int(input('Column dim. in dir. 2= '))
    e_column_head1 = rcolumn_section1 + 2 *(head_depth - 40)
    print(f'Column Section= {rcolumn_section1}x{rcolumn_section2}mm')
elif column_type.upper() == squares:
    scolumn_section = int(input('Column width = '))
    e_column_head1 = scolumn_section + 2 *(head_depth - 40)
    print(f'Column Section= {scolumn_section}mm squares')
else:
    ccolumn_section = int(input('Column Diameter = '))
    e_column_head1 = ccolumn_section + 2 *(head_depth - 40)
    print(f'Column section= {ccolumn_section}mm dia ')
drop_size = short_span / 3
print(f'Drop size/Column Strip = {round(drop_size, 3)}mm')
middle_strip = long_span - drop_size
print(f'Middle Strip = {round(middle_strip, 3)}mm')
head_options = [e_column_head1, drop_size]
min = head_options[0]
for options in head_options:
    if min > options:
        min = options
print(f'Column Head Section= {round(min, 3)}mm')

print('LOAD AND ANALYSIS PARAMETERS')
conc_unit_weight = 24
conc_strength = int(input('fcu(N/mm²)= '))
steel_strength = int(input('fy(N/mm²)= '))
bar_dia = int(input('Bar dia.(∅mm)= '))
bar_area = math.pi * bar_dia**2 / 4
part_load = float(input('Partition load(KN/m²) = '))
serv_load = float(input('Service/Finishes load(KN/m²)= '))
imp_load = float(input('Imposed load(KN/m²)= '))
dead_load = slab_depth / 1000 * conc_unit_weight + part_load + serv_load
sls = dead_load + imp_load
uls = 1.4 * dead_load + 1.6 * imp_load
print(f'ULS = {uls}KN/m²')
conv_sspan = short_span / 1000
conv_lspan = long_span / 1000
conv_min = min / 1000
slab_load = uls * conv_sspan * conv_lspan
drop_load = slab_depth / 1000 * 1.4 * conc_unit_weight * (drop_size / 1000)**2
total_load = slab_load + drop_load
eq_load = total_load / (conv_lspan * conv_sspan)
print(f'Equivalent Load per m² = {round(eq_load, 3)}KN/m²')
d_hc = (conv_min**2 * 4 / math.pi)**0.5
if d_hc > conv_sspan / 4:
    hc = conv_min
else:
    hc = d_hc
eff_span = conv_sspan - (2 * hc / 3)
print('SLAB CONDITIONS/ MOMENT CONDITIONS')
simple_outer = 'SOS'
simple_middle = 'SMS'
cont_outer = 'COS'
cont_near_middle = 'CMS'
cont_interior = 'CIS'
end_condition = input('''ENTER CODE APPROPRIATELY
Simple Support(At Outer Support)= SOS
Simple Support(Near Middle of end Span)= SMS
Continuous Support(At Outer Support)= COS
Continuous Support(Near middle of end span)= CMS
Continuous Support(At first interior supports)= CIS
Enter = ''')
eff_depth1 = slab_depth - slab_cover - bar_dia / 2
eff_depth2 = slab_depth + drop_depth - slab_cover - bar_dia / 2
# print(total_load, eff_span)


def stiffness(moment1):
    return (moment1 * 10**6) / (conc_strength * (short_span - drop_size) * eff_depth1**2)


def k(col_mom):
    return (col_mom * 10**6) / (conc_strength * drop_size * eff_depth2**2)


def la(stiffness1):
    return 0.5 + (0.25 - stiffness1 / 0.9)**0.5


def a_steel(moment2, la0):
    return (moment2 * 10**6) / (0.87 * steel_strength * la0 * eff_depth1)


def a_steel_c(moment2, la0):
    return (moment2 * 10**6) / (0.87 * steel_strength * la0 * eff_depth2)


def bar_no(ast, a_bar):
    return ast * 1.1 / a_bar


min_as = 0.13 / 100 * (short_span - drop_size) * slab_depth
min_as_col = 0.13 / 100 * drop_size * slab_depth

if end_condition.upper() == simple_outer:
    moment = 0
    shear = 0.4 * total_load
    print(f'Moment = {round(moment, 2)}KNm  Shear = {round(shear, 2)}KN')
    print(f'As Min. = {round(min_as, 2)}mm²')
    bar = bar_no(min_as, bar_area)
    print(f'Provide {round(bar)}Y{bar_dia}')
    print()
    print('CHECKS')
    pre_m = moment * 10**6 / (short_span * eff_depth1**2)
    fs = (2 / 3) * steel_strength * min_as / (bar * bar_area)
    mod_factor = 0.55 + (477 - fs) / (120 * (0.9 + pre_m))
    d_req = short_span / (mod_factor * 20)
    if d_req < eff_depth1:
        print('Deflection is satisfactory')
    else:
        print('Deflection not satisfied, increase slab depth')
elif end_condition.upper() == simple_middle:
    moment = 0.086 * total_load * eff_span
    col_mom = 0.55 * moment
    mid_mom = 0.45 * moment
    print(f'Moment = {round(moment, 2)}KNm')
    k1 = k(col_mom)
    k2 = stiffness(mid_mom)
    if k1 > 0.156:
        print(' K > 0.156. Increase slab depth or design compression reinforcement, further analysis required')
    else:
        la1 = la(k1)
        aos = a_steel_c(col_mom, la1)
        if aos > min_as:
            print(f'Column Strip As required = {round(aos, 2)}mm²')
            bar = bar_no(aos, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        else:
            print(f'Column Strip As Min. required = {round(min_as, 2)}mm²')
            bar = bar_no(min_as, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
    if k2 > 0.156:
        print(' K > 0.156. Increase slab depth or design compression reinforcement, further analysis required')
    else:
        la2 = la(k2)
        aos = a_steel(mid_mom, la2)
        if aos > min_as:
            print(f'Middle Strip As required = {round(aos, 2)}mm²')
            bar = bar_no(aos, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        else:
            print(f'Middle Strip As Min. required = {round(min_as, 2)}mm²')
            bar = bar_no(min_as, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        print()
        print('CHECKS')
        pre_m = mid_mom * 10**6 / (short_span * eff_depth1**2)
        fs = (2 / 3) * steel_strength * aos / (bar * bar_area)
        mod_factor = 0.55 + (477 - fs) / (120 * (0.9 + pre_m))
        d_req = short_span / (mod_factor * 20)
        if d_req < eff_depth1:
            print('Deflection is satisfactory')
        else:
            print('Deflection not satisfied, increase slab depth')
elif end_condition.upper() == cont_outer:
    neg_moment = 0.04 * total_load * eff_span
    pos_moment = 0.083 * total_load * eff_span
    col_neg_moment = 0.75 * neg_moment
    col_pos_moment = 0.55 * pos_moment
    mid_neg_moment = 0.25 * neg_moment
    mid_pos_moment = 0.45 * pos_moment
    k1 = k(col_neg_moment)
    if k1 > 0.156:
        print('K1 > 0.156. Increase head depth or design compression reinforcement, further analysis required')
    else:
        la1 = la(k1)
        aos1 = a_steel_c(col_neg_moment, la1)
        if aos1 > min_as_col:
            print(f'Column Strip Edge-As required = {round(aos1, 2)}mm²')
            bar = bar_no(aos1, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        else:
            print(f'Column Strip Edge-As required = {round(min_as_col, 2)}mm²')
            bar = bar_no(min_as_col, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
    # put la after each k
    k2 = k(col_pos_moment)
    if k2 > 0.156:
        print('K2 > 0.156. Increase head depth or design compression reinforcement, further analysis required')
    else:
        la2 = la(k2)
        aos2 = a_steel_c(col_pos_moment, la2)
        if aos2 > min_as_col:
            print(f'Column Strip Span-As required = {round(aos2, 2)}mm²')
            bar = bar_no(aos2, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        else:
            print(f'Column Strip Span-As required = {round(min_as_col, 2)}mm²')
            bar = bar_no(min_as_col, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
    k3 = stiffness(mid_neg_moment)
    if k3 > 0.156:
        print('K3 > 0.156. Increase slab depth or design compression reinforcement, further analysis required')
    else:
        la3 = la(k3)
        aos3 = a_steel(mid_neg_moment, la3)
        if aos3 > min_as:
            print(f'Middle Strip Edge-As required = {round(aos3, 2)}mm²')
            bar = bar_no(aos3, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        else:
            print(f'Middle Strip Edge-As required = {round(min_as, 2)}mm²')
            bar = bar_no(min_as, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
    k4 = stiffness(mid_pos_moment)
    if k4 > 0.156:
        print('K4 > 0.156. Increase slab depth or design compression reinforcement, further analysis required')
#    stiffness_class = [k1, k2, k3, k4]
#   for number in stiffness_class:
    else:
        la4 = la(k4)
        aos4 = a_steel(mid_pos_moment, la4)
        if aos4 > min_as:
            print(f'Middle Strip Span-As required = {round(aos4, 2)}mm²')
            bar = bar_no(aos4, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        else:
            print(f'Middle Strip Span-As required = {round(min_as, 2)}mm²')
            bar = bar_no(min_as, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        print()
        print('CHECKS')
        pre_m = mid_pos_moment * 10**6 / (short_span * eff_depth1**2)
        fs = (2 / 3) * steel_strength * aos4 / (bar * bar_area)
        mod_factor = 0.55 + (477 - fs) / (120 * (0.9 + pre_m))
        d_req = short_span / (mod_factor * 26)
        if d_req < eff_depth1:
            print('Deflection is satisfactory')
        else:
            print('Deflection not satisfied, increase slab depth')
    shear = 0.46 * total_load
#    print(f'Column Strip Negative Moment = {col_neg_moment}KNm  Shear = {shear}KN')

elif end_condition.upper() == cont_near_middle:
    moment = 0.075 * total_load * eff_span
    col_mom = 0.55 * moment
    mid_mom = 0.45 * moment
    print(f'Moment = {round(moment, 2)}KNm')
    k1 = k(col_mom)
    k2 = stiffness(mid_mom)
    if k1 > 0.156:
        print('K > 0.156. Increase head depth or design compression reinforcement, further analysis required')
    else:
        la1 = la(k1)
        aos = a_steel_c(col_mom, la1)
        if aos > min_as:
            print(f'Column Strip As required = {round(aos, 2)}mm²')
            bar = bar_no(aos, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        else:
            print(f'Column Strip As min. required = {round(min_as, 2)}mm²')
            bar = bar_no(min_as, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
    if k2 > 0.156:
        print('K2 > 0.156. Increase slab depth or design compression reinforcement, further analysis required')
    else:
        la2 = la(k2)
        aos = a_steel(mid_mom, la2)
        if aos > min_as:
            print(f'Middle Strip As required = {round(aos, 2)}mm²')
            bar = bar_no(aos, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        else:
            print(f'Middle Strip As min. required = {round(min_as, 2)}mm²')
            bar = bar_no(min_as, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        print()
        print('CHECKS')
        pre_m = mid_mom * 10**6 / (short_span * eff_depth1**2)
        fs = (2 / 3) * steel_strength * aos / (bar * bar_area)
        mod_factor = 0.55 + (477 - fs) / (120 * (0.9 + pre_m))
        d_req = short_span / (mod_factor * 26)
        if d_req < eff_depth1:
            print('Deflection is satisfactory')
        else:
            print('Deflection not satisfied, increase slab depth')
else:
    neg_moment = 0.086 * total_load * eff_span
    pos_moment = 0.063 * total_load * eff_span
    col_neg_moment = 0.75 * neg_moment
    col_pos_moment = 0.55 * pos_moment
    mid_neg_moment = 0.25 * neg_moment
    mid_pos_moment = 0.45 * pos_moment
    k1 = k(col_neg_moment)
    if k1 > 0.156:
        print('K1 > 0.156. Increase head depth or design compression reinforcement, further analysis required')
    else:
        la1 = la(k1)
        aos1 = a_steel_c(col_neg_moment, la1)
        if aos1 > min_as_col:
            print(f'Column Strip Edge-As required = {round(aos1, 2)}mm²')
            bar = bar_no(aos1, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        else:
            print(f'Column Strip Edge-As required = {round(min_as_col, 2)}mm²')
            bar = bar_no(min_as_col, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
    k2 = k(col_pos_moment)
    if k2 > 0.156:
        print('K2 > 0.156. Increase head depth or design compression reinforcement, further analysis required')
    else:
        la2 = la(k2)
        aos2 = a_steel_c(col_pos_moment, la2)
        if aos2 > min_as_col:
            print(f'Column Strip Span-As required = {round(aos2, 2)}mm²')
            bar = bar_no(aos2, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        else:
            print(f'Column Strip Span-As required = {round(min_as_col, 2)}mm²')
            bar = bar_no(min_as_col, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
    k3 = stiffness(mid_neg_moment)
    if k3 > 0.156:
        print('K3 > 0.156. Increase slab depth or design compression reinforcement, further analysis required')
    else:
        la3 = la(k3)
        aos3 = a_steel(mid_neg_moment, la3)
        if aos3 > min_as:
            print(f'Middle Strip Edge-As required = {round(aos3, 2)}mm²')
            bar = bar_no(aos3, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        else:
            print(f'Middle Strip Edge-As required = {round(min_as, 2)}mm²')
            bar = bar_no(min_as, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
    k4 = stiffness(mid_pos_moment)
    if k4 > 0.156:
        print('K4 > 0.156. Increase slab depth or design compression reinforcement, further analysis required')
    else:
        la4 = la(k4)
        aos4 = a_steel(mid_pos_moment, la4)

        if aos4 > min_as:
            print(f'Middle Strip Span-As required = {round(aos4, 2)}mm²')
            bar = bar_no(aos4, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        else:
            print(f'Middle Strip Span-As required = {round(min_as, 2)}mm²')
            bar = bar_no(min_as, bar_area)
            print(f'Provide {round(bar)}Y{bar_dia}')
        print()
        print('CHECKS')
        pre_m = mid_pos_moment * 10**6 / (short_span * eff_depth1**2)
        fs = (2 / 3) * steel_strength * aos4 / (bar * bar_area)
        mod_factor = 0.55 + (477 - fs) / (120 * (0.9 + pre_m))
        d_req = short_span / (mod_factor * 26)
        if d_req < eff_depth1:
            print('Deflection is satisfactory')
        else:
            print('Deflection not satisfied, increase slab depth')
    shear = 0.6 * total_load

#    print(f'Column Strip Negative Moment = {col_neg_moment}KNm  Shear = {shear}KN')

col_head_per = math.pi * hc * 1000
shear_V = total_load - (eq_load * math.pi * hc**2) / 4
dy_shear = 1.15 * shear_V
shear_stress = (dy_shear * 1000) / (col_head_per * eff_depth2)
vc_conc = 0.8 * conc_strength**0.5
if shear_stress < vc_conc:
    print('Column head section is adequate in shear')
else:
    print('Column head section is inadequate in shear, adjust')
drop_crit_sect = (drop_size / 1000) + (2 * 1.5 * eff_depth1 / 1000)
drop_per = 4 * drop_crit_sect * 1000
force_V = total_load - eq_load * drop_crit_sect**2
dy_shear2 = 1.15 * force_V
shear_str = (dy_shear2 * 1000) / (drop_per * eff_depth1)
if shear_str < vc_conc:
    print('Drop panel section is adequate in shear')
else:
    print('Drop panel section is inadequate in shear, adjust')








#thickness = 200
#print(f'{converters.m_to_mm(thickness)}mm')
#width = 5
#print(f'{converters.m_to_mm(width)}mm')

