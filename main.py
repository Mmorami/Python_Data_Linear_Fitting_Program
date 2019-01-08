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


# calculates chi^2 and chi^ red
# prints the values of a, da, b, db, chi^2, chi^2 red
# returns a list with all parameters' values
def calc_chi_sqr(work_data):

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
    chi_sqr = 0
    for i in range(n):
        chi_sqr += ((y[i] - (a*x[i] + b))/dy[i])**2
    chi_sqr_red = chi_sqr/(n-2)

    print("a = {0} +- {1}".format(a, da))
    print("b = {0} +- {1}".format(b, db))
    print("chi2 = {0}".format(chi_sqr))
    print("chi2_reduced = {0}".format(chi_sqr_red))

    parameters = {'a': a, 'da': da, 'b': b, 'db': db}

    return parameters


# plots the data
def plot_correlation(data_dict, parameters):
    x = data_dict.get('x')
    a = parameters.get('a')
    b = parameters.get('b')
    f = []
    for i in x:
        f.append(b + i * a)
    pyplot.plot(x, f, 'red')
    pyplot.errorbar(x=x, y=data_dict.get('y'), yerr=data_dict.get('dy'), xerr=data_dict.get('dx'), fmt='none', ecolor='blue')
    pyplot.ylabel(data_dict.get('y axis'))
    pyplot.xlabel(data_dict.get('x axis'))
    pyplot.show()
    pyplot.savefig(fname='linear_fit', format='svg')


# Main function
def fit_linear(filename):
    # raw_data = open_input_file(filename)
    raw_data = open_input_file('input_cols.txt')
    data_orientation = check_row_or_col(raw_data)

    try:
        workable_data = create_dict(raw_data, data_orientation)
        correlation_parameters = calc_chi_sqr(workable_data)
        plot_correlation(workable_data, correlation_parameters)
    except Exception as ex:
        print(ex)
