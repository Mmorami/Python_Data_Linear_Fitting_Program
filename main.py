from matplotlib import pyplot


# opens the input file in variable file_data
# returns the text data
def open_input_file(file_name):
    file_obj = open(file_name, 'r')
    file_data = file_obj.readlines()
    file_obj.close()
    return file_data


# checks whether the data is sorted in rows or columns
# returns the orientation as either 'r' or 'c'
def check_row_or_col(file):
    col = file[0].lower()
    if ('dx' in col) and ('dy' in col):
        return 'c'
    else:
        return 'r'


# strips the data list of unwanted characters (\n,trailing spaces, and empty items) and splits the strings to lists
# returns the new list
def strip_data(data_list):
    data = []
    for item in data_list:
        if ':' in item:
            item_value_string = item.strip().strip('\n').split(':')
        else:
            item_value_string = item.strip().strip('\n').lower().split()
        if item_value_string:
            data.append(item_value_string)
    return data


# inserts data to rows
# returns a sorted dictionary by keys
def insert_rows(data_list):
    dict_rows = {}
    for item in data_list:

        title = item.pop(0)
        dict_rows[title] = []
        for num in item:
            if ' ' in title:
                dict_rows[title] = num.strip()
            else:
                dict_rows[title].append(float(num.strip()))
    return dict_rows


# inserts data to columns
# returns a sorted dictionary by keys
def insert_cols(data_list):
    dict_cols = {}
    title_list = data_list[0]

    for titles in range(0, len(title_list)):
        dict_cols[title_list[titles]] = []

        for inner_list_index in range(1, len(data_list)):
            if data_list[inner_list_index]:
                if ' ' not in data_list[inner_list_index][0]:
                    dict_cols[title_list[titles]].append(float(data_list[inner_list_index].pop(0)))

    for item in data_list:
        if (item != []) and (' ' in item[0]):
            dict_cols[item.pop(0)] = item[1].strip()
    return dict_cols


# checks for data validation
# 1) that all value lists are equal in size
# 2) that values for dx and dy are non negative
def check_data_validation(data_dict):
    x = data_dict.get('x')
    dx = data_dict.get('dx')
    y = data_dict.get('y')
    dy = data_dict.get('dy')
    dtot = []
    if len(x) == len(dx) == len(y) == len(dy):
        dtot.extend(dx)
        dtot.extend(dy)
        for val in dtot:
            if val < 0:
                raise Exception('Input file error: Not all uncertainties are positive.')
    else:
        raise Exception('Input file error: Data lists are not the same length.')


# inserts the data to a dictionary
# returns the sorted dictionary
def create_dict(file, orientation):
    data = strip_data(file)
    if orientation == 'r':
        data_dict = insert_rows(data)
    else:
        data_dict = insert_cols(data)
    check_data_validation(data_dict)
    return data_dict


# calculates z bar
# returns value for z bar
def calc_z_bar(z, dy):
    numerator = 0
    denominator = 0
    for i in range(0, len(z)):
        numerator += z[i] / (dy[i] ** 2)
        denominator += 1 / (dy[i] ** 2)
    z_bar = numerator/denominator
    return z_bar


# calculates chi^2 for mandatory part
# returns the chi^2 value
def calc_chi_sqr(y, a, x, b, dy, n):
    chi_sqr = 0
    for i in range(n):
        chi_sqr += ((y[i] - (a*x[i] + b))/dy[i])**2
    return chi_sqr


# calculates all parameters for the correlation
# prints the values of a, da, b, db, chi^2, chi^2 red
# returns a list with all parameters' values
def calc_parameters(work_data):

    # defining the basic elements for calculating the factors
    n = len(work_data.get('x'))
    x = work_data.get('x')
    y = work_data.get('y')
    dy = work_data.get('dy')

# elements for calculating correlation's factors

    # a numerator
    xy = [x[i]*y[i] for i in range(n)]
    xy_bar = calc_z_bar(xy, dy)

    x_bar = calc_z_bar(x, dy)

    # a denominator
    x_sqr = [x[i]*x[i] for i in range(n)]
    x_sqr_bar = calc_z_bar(x_sqr, dy)

    # da numerator
    dy_sqr = [dy[i]*dy[i] for i in range(n)]
    dy_sqr_bar = calc_z_bar(dy_sqr, dy)

    # b numerator
    y_bar = calc_z_bar(y, dy)

    # calculating the factors
    a = (xy_bar - (x_bar * y_bar))/(x_sqr_bar - x_bar**2)
    da = (dy_sqr_bar/(n * (x_sqr_bar - x_bar**2))) ** 0.5
    b = (y_bar - a * x_bar)
    db = ((dy_sqr_bar * x_sqr_bar)/(n * (x_sqr_bar - x_bar**2))) ** 0.5

    # calculating chi^2 and chi^2 red
    chi_sqr = calc_chi_sqr(y, a, x, b, dy, n)
    chi_sqr_red = chi_sqr/(n-2)

    print("a = {0} +- {1}".format(a, da))
    print("b = {0} +- {1}".format(b, db))
    print("chi2 = {0}".format(chi_sqr))
    print("chi2_reduced = {0}".format(chi_sqr_red))

    parameters = {'a': a, 'da': da, 'b': b, 'db': db}

    return parameters


# calculates the values (f) of a function with respect to the corresponding parameters and x values
# returns a list of values
def calc_linear_values(x, a, b):
    f = []
    for i in x:
        f.append(b + i * a)
    return f


# plots the data
def plot_correlation(data_dict, parameters):
    x = data_dict.get('x')
    a = parameters.get('a')
    b = parameters.get('b')

    f = calc_linear_values(x, a, b)

    pyplot.plot(x, f, 'red')
    pyplot.errorbar(x=x, y=data_dict.get('y'), yerr=data_dict.get('dy'), xerr=data_dict.get('dx'), fmt='none', ecolor='blue')
    pyplot.ylabel(data_dict.get('y axis'))
    pyplot.xlabel(data_dict.get('x axis'))
    pyplot.show()
    pyplot.savefig(fname='linear_fit', format='svg')


# creates a list of the parameters for iteration
# returns the full list of values
def create_parameter_list(q_data):
    q_values = []
    i = q_data[0]
    while abs(i) <= abs(q_data[1]):
        q_values.append(i)
        i += q_data[2]
    return q_values


# calculates chi^2 for bonus part
def calc_chi_sqr_bonus(y, a, x, b, dy, dx, n):
    x_plus_dx = [x[i] + dx[i] for i in range(n)]
    x_minus_dx = [x[i] - dx[i] for i in range(n)]
    f_numerator = calc_linear_values(x, a, b)
    f_x_plus_dx = calc_linear_values(x_plus_dx, a, b)
    f_x_minus_dx = calc_linear_values(x_minus_dx, a, b)

    chi_sqr = 0
    for i in range(n):
        chi_sqr += ((y[i] - f_numerator[i])/((dy[i])**2 + (f_x_plus_dx[i] - f_x_minus_dx[i])**2)**0.5)**2
    return chi_sqr


# Numerically searches for best fit parameters
# prints the values of a, da, b, db, chi^2, chi^2 red
# returns a list with all parameters' values
def numeric_fit(work_data):

    # defining parameters needed for chi calculation
    n = len(work_data.get('x'))
    x = work_data.get('x')
    y = work_data.get('y')
    dx = work_data.get('dx')
    dy = work_data.get('dy')

    a_data = work_data.get('a')
    b_data = work_data.get('b')
    a_values = create_parameter_list(a_data)
    b_values = create_parameter_list(b_data)

    # defines initial parameters for comparing best a & b pair
    best_chi = calc_chi_sqr(y, a_values[0], x, b_values[0], dy, n)
    best_a = a_values[0]
    best_b = b_values[0]

    for i in a_values:
        for j in b_values:
            chi_sqr = calc_chi_sqr_bonus(y, i, x, j, dy, dx, n)
            if chi_sqr <= best_chi:
                best_chi = chi_sqr
                best_a = i
                best_b = j
    best_chi_red = best_chi/(n-2)

    print("a = {0:.2f} +- {1}".format(best_a, abs(a_data[2])))
    print("b = {0:.2f} +- {1}".format(best_b, abs(b_data[2])))
    print("chi2 = {0}".format(best_chi))
    print("chi2_reduced = {0}".format(best_chi_red))

    parameters = {'a': best_a, 'da': a_data[2], 'b': best_b, 'db': b_data[2], 'a_list': a_values}
    return parameters


# plots chi function
def plot_chi(work_data, parameters):
    a = parameters.get('a_list')
    b = parameters.get('b')

    n = len(work_data.get('x'))
    x = work_data.get('x')
    y = work_data.get('y')
    dx = work_data.get('dx')
    dy = work_data.get('dy')

    f = []
    for i in a:
        f.append(calc_chi_sqr_bonus(y, i, x, b, dy, dx, n))
    pyplot.plot(a, f, 'blue')
    pyplot.ylabel('chi2(a, b = {0:.2f})'.format(b))
    pyplot.xlabel('a')
    pyplot.show()
    pyplot.savefig(fname='numeric_sampling', format='svg')


# Bonus function
def search_best_parameter(filename):
    raw_data = open_input_file(filename)
    data_orientation = check_row_or_col(raw_data)
    try:
        workable_data = create_dict(raw_data, data_orientation)
        correlation_parameters = numeric_fit(workable_data)
        plot_correlation(workable_data, correlation_parameters)
        plot_chi(workable_data, correlation_parameters)
    except Exception as ex:
        print(ex)


# Main function
def fit_linear(filename):
    raw_data = open_input_file(filename)
    data_orientation = check_row_or_col(raw_data)

    try:
        workable_data = create_dict(raw_data, data_orientation)
        correlation_parameters = calc_parameters(workable_data)
        plot_correlation(workable_data, correlation_parameters)
    except Exception as ex:
        print(ex)


# fit_linear('input_rows.txt')
# print()
# search_best_parameter('input.txt')

